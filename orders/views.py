import csv
from functools import wraps
from http.client import OK, CREATED, BAD_REQUEST
from io import StringIO
import logging
# from bootstrap.future import SessionWizardView
import mimetypes
from urllib.parse import urljoin

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, render, get_object_or_404
from django.forms.formsets import formset_factory
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_GET
from paypal.standard.forms import PayPalPaymentsForm

from orders import models
from orders.forms import CartItemForm, OrderItemFormset
from orders.models import OrdersEnabled
from orders.utils import get_ingredient

log = logging.getLogger(__name__)


def orders_enabled(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if OrdersEnabled.is_enabled():
            return view(request, *args, **kwargs)
        message = "Sorry, we're not currently taking orders, keep an eye on our facebook page."
        return render(
            request,
            'orders/orders_disabled.html',
            {'error': message},
            status=BAD_REQUEST)
    return wrapper


def main(request):
    return render_to_response('orders/main.html', context_instance=RequestContext(request))


def create_cart_formset(request, user_order=None):
    cart = _get_cart_from_session(request)
    initial = [dict(ingredient=get_ingredient(name), quantity=q) for name, q in cart.items()]
    Formset = inlineformset_factory(
        models.UserOrder,
        models.OrderItem,
        formset=OrderItemFormset,
        extra=len(initial),
        max_num=len(initial),
        fields=("quantity", "ingredient"),
        widgets={
            "ingredient": forms.HiddenInput(),
            "quantity": forms.HiddenInput(),
        })
    data = request.POST if request.POST else None
    if not user_order:
        user_order = models.UserOrder(user=request.user)
    cart_formset = Formset(
        data=data,
        instance=user_order,
        initial=initial,
        prefix="cart")
    return cart_formset


class OrderIngredientView(TemplateView):
    http_method_names = ['get', 'post']
    model = None

    @staticmethod
    def _update_session(formset, request):
        if formset.is_valid():
            for cleaned_data in formset.cleaned_data:
                quantity = cleaned_data.get("quantity", 0)
                ingredient_name = cleaned_data.get("ingredient_name")
                cart = _get_cart_from_session(request)
                if quantity and quantity > 0:
                    cart[ingredient_name] = quantity + cart.get(ingredient_name, 0)
                    request.session.modified = True

    @method_decorator(login_required)
    @method_decorator(orders_enabled)
    def get(self, request, *args, **kwargs):
        ingredient_formset = self.formset_class(initial=self.initial, prefix="ingredients")
        cart_formset = create_cart_formset(request)
        return render(
            request,
            'orders/ingredient_list.html', {
                'title': self.title,
                'ingredient_formset': ingredient_formset,
                'cart_formset': cart_formset})

    @method_decorator(login_required)
    @method_decorator(orders_enabled)
    def post(self, request, *args, **kwargs):
        formset = self.formset_class(request.POST, initial=self.initial, prefix="ingredients")
        if formset.is_valid():
            self.__class__._update_session(formset, request)
            return HttpResponseRedirect('')
        return render(
            request,
            'orders/ingredient_list.html', {
                'title': self.title,
                'ingredient_formset': formset},
            status=BAD_REQUEST)

    @property
    def initial(self):
        return [dict(
            ingredient_name=i.name,
            quantity=0, unit_cost=i.unit_cost_excl_gst_incl_surcharge,
            unit_size=i.unit_size) for i in self.model.objects.all()]

    @property
    def formset_class(self):
        return formset_factory(CartItemForm, max_num=len(self.initial))

    @property
    def title(self):
        return self.__class__.__name__


class Grains(OrderIngredientView):
    model = models.Grain


class Hops(OrderIngredientView):
    model = models.Hop


@require_GET
@login_required
def review_order(request):
    cart_formset = create_cart_formset(request)

    # paypal_dict = {
    #     "business": settings.PAYPAL_RECEIVER_EMAIL,
    #     "amount": order_total(cart_formset),
    #     "item_name": "Order #%d" % models.UserOrder.objects.count() + 1,
    #     "invoice": "unique-invoice-id",
    #     "notify_url": request.build_absolute_uri(reverse('paypal_ipn')),
    #     "return_url": request.build_absolute_uri(reverse('order_complete')),
    #     "cancel_return": request.get_full_path(),
    #
    # }

    # Create the instance.
    # form = PayPalPaymentsForm(initial={
    #     "business": settings.PAYPAL_RECEIVER_EMAIL,
    #     "amount": order_total(cart_formset),
    #     "item_name": "Order #%d" % (models.UserOrder.objects.count() + 1),
    #     "invoice": "unique-invoice-id",
    #     "notify_url": request.build_absolute_uri('payment/ASD45623SDF7878aetrty/'),
    #     "return_url": request.build_absolute_uri(reverse('checkout')),
    #     "cancel_return": request.get_full_path(),
    #
    # })
    # context = {"form": form}
    # return render_to_response("payment.html", context)

    return render(request, 'orders/review_cart.html', {'cart_formset': cart_formset})


@require_POST
@login_required
def checkout(request):
    # ToDo: check that order has been reviewed!
    # ToDo: Email user a summary
    user_order = models.UserOrder.objects.create(user=request.user)
    formset = create_cart_formset(request, user_order)
    if formset.is_valid():
        formset.save()
        del request.session['cart']



        # _email_order_confirmation(request, user_order)
        return HttpResponseRedirect(redirect_to=reverse('payment', args=(formset.instance.id,)))
    user_order.delete()
    # ToDo: email admin on failure
    return HttpResponseBadRequest('Could not complete your order')


@require_GET
@login_required
def payment(request, order_id):
    order_id = int(order_id)



    form = PayPalPaymentsForm(initial={
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "%5.2f" % models.UserOrder.objects.get(id=order_id).total,
        "item_name": "UCBC Grain/Hop Order #%d" % order_id,
        "invoice": str(order_id),
        "notify_url": urljoin(request.META['wsgi.url_scheme'] + "://" + request.get_host(), 'payment/ASD45623SDF7878aetrty/'),
        "return_url": urljoin(request.META['wsgi.url_scheme'] + "://" + request.get_host(), ''),
        "cancel_return": request.get_full_path(),

    })
    return render(request, 'orders/payment.html', {'form': form})


def order_complete(request, order_id):
    return render(request, 'orders/order_complete.html', {'order_id': order_id})


@require_POST
@login_required
def cart_delete_item(request):
    cart = _get_cart_from_session(request)
    try:
        ingredient_id = int(request.POST.get('ingredient_id'))
        ingredient_name = models.Ingredient.objects.get(id=ingredient_id).name
        if ingredient_name in cart:
            del cart[ingredient_name]
            request.session.modified = True
    except KeyError:
        log.error("cart_delete_item: no ingredient_id key in POST data. POST: %s" % request.POST)
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse()


@require_GET
@login_required
def supplier_order_summary_csv(request, order_id):
    order = get_object_or_404(models.SupplierOrder, id=order_id)
    response = HttpResponse(content_type=mimetypes.types_map['.csv'])
    response['Content-Disposition'] = 'attachment; filename="%s_order.csv"' % order.supplier.name

    writer = csv.writer(response)
    writer.writerow(['Name', 'Quantity'])
    for name, (quantity, total) in order.summary.items():
        ingredient = models.Ingredient.objects.get(name=name)
        humanized_quantity = models.Ingredient.unit_size_plural(ingredient.unit_size, quantity)
        writer.writerow([name, humanized_quantity])
    return response


@login_required
def import_ingredients_from_csv(request, model_name):
    if hasattr(models, model_name):
        model_ = getattr(models, model_name)
    else:
        raise Http404()

    class UploadFileForm(forms.Form):
        file = forms.FileField(widget=forms.FileInput(attrs={"class": "form-control input-sm"}))

    class IngredientUploadForm(forms.ModelForm):
        class Meta:
            model = model_

    if request.method == "POST":
        contents = "".join([c.decode(encoding='UTF-8') for c in request.FILES['file'].chunks()])
        reader = csv.reader(StringIO(contents))
        for row in reader:
            if reader.line_num > 1:
                form = IngredientUploadForm(data={
                    'name': row[0],
                    'unit_cost': float(row[1]),
                    'unit_size': row[2],
                    'supplier': get_object_or_404(models.Supplier, name=row[3]).id,
                })
                if form.is_valid():
                    form.save()
                else:
                    log.info("Import validation errors: %s" % form.errors)
        return HttpResponseRedirect('')
    else:

        form = UploadFileForm()
        return render(request, 'orders/import_ingredients.html', {'form': form})


def _get_cart_from_session(request):
    return request.session.setdefault('cart', {})
