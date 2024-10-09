from django import forms
from ecommapp.models import product_review

class productreviewform(forms.ModelForm):
    Review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Add a Review'}))
    
    class Meta:
        model = product_review
        fields = ['review','rating']