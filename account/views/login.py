from django.conf import settings
from django import forms
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

@view_function
def process_request(request):

        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                form.commit(request)
                return HttpResponseRedirect('/account/index')

        else:
            # prepare an empty form
            form = LoginForm()

        return dmp_render(request, 'login.html', {'form' : form,})



class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=100,
        widget=forms.TextInput(attrs={ 'class': 'form-control'})
    )
    password = forms.CharField(label='Password', max_length=100,
        widget=forms.PasswordInput(attrs={ 'class': 'form-control'})
    )

    def clean(self):
        self.user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid username or password')
        return self.cleaned_data

    def commit(self, request):
        login(request, self.user)
        return 4


@view_function
def modal(request):

        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                form.commit(request)
                return HttpResponse('''
                <script>
                    window.location.href = '/homepage/index/';
                </script>
                ''')

        else:
            # prepare an empty form
            form = LoginForm()

        return dmp_render(request, 'login.modal.html', {'form' : form,})
