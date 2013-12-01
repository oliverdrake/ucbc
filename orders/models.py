from django.db import models
from django.contrib.auth import get_user_model

SUPPLIER_GLADFIELDS = "Gladfields"
SUPPLIER_MALTEUROPE = "Malteurope"
SUPPLIER_NZHOPS = "NZHops"


class Supplier(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255, blank=False)
    unit_cost = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        blank=False,
        verbose_name="Unit Cost (NZD) (excl. GST)")
    unit_size = models.CharField(
        max_length=255,
        choices=(
            ("Kg", "1 Kg"),
            ("sack", "Sack (25Kg)"),
            ("100g", "100 gram")),
        blank=False, null=True)
    supplier = models.ForeignKey(Supplier, related_name="ingredients", blank=False, null=True, default=None)

    def supplier_name(self):
        return self.supplier.name

    def unit_cost_excl_gst(self):
        return "$%3.2f" % (self.unit_cost)

    def __str__(self):
        return "%s (%s)" % (self.name, self.supplier.name)


class Grain(Ingredient):
    pass


class Hop(Ingredient):
    pass


class AbstractOrder(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ORDERED = "ordered"
    STATUS_READY_FOR_PICKUP = "ready_for_pickup"
    status = models.CharField(
        max_length=255,
        choices=(
            (STATUS_PENDING, "pending"),
            (STATUS_ORDERED, "ordered from supplier"),
            (STATUS_READY_FOR_PICKUP, "arrived and ready for pickup")),
        blank=False)
    class Meta:
        abstract = True


class SupplierOrder(AbstractOrder):
    supplier = models.ForeignKey(Supplier, related_name="orders", blank=False)


class UserOrder(AbstractOrder):
    user = models.ForeignKey(get_user_model(), related_name="orders", blank=False)

    @property
    def total(self):
        return sum([o.total for o in self.ingredient_orders.all()])

    def username(self):
        return self.user.username

    def total_excl_gst(self):
        return "$%3.2f" % self.total


class SingleIngredientOrder(models.Model):
    """ One entry in an order """
    ingredient = models.ForeignKey(Ingredient, related_name="single_ingredient_orders", blank=False)
    quantity = models.PositiveIntegerField(blank=False)
    order = models.ForeignKey(UserOrder, related_name="ingredient_orders", blank=False)

    def __str__(self):
        return "Ingredient"

    @property
    def ingredient_name(self):
        return self.ingredient.name

    @property
    def total(self):
        """ Total Excluding GST """
        return self.quantity * self.ingredient.unit_cost
