from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from orders import models
from orders.forms import OrderItemForm
from django.template import RequestContext
from django.views.decorators.http import require_POST


def _get_cart_from_session(request):
    return request.session.setdefault('cart', {})


def main(request):
    return render_to_response('orders/main.html', context_instance=RequestContext(request))


def _update_session(formset, request):
    if formset.is_valid():
        for form, cleaned_data in zip(formset, formset.cleaned_data):
            quantity = cleaned_data.get("quantity", 0)
            cart = _get_cart_from_session(request)
            if quantity and quantity > 0:
                cart[form.ingredient.name] = quantity + cart.get(form.ingredient.name, 0)
                request.session.modified = True


@login_required
def grains(request):
    initial = [dict(ingredient=i) for i in models.Grain.objects.all()]
    OrderItemFormset = formset_factory(OrderItemForm, max_num=len(initial))
    formset = OrderItemFormset(initial=initial)

    if request.method == 'POST':
        formset = OrderItemFormset(request.POST, initial=initial)
        _update_session(formset, request)

    return render_to_response(
        'orders/ingredient_list.html', {
            'title': 'Grains',
            'formset': formset},
        context_instance=RequestContext(request))


@login_required
def hops(request):
    initial = [dict(ingredient=i) for i in models.Hop.objects.all()]
    OrderItemFormset = formset_factory(OrderItemForm, max_num=len(initial))
    formset = OrderItemFormset(initial=initial)

    if request.method == 'POST':
        formset = OrderItemFormset(request.POST, initial=initial)
        _update_session(formset, request)

    return render_to_response(
        'orders/ingredient_list.html', {
            'title': 'Hops',
            'formset': formset},
        context_instance=RequestContext(request))


@login_required
def cart(request):
    print(request.POST)
    return HttpResponse()


@require_POST
def cart_delete_item(request):
    cart = _get_cart_from_session(request)
    ingredient_name = request.POST.get('ingredient_name')
    if ingredient_name not in cart:
        return HttpResponseBadRequest()
    del cart[ingredient_name]
    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
