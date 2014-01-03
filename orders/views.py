from http.client import OK, CREATED, BAD_REQUEST
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response, render
from django.forms.formsets import formset_factory, BaseFormSet
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from orders import models
from orders.forms import CartItemForm
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_GET


def main(request):
    return render_to_response('orders/main.html', context_instance=RequestContext(request))


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
    def get(self, request, *args, **kwargs):
        formset = self.formset_class(initial=self.initial)
        return render(
            request,
            'orders/ingredient_list.html', {
                'title': self.title,
                'formset': formset})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        formset = self.formset_class(request.POST, initial=self.initial)
        if formset.is_valid():
            self.__class__._update_session(formset, request)
            return HttpResponseRedirect('')
        return render(
            request,
            'orders/ingredient_list.html', {
                'title': self.title,
                'formset': formset},
            status=BAD_REQUEST)

    @property
    def initial(self):
        return [dict(ingredient_name=i.name, quantity=0, unit_cost=i.unit_cost, unit_size=i.unit_size) for i in self.model.objects.all()]

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


@require_POST
@login_required
def review_order(request):
    return render(request, 'orders/review_cart.html')


@require_POST
@login_required
def checkout(request):
    # ToDo: check that order has been reviewed!
    # ToDo: Email user a summary

    def validate(data):
        for ingredient_name, quantity in data.items():
            try:
                quantity = int(quantity)
                if quantity < 0:
                    break
                ingredient = _get_ingredient(ingredient_name)
            except ValueError:
                break
            except models.Grain.DoesNotExist:
                break
            except models.Hop.DoesNotExist:
                break
        else:
            return True
        return False

    cart = _get_cart_from_session(request)
    if validate(cart):
        order = models.UserOrder.objects.create(user=request.user)
        for name, quantity in cart.items():
            ingredient = _get_ingredient(name)
            models.OrderItem.objects.create(
                ingredient=ingredient,
                quantity=int(quantity),
                order=order)
        del request.session['cart']
        request.session.modified = True
        return HttpResponseRedirect(redirect_to=reverse('order_complete'))
    # ToDo: email admin on failure
    return HttpResponseBadRequest('Could not complete your order')


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


def _get_cart_from_session(request):
    return request.session.setdefault('cart', {})


def _get_ingredient(name):
    return models.Grain.objects.get(name=name)
