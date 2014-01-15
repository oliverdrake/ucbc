from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple, ForeignKeyRawIdWidget
from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms.models import BaseInlineFormSet

from orders.models import OrderItem, SupplierOrder, Ingredient, UserOrder


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


class CartItemForm(forms.Form):
    ingredient_name = forms.CharField(widget=forms.HiddenInput())
    unit_cost = forms.DecimalField(widget=forms.HiddenInput())
    unit_size = forms.CharField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(widget=forms.widgets.TextInput(attrs={
        "class": "form-control input-sm",
        "value": "0"}))


class OrderItemFormset(BaseInlineFormSet):
    def clean(self):
        super(OrderItemFormset, self).clean()
        # Dirty hack as I can't get inline formsets to work
        for i, form in enumerate(self.forms):
            prefix = '%s-%d-' % (self.prefix, i)
            ingredient_id = int(form.data.get(prefix + "ingredient"))
            quantity = int(form.data.get(prefix + "quantity"))
            form.instance.ingredient = Ingredient.objects.get(id=ingredient_id)
            form.instance.quantity = quantity

    def save(self, commit=True):
        super(OrderItemFormset, self).save(commit=commit)
        for form in self.forms:
            if form.is_valid():
                form.save()


class SupplierOrderAdminForm(forms.ModelForm):
    class Meta:
        model = SupplierOrder

    ingredient_orders = forms.ModelMultipleChoiceField(
        required=False,
        queryset=OrderItem.objects.all(),
        widget=FilteredSelectMultiple(verbose_name='Order Items', is_stacked=False),
        help_text="Select order items to add to this supplier order. " +
                  "Note: unpaid user orders are excluded from this list.")

    def __init__(self, *args, **kwargs):
        super(SupplierOrderAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['ingredient_orders'].initial = self.instance.ingredient_orders.all()
            self.fields['ingredient_orders'].queryset = OrderItem.objects.\
                filter(ingredient__supplier=self.instance.supplier).\
                filter(user_order__status=UserOrder.STATUS_PAID)

    def save(self, *args, **kwargs):
        instance = super(SupplierOrderAdminForm, self).save(commit=False)
        self.fields['ingredient_orders'].initial.update(supplier_order=None)
        self.cleaned_data['ingredient_orders'].update(supplier_order=instance)
        return instance
