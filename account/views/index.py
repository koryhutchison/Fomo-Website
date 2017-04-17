from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('/account/login/')

    return dmp_render(request, 'index.html', {})
