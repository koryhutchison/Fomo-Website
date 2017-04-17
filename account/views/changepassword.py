from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from account import models as amod
from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from .. import dmp_render, dmp_render_to_string
from formlib.form import FormMixIn

@view_function
@login_required
@permission_required('account.user_edit_user')
def process_request(request):

    try:
        user = amod.FomoUser.objects.get(id=request.urlparams[0])
    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/account/index/')

    form = PasswordChangeForm(request, user=user)
    if form.is_valid():
        form.commit(request, user)
        return HttpResponseRedirect('/account/index/')


    context = {
        'form' : form,
        'user' : user,
    }
    return dmp_render(request, 'changepassword.html', context)

class PasswordChangeForm(FormMixIn, forms.Form):
    def init(self, user):
        self.fields['old_password'] = forms.CharField(label="Old Password", widget=forms.PasswordInput())
        self.fields['new_password'] = forms.CharField(label="New Password", widget=forms.PasswordInput())
        self.fields['verify_password'] = forms.CharField(label="Verify Password", widget=forms.PasswordInput())

    def clean(self):
        user = amod.FomoUser.objects.get(id=self.request.urlparams[0])
        check = check_password(self.cleaned_data.get('old_password'), user.password)
        if check is False:
            raise forms.ValidationError('Old Password is incorrect')
        new_password = self.cleaned_data.get('new_password')
        verify_password = self.cleaned_data.get('verify_password')
        if new_password != verify_password:
            raise forms.ValidationError('New passwords do not match')
        return self.cleaned_data

    def commit(self, request, user):
        # put the fields to commit here.
        user.set_password(self.cleaned_data.get('new_password'))
        user.save()
        login(request, user)
