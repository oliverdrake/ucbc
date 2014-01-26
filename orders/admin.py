from functools import partial
from django.contrib import admin, messages
from .models import Grain, Hop, UserOrder, Supplier, OrderItem, SupplierOrder, OrdersEnabled, Surcharge
from orders.forms import SupplierOrderAdminForm


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "supplier_name", "unit_cost_excl_gst", "unit_size")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    verbose_name_plural = "Add Ingredients"
    verbose_name = "Item"
    fields = ("ingredient", "quantity")


class ReadOnlyOrderItemInline(OrderItemInline):
    def get_readonly_fields(self, request, obj=None):
        return self.model._meta.get_all_field_names()


def flag_as_paid(modeladmin, request, queryset):
    queryset.update(status=UserOrder.STATUS_PAID)


class UserOrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline, )
    list_display = ("id", "username", "total_excl_gst", "status")
    readonly_fields = ("total_excl_gst", )
    actions = (flag_as_paid, )


class SupplierOrderAdmin(admin.ModelAdmin):
    list_display = ("supplier_name", "status", "total_excl_gst")
    readonly_fields = ("supplier", "total_excl_gst", "total_incl_gst")
    change_form_template = 'orders/supplier_order_change_form.html'

    def get_queryset(self, request):
        supplier_orders = SupplierOrder.objects.filter(status=SupplierOrder.STATUS_PENDING)
        for supplier in Supplier.objects.all():
            order, _ = supplier_orders.get_or_create(supplier=supplier)
            OrderItem.objects.filter(
                supplier_order=None,
                ingredient__supplier=supplier).update(supplier_order=order)
        return SupplierOrder.objects.all()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def add_to_supplier_order(supplier_order, modeladmin, request, queryset):
    if queryset.filter(user_order__status=UserOrder.STATUS_UNPAID).count() > 0:
        messages.warning(request, "Some order items selected could not be added to supplier order as they havn't been paid for")
    queryset.filter(user_order__status=UserOrder.STATUS_PAID).update(supplier_order=supplier_order)


def remove_from_supplier_orders(modeladmin, request, queryset):
    queryset.update(supplier_order=None)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "quantity", "unit_size", "user_order", "supplier_order", "paid")
    list_per_page = 200
    list_filter = ("ingredient__supplier__name", "user_order__status")
    readonly_fields = ("user_order", )
    actions = (remove_from_supplier_orders, )

    def get_actions(self, request):
        actions = super(OrderItemAdmin, self).get_actions(request)
        for order in SupplierOrder.pending_orders():
            name = "Add to %s" % order
            actions[name] = (partial(add_to_supplier_order, order), name, name)
        return actions

    def has_add_permission(self, request):
        return False


class OrdersEnabledAdmin(admin.ModelAdmin):
    list_display = ("name", "enabled", )

    def name(self, *args, **kwargs):
        return "Orders Enabled"


class SurchargeAdmin(admin.ModelAdmin):
    list_display = ("name", "surcharge_percentage", "order_surcharge")

    def name(self, *args, **kwargs):
        return "Surcharges"


admin.site.register(Grain, IngredientAdmin)
admin.site.register(Hop, IngredientAdmin)
admin.site.register(UserOrder, UserOrderAdmin)
admin.site.register(Supplier)
admin.site.register(SupplierOrder, SupplierOrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrdersEnabled, OrdersEnabledAdmin)
admin.site.register(Surcharge, SurchargeAdmin)
