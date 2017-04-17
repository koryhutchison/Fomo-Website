from django.conf import settings
from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string

@view_function
# @login_required
# @permission_required('account.contactus', raise_exception=True)
def process_request(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            # act on the form here
            return HttpResponseRedirect('/')

    else:
        # prepare an empty form
        form = ContactForm()

    return dmp_render(request, 'contact.html', {'form' : form,})

class ContactForm(forms.Form):
    name = forms.CharField(label='Full name', max_length=100,
        widget=forms.TextInput(attrs={ 'class': 'form-control'})
    )
    email = forms.EmailField(label='Email', max_length=100,
        widget=forms.TextInput(attrs={ 'class': 'form-control'})
    )
    message = forms.CharField(label='Message', max_length=1000,
        widget=forms.Textarea(attrs={ 'class': 'form-control'})
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        parts = name.strip().split()
        if len(parts) <= 1:
            raise forms.ValidationError('Please enter both first and last name')

        return name
