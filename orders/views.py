from http.client import OK, CREATED, BAD_REQUEST
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response, render
from django.forms.formsets import formset_factory
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from orders import models
from orders.forms import OrderItemForm
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_GET


def _get_cart_from_session(request):
    return request.session.setdefault('cart', {})


def main(request):
    return render_to_response('orders/main.html', context_instance=RequestContext(request))


class OrderIngredientView(TemplateView):
    http_method_names = ['get', 'post']
    model = None

    @staticmethod
    def _update_session(formset, request):
        if formset.is_valid():
            for form, cleaned_data in zip(formset, formset.cleaned_data):
                quantity = cleaned_data.get("quantity", 0)
                cart = _get_cart_from_session(request)
                if quantity and quantity > 0:
                    cart[form.ingredient.name] = quantity + cart.get(form.ingredient.name, 0)
                    request.session.modified = True

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        formset = self.form_class(initial=self.initial)
        return render(
            request,
            'orders/ingredient_list.html', {
                'title': self.title,
                'formset': formset})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST, initial=self.initial)
        status = BAD_REQUEST
        if formset.is_valid():
            self.__class__._update_session(formset, request)
            status = CREATED
        return render(
            request,
            'orders/ingredient_list.html', {
                'title': self.title,
                'formset': formset},
            status=status)

    @property
    def initial(self):
        return [dict(ingredient=i) for i in self.model.objects.all()]

    @property
    def form_class(self):
        return formset_factory(OrderItemForm, max_num=len(self.initial))

    @property
    def title(self):
        return self.__class__.__name__


class Grains(OrderIngredientView):
    model = models.Grain


class Hops(OrderIngredientView):
    model = models.Hop


@login_required
def checkout(request):
    # check that order has been reviewed!
    # Email user a summary

    def get_ingredient(name):
        return models.Grain.objects.get(name=name)

    def validate(data):
        for ingredient_name, quantity in data.items():
            try:
                quantity = int(quantity)
                if quantity < 0:
                    break
                ingredient = get_ingredient(ingredient_name)
            except ValueError:
                break
            except models.DoesNotExist:
                break
        else:
            return True
        return False

    if request.method == 'POST':
        cart = _get_cart_from_session(request)
        if validate(cart):
            order = models.UserOrder.objects.create(user=request.user)
            for name, quantity in cart.items():
                ingredient = get_ingredient(name)
                models.OrderItem.objects.create(
                    ingredient=ingredient,
                    quantity=int(quantity),
                    order=order)
            del request.session['cart']
            request.session.modified = True
            return HttpResponseRedirect(redirect_to=reverse('order_complete'))
        return HttpResponseBadRequest('Could not complete your order')
    else:
        return render(request, 'orders/review_cart.html')


def order_complete(request):
    return render(request, 'orders/order_complete.html')


@require_POST
@login_required
def cart_delete_item(request):
    cart = _get_cart_from_session(request)
    ingredient_name = request.POST.get('ingredient_name')
    if ingredient_name not in cart:
        return HttpResponseBadRequest()
    del cart[ingredient_name]
    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
