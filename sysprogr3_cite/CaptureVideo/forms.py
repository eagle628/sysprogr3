# from
# https://qiita.com/narupo/items/e3dbdd5d030952d10661

from django import forms

class PhotoForm(forms.Form):
    image = forms.ImageField()

class PassForm(forms.Form):
    pass
