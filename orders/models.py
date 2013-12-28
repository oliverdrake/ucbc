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
    name = models.CharField(max_length=255, blank=False, unique=True)
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
    ingredient_type = "grain"


class Hop(Ingredient):
    ingredient_type = "hops"


#class AbstractOrder(models.Model):
#
#    class Meta:
#        abstract = True


class SupplierOrder(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ORDERED = "ordered"
    STATUS_ARRIVED = "arrived"
    status = models.CharField(
        max_length=255,
        choices=(
            (STATUS_PENDING, "pending"),
            (STATUS_ORDERED, "ordered from supplier"),
            (STATUS_ARRIVED, "arrived and ready to be distributed")),
        blank=False,
        default=STATUS_PENDING)
    supplier = models.ForeignKey(Supplier, related_name="orders", blank=False)

    @classmethod
    def pending_orders(cls):
        return cls.objects.filter(status=cls.STATUS_PENDING)

    @property
    def total(self):
        return sum([item.total for item in self.ingredient_orders.all()])

    def supplier_name(self):
        return self.supplier.name

    def total_excl_gst(self):
        return "$%3.2f" % self.total

    def total_in_unpaid_order_items(self):
        unpaid_order_items = OrderItem.objects.filter(ingredient__supplier=self.supplier)
        unpaid_order_items.filter(order__status=UserOrder.STATUS_UNPAID)
        return "$%3.2f" % sum([i.total for i in unpaid_order_items])
    total_in_unpaid_order_items.short_description = "Unpaid order items"

    def __str__(self):
        return "%s %d: %s (%s)" % (self.__class__.__name__, self.id, self.supplier.name, self.status)


class UserOrder(models.Model):
    STATUS_UNPAID = "unpaid"
    STATUS_PAID = "paid"
    status = models.CharField(
        max_length=255,
        choices=(
            (STATUS_UNPAID, "unpaid"),
            (STATUS_PAID, "paid")),
        editable=False,
        blank=False,
        default=STATUS_UNPAID)
    user = models.ForeignKey(get_user_model(), related_name="orders", blank=False)

    @property
    def total(self):
        return sum([o.total for o in self.ingredient_orders.all()])

    def username(self):
        return self.user.username

    def total_excl_gst(self):
        return "$%3.2f" % self.total

    def __str__(self):
        return "%s %d: %s" % (self.__class__.__name__, self.id, self.username())


class OrderItem(models.Model):
    """ One entry in an order """
    STATUS_PENDING = "pending"
    STATUS_ORDERED = "ordered_from_supplier"
    STATUS_READY_FOR_PICKUP = "ready_for_pickup"
    status = models.CharField(
        max_length=255,
        choices=(
            (STATUS_PENDING, "pending"),
            (STATUS_ORDERED, "ordered from supplier"),
            (STATUS_READY_FOR_PICKUP, "arrived and ready for pickup")),
        blank=False,
        default=STATUS_PENDING)
    ingredient = models.ForeignKey(Ingredient, related_name="single_ingredient_orders", blank=False)
    quantity = models.PositiveIntegerField(blank=False)
    order = models.ForeignKey(UserOrder, related_name="ingredient_orders", blank=False)
    supplier_order = models.ForeignKey(
        SupplierOrder,
        related_name="ingredient_orders",
        blank=True,
        null=True,
        default=None)

    def __str__(self):
        return "%s, %s, tot: $%2.2f" % (
            self.ingredient.name,
            self.ingredient.supplier_name(),
            self.total)

    @property
    def ingredient_name(self):
        return self.ingredient.name

    @property
    def total(self):
        """ Total Excluding GST """
        return self.quantity * self.ingredient.unit_cost

    def username(self):
        return self.order.username()

    def unit_size(self):
        return self.ingredient.unit_size

    def unit_cost(self):
        return self.ingredient.unit_cost

    def paid(self):
        return self.order.status
