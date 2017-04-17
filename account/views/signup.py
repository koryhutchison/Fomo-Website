from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from account import models as amod
from django import forms
from django.contrib.auth import authenticate, login
from .. import dmp_render, dmp_render_to_string
from formlib.form import FormMixIn

@view_function
def process_request(request):

    form = UserCreateForm(request)
    if form.is_valid():
        form.commit(request)
        return HttpResponseRedirect('/account/index/')


    context = {
        'form' : form,
    }
    return dmp_render(request, 'signup.html', context)


class UserCreateForm(FormMixIn, forms.Form):
    form_id = 'signup_form'
    def init(self):
        self.fields['first_name'] = forms.CharField(label="First Name")
        self.fields['last_name'] = forms.CharField(label="Last Name")
        self.fields['address'] = forms.CharField(label="Address", required=False)
        self.fields['city'] = forms.CharField(label="City", required=False)
        self.fields['state'] = forms.CharField(label="State", required=False)
        self.fields['zipcode'] = forms.CharField(label="Zipcode", required=False)
        self.fields['birth_date'] = forms.DateTimeField(label="Birth Date", required=False)
        self.fields['gender'] = forms.ChoiceField(label="Gender", required=True, choices=
            [
                ['Male', 'Male'],
                ['Female', 'Female'],
                ['Other', 'Other'],
            ]
        )
        self.fields['email'] = forms.EmailField(label="Email Address", required=True)
        self.fields['username'] = forms.CharField(label="User Name", max_length="100")
        self.fields['password'] = forms.CharField(label="Password", widget=forms.PasswordInput())
        self.fields['verify_password'] = forms.CharField(label="Verify Password", widget=forms.PasswordInput())

    def clean(self):
        cur_username = self.cleaned_data.get('username')
        user = amod.FomoUser.objects.filter(username=cur_username)

        if len(user) >= 1:
            raise forms.ValidationError('Username already taken')
        password = self.cleaned_data.get('password')
        verify_password = self.cleaned_data.get('verify_password')
        if password != verify_password:
            raise forms.ValidationError('New passwords do not match')
        return self.cleaned_data

    def commit(self, request):
        # put the fields to commit here.
        user = amod.FomoUser()
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
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        login(request, user)

        return 4
