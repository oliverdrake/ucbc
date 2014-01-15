from functools import partial
from django.contrib import admin, messages
from .models import Grain, Hop, UserOrder, Supplier, OrderItem, SupplierOrder, OrdersEnabled
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


class UserOrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline, )
    list_display = ("id", "username", "total_excl_gst", "status")
    readonly_fields = ("total_excl_gst", )


class SupplierOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "supplier_name", "status", "total_excl_gst")
    readonly_fields = ("total_excl_gst",)
    form = SupplierOrderAdminForm


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

admin.site.register(Grain, IngredientAdmin)
admin.site.register(Hop, IngredientAdmin)
admin.site.register(UserOrder, UserOrderAdmin)
admin.site.register(Supplier)
admin.site.register(SupplierOrder, SupplierOrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrdersEnabled, OrdersEnabledAdmin)
