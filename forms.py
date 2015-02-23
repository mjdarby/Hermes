from django import forms

class BoardForm(forms.Form):
    author = forms.CharField(max_length=30, label="Name (optional)", required=False)
    email = forms.CharField(max_length=30, label="Email (optional)", required=False)
    title = forms.CharField(max_length=30, label="Title (optional)", required=False)
    text = forms.CharField(max_length=1000, label="Comment", widget=forms.Textarea(attrs={'rows': 3}))
