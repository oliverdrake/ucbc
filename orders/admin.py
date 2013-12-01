from django.contrib import admin
from .models import Grain, Hop, UserOrder, Supplier, SingleIngredientOrder


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "supplier_name", "unit_cost_excl_gst", "unit_size")


class SingleIngredientOrderInline(admin.TabularInline):
    model = SingleIngredientOrder
    extra = 1
    verbose_name_plural = "Add Ingredients"


class UserOrderAdmin(admin.ModelAdmin):
    inlines = (SingleIngredientOrderInline, )
    list_display = ("id", "username", "total_excl_gst")


admin.site.register(Grain, IngredientAdmin)
admin.site.register(Hop, IngredientAdmin)
admin.site.register(UserOrder, UserOrderAdmin)
admin.site.register(Supplier)
