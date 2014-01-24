from django.db import models
from django.contrib.auth import get_user_model


class Supplier(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    UNIT_SIZE_KG = "Kg"
    UNIT_SIZE_SACK = "sack"
    UNIT_SIZE_100G = "100g"

    name = models.CharField(max_length=255, blank=False, unique=True)
    unit_cost = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        blank=False,
        verbose_name="Unit Cost (NZD) (excl. GST)")
    unit_size = models.CharField(
        max_length=255,
        choices=(
            (UNIT_SIZE_KG, "1 Kg"),
            (UNIT_SIZE_SACK, "Sack (25Kg)"),
            (UNIT_SIZE_100G, "100 gram")),
        blank=False, null=True)
    supplier = models.ForeignKey(Supplier, related_name="ingredients", blank=False, null=True, default=None)

    @staticmethod
    def unit_size_plural(unit_size, quantity):
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("invalid quantity: %d" % quantity)
        if unit_size in (Ingredient.UNIT_SIZE_SACK, Ingredient.UNIT_SIZE_KG):
            if quantity is not 1:
                unit_size = unit_size + "s"
            return "%d %s" % (quantity, unit_size)
        elif unit_size == Ingredient.UNIT_SIZE_100G:
            if quantity < 10:
                return "%d00 grams" % quantity
            else:
                quantity = float(quantity) / 10
                return "%3.1f Kg" % quantity
        else:
            raise ValueError("invalid unit size: %s" % unit_size)

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


class _BaseOrder(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class SupplierOrder(_BaseOrder):
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

    @property
    def summary(self):
        items = {}
        for item in self.ingredient_orders.all():
            name = item.ingredient.name
            quantity, total = items.setdefault(name, (0, 0))
            quantity += item.quantity
            total += float(item.total)
            items[name] = (quantity, total)
        return items

    def supplier_name(self):
        return self.supplier.name

    def total_excl_gst(self):
        return "$%3.2f" % self.total

    def total_incl_gst(self):
        from orders.utils import add_gst
        return "$%3.2f" % add_gst(self.total)

    def total_in_unpaid_order_items(self):
        unpaid_order_items = OrderItem.objects.filter(ingredient__supplier=self.supplier)
        unpaid_order_items.filter(order__status=UserOrder.STATUS_UNPAID)
        return "$%3.2f" % sum([i.total for i in unpaid_order_items])
    total_in_unpaid_order_items.short_description = "Unpaid order items"

    def __str__(self):
        return "%s %d: %s (%s)" % (self.__class__.__name__, self.id, self.supplier.name, self.status)


class UserOrder(_BaseOrder):
    STATUS_UNPAID = "unpaid"
    STATUS_PAID = "paid"
    status = models.CharField(
        max_length=255,
        choices=(
            (STATUS_UNPAID, "unpaid"),
            (STATUS_PAID, "paid")),
        blank=False,
        default=STATUS_UNPAID)
    user = models.ForeignKey(get_user_model(), related_name="orders", blank=False)

    @property
    def total(self):
        # ToDo: might be worth moving this into sql
        return sum([o.total for o in self.order_items.all()])

    def username(self):
        return self.user.username

    def total_excl_gst(self):
        return "$%3.2f" % self.total

    def __str__(self):
        return "%s %d: %s" % (self.__class__.__name__, self.id, self.username())


class OrderItem(models.Model):
    """ One entry in an order """
    ingredient = models.ForeignKey(Ingredient, related_name="single_ingredient_orders", blank=False)
    quantity = models.PositiveIntegerField(blank=False)
    user_order = models.ForeignKey(UserOrder, related_name="order_items", blank=False)
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
        return self.user_order.username()

    def unit_size(self):
        return self.ingredient.unit_size

    def unit_cost(self):
        return self.ingredient.unit_cost

    def paid(self):
        return self.user_order.status


class OrdersEnabled(models.Model):
    """
    Singleton flag used to enable/disable orders (for periods of time where there's no
    orders in the foreseeable future.
    Idea borrowed from https://github.com/defbyte/django-singleton
    """
    enabled = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        verbose_name_plural = 'Orders Enabled'

    @classmethod
    def is_enabled(cls):
        return cls.objects.get_or_create(id=1)[0].enabled

    def save(self, *args, **kwargs):
        self.id = 1
        super(OrdersEnabled, self).save(*args, **kwargs)
