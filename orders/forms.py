from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from orders.models import OrderItem, SupplierOrder


class SelectIngredientOrderWidget(FilteredSelectMultiple):
    field = None

    def render(self, name, value, attrs=None, choices=()):
        selected_ingredients = [e.ingredient.name for e in self.field.queryset.all()]
        return super(SelectIngredientOrderWidget, self).render(
            name, value=selected_ingredients, attrs=attrs, choices=choices)


class SupplierSelectIngredientsForm(forms.ModelForm):

    class Meta:
        model = SupplierOrder
        fields = ("supplier", "status", "ingredient_orders")

    ingredient_orders = forms.ModelMultipleChoiceField(
        queryset=OrderItem.objects,
        label="Select Ingredients",
        widget=SelectIngredientOrderWidget("which ingredients to order", is_stacked=False),
        required=False
    )
    ingredient_orders.widget.field = ingredient_orders

    def save(self, commit=True):
        super(SupplierSelectIngredientsForm, self).save(commit=commit)


# class OrderItemForm(forms.ModelForm):
#     class Meta:
#         model = OrderItem
#         fields = ("quantity", )
#         widgets = {
#             'quantity': forms.widgets.TextInput(attrs={
#                 "class": "form-control input-sm",
#                 "value": "0"}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         if "initial" in kwargs:
#             self.ingredient = kwargs["initial"].get("ingredient", None)
#         super(OrderItemForm, self).__init__(*args, **kwargs)


# class OrderItemForm(forms.ModelForm):



class CartItemForm(forms.Form):
    ingredient_name = forms.CharField(widget=forms.HiddenInput())
    unit_cost = forms.DecimalField(widget=forms.HiddenInput())
    unit_size = forms.CharField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(widget=forms.widgets.TextInput(attrs={
        "class": "form-control input-sm",
        "value": "0"}))

