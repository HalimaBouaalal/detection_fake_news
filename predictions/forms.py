from django import forms

class TextInputForm(forms.Form):
    text = forms.CharField(label='Texte à analyser', max_length=500)
