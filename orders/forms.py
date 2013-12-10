from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from orders.models import OrderItem, SupplierOrder


class SelectIngredientOrderWidget(FilteredSelectMultiple):
    field = None
    #def __init__(self, field, verbose_name, is_stacked, attrs=None, choices=()):
    #    self.field = field
    #    super(SelectIngredientOrderWidget, self).__init__(verbose_name, is_stacked, attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        selected_ingredients = [e.ingredient.name for e in self.field.queryset.all()]
        return super(SelectIngredientOrderWidget, self).render(
            name, value=selected_ingredients, attrs=attrs, choices=choices)


#class SelectIngredientOrderField(forms.ModelMultipleChoiceField):
#    def __init__(self, queryset, cache_choices=False, required=True,
#                 widget=None, label=None, initial=None,
#                 help_text='', *args, **kwargs):
#        if widget is not None:
#            widget.
#        super(SelectIngredientOrderField, self).__init__(queryset, cache_choices=False, required=True,
#                 widget=None, label=None, initial=None,
#                 help_text='', *args, **kwargs)


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


