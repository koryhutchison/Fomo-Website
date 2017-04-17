from django.conf import settings
from django_mako_plus import view_function
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from datetime import datetime
from account import models as amod
from .. import dmp_render, dmp_render_to_string
import json

@view_function
def process_request(request):

    # try:
    user = amod.FomoUser.objects.get(id=request.urlparams[0])
    # except amod.FomoUser.DoesNotExist:
    #     return HttpResponseNotFound('Bad User id')

    ret = {
        'firstname': user.first_name,
        'lastname': user.last_name,
        'email': user.email,
        'groups': [],
    }

    for g in user.groups.all():
        ret['groups'].append(g.name)


    return JsonResponse(ret)
