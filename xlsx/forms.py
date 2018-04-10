from django import forms

class xlsx(forms.Form):
    epid = forms.CharField(label='Your name', max_length=100)