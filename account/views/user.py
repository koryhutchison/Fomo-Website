from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from account import models as amod
from django import forms
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

    form = UserEditForm(request, user=user, initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'address': user.address,
        'city': user.city,
        'state': user.state,
        'zipcode': user.zipcode,
        'birth_date': user.birth_date,
        'gender': user.gender,
        'email': user.email,
        'username': user.username,

    })
    if form.is_valid():
        form.commit(user)
        return HttpResponseRedirect('/account/index/')


    context = {
        'user': user,
        'form' : form,
    }
    return dmp_render(request, 'user.html', context)


class UserEditForm(FormMixIn, forms.Form):
    form_id = 'edit_user_form'
    def init(self, user):
        self.fields['first_name'] = forms.CharField(label="First Name")
        self.fields['last_name'] = forms.CharField(label="Last Name")
        self.fields['address'] = forms.CharField(label="Address", required=False)
        self.fields['city'] = forms.CharField(label="City", required=False)
        self.fields['state'] = forms.CharField(label="State", required=False)
        self.fields['zipcode'] = forms.CharField(label="Zipcode", required=False)
        self.fields['birth_date'] = forms.DateField(label="Birth Date", required=False)
        self.fields['gender'] = forms.ChoiceField(label="Gender", required=True, choices=
            [
                ['Male', 'Male'],
                ['Female', 'Female'],
                ['Other', 'Other'],
            ]
        )
        self.fields['email'] = forms.EmailField(label="Email Address")
        self.fields['username'] = forms.CharField(label="User Name", max_length="100")

    def clean_username(self):
        cur_username = self.cleaned_data.get('username')
        user = amod.FomoUser.objects.filter(username=cur_username).exclude(id=self.request.urlparams[0])

        if len(user) >= 1:
            raise forms.ValidationError('Username already taken')
        return cur_username


    def commit(self, user):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.city = self.cleaned_data.get('city')
        user.state = self.cleaned_data.get('state')
        user.zipcode = self.cleaned_data.get('zipcode')
        user.birth_date = self.cleaned_data.get('birth_date')
        user.gender = self.cleaned_data.get('gender')
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('username')
        user.save()
        return 4


@view_function
def delete(request):
    try:
        user = amod.FomoUser.objects.get(id=request.urlparams[0])
    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/manager/users/')

    user.delete()
    return HttpResponseRedirect('/manager/users/')
