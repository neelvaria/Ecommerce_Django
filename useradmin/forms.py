from ecommapp.models import *
from django import forms

class AddProduct(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Product Title', "class":"form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Product Description', "class":"form-control"}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Product Price', "class":"form-control"}))
    old_price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Product Old Price', "class":"form-control"}))
    type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Product Type Eg: Organic','class': 'form-control'}))
    stock_count = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'How many are in Stock ?', "class":"form-control"}))
    expiry = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Product Expiry', "class":"form-control"}))
    mfd = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Product Manufacture Date', "class":"form-control"}))
    tags = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Product Tags', "class":"form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'placeholder': 'Product Image', "class":"form-control"}))
    
    class Meta:
        model = Product
        fields = [
            'title','image','description','price','old_price','specification','type',
            'stock','expiry','mfg','tags','in_stock','digital','category'
        ]
    
    