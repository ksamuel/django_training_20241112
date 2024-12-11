from django import forms


class PalindromForm(forms.Form):
    word = forms.CharField(max_length=300, label="Mot à vérifier", required=True)
    boost = forms.BooleanField(initial=False, required=False)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["boost"]:
            cleaned_data["word"] = cleaned_data["word"].upper()

        return cleaned_data
