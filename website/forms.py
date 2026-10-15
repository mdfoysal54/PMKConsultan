from django import forms
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    website=forms.CharField(required=False,widget=forms.TextInput(attrs={'autocomplete':'off','tabindex':'-1'}))
    class Meta:
        model=Inquiry
        fields=['name','email','company','service','budget','details']
        widgets={'details':forms.Textarea(attrs={'rows':5,'placeholder':'Tell us about your goals, timeline and requirements'})}
    def clean_name(self):
        value=self.cleaned_data['name'].strip()
        if len(value)<2: raise forms.ValidationError('Please enter your name.')
        return value
