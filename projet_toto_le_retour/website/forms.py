from django import forms

from website.models import Product


class PalindromForm(forms.Form):
    word = forms.CharField(max_length=300, label="Mot à vérifier", required=True)
    boost = forms.BooleanField(initial=False, required=False)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["boost"]:
            cleaned_data["word"] = cleaned_data["word"].upper()

        return cleaned_data


class ProductForm(forms.Form):
    name = forms.CharField(max_length=300, required=True)
    price = forms.FloatField(min_value=0)


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "price"]
