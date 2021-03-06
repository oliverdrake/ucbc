from django.db import models
from django.contrib.auth import get_user_model

# Register Signals
from paypal.standard.ipn.signals import payment_was_successful
from orders import signals
payment_was_successful.connect(signals.order_paid, dispatch_uid="paypal_payment_success")


class Supplier(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class _UnitSizeSack(object):
    name = "sack"
    description = "Sack (25Kg)"

    def plural(self, quantity):
        unit_size = self.name
        if quantity is not 1:
            unit_size = self.name + "s"
        return "%d %s" % (quantity, unit_size)


class _UnitSizeKg(object):
    name = "Kg"
    description = "1 Kg"

    def plural(self, quantity):
        if quantity == 1:
            return "1 Kg"
        return "%dx 1Kg" % quantity


class _UnitSize100G(object):
    name = "100g"
    description = "100 gram"

    def plural(self, quantity):
        if quantity == 0:
            return "0"
        elif quantity == 1:
            return "100g"
        else:
            return "%dx 100g" % quantity


class _UnitSize5Kg(object):
    name = "5Kg"
    description = ("5Kg bag")

    def plural(self, quantity):
        return "%dx 5Kg bag%s" % (quantity, 's' if quantity > 1 else '')


class Ingredient(models.Model):
    UNITS = (_UnitSizeSack(), _UnitSizeKg(), _UnitSize100G(), _UnitSize5Kg())

    name = models.CharField(max_length=255, blank=False, unique=True)
    unit_cost = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        blank=False,
        verbose_name="Unit Cost (NZD) (excl. GST)")
    unit_size = models.CharField(
        max_length=255,
        choices=((u.name, u.description) for u in UNITS),
        blank=False, null=True)
    supplier = models.ForeignKey(Supplier, related_name="ingredients", blank=False, null=True, default=None)

    @staticmethod
    def unit_size_plural(unit_size, quantity):
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("invalid quantity: %d" % quantity)

        try:
            unit = next(filter(lambda u: u.name == unit_size, Ingredient.UNITS))
        except StopIteration:
            raise ValueError("Invalid/unknown unit_size: %s" % unit_size)
        return unit.plural(quantity)

    def supplier_name(self):
        return self.supplier.name

    def unit_cost_excl_gst(self):
        return "$%3.2f" % (self.unit_cost)

    @property
    def unit_cost_excl_gst_incl_surcharge(self):
        return float(self.unit_cost) * Surcharge.get_factor()

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
        from orders.utils import add_gst
        return add_gst(sum([o.total for o in self.order_items.all()])) + Surcharge.get_order_surcharge()

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
        return self.quantity * self.ingredient.unit_cost_excl_gst_incl_surcharge

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
        return super(OrdersEnabled, self).save(*args, **kwargs)


class Surcharge(models.Model):
    surcharge_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False,
                                               default=0.0, help_text="surcharge as a percentage cut of the order [0-100%]")
    order_surcharge = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False,
                                          default=0.0, help_text="Surcharge in $ per order on top of percentage cut")

    @classmethod
    def get_surcharge_percentage(cls):
        surcharge, _ = cls.objects.get_or_create(id=1)
        return float(surcharge.surcharge_percentage)

    @classmethod
    def get_factor(cls):
        return 1 + cls.get_surcharge_percentage() / 100

    @classmethod
    def get_order_surcharge(cls):
        surcharge, _ = cls.objects.get_or_create(id=1)
        return float(surcharge.order_surcharge)
