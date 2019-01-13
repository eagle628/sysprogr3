# from
# https://qiita.com/narupo/items/e3dbdd5d030952d10661

LOCALE_CHOICES = [
    (0,'label0'),
    (1,'label1'),
    (2,'label2'),
    (3,'label3'),
    (4,'label4'),
    (5,'label5'),
    (6,'label6'),
    (7,'label7'),
    (8,'label8'),
    (9,'label9'),
    (10,'label10'),
    (11,'label11'),
]


from django import forms

class PhotoForm(forms.Form):
    image = forms.ImageField()

class PassForm(forms.Form):
    pass

class SerachForm(forms.Form):
    start = forms.ChoiceField(label='Start Point', choices=LOCALE_CHOICES, initial=0)
    end = forms.ChoiceField(label='End Point', choices=LOCALE_CHOICES, initial=0)
