from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response
from flatblocks.models import FlatBlock


def index(request):
    return render_to_response(
        'index.html',
        {},
        context_instance=RequestContext(request))


def howto(request, name):
    try:
        flatblock = FlatBlock.objects.get(slug=name)
        return render(request, 'main/howto.html', {'howto_name': name})
    except FlatBlock.DoesNotExist:
        return HttpResponseNotFound('Could not find the howto: %s' % name)
    return HttpResponseServerError('Error rendering the howto: %s' % name)


def committee(request):
    users = get_user_model().objects.filter(groups__name="Committee")
    return render(request, 'main/committee.html', {'users': users})
