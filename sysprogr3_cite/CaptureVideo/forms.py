# from
# https://qiita.com/narupo/items/e3dbdd5d030952d10661

LOCALE_CHOICES = [
    (0,'bf-0'),
    (1,'bf-1'),
    (2,'bf-2'),
    (3,'bf-3'),
    (4,'bf-4'),
    (5,'bf-5'),
    (6,'bf-6'),
    (7,'bf-7'),
    (8,'bf-8'),
    (9,'bf-9'),
    (10,'bf-10'),
    (11,'bf-11'),
    (12,'bf-12'),
    (0+13,'1f-0'),
    (1+13,'1f-1'),
    (2+13,'1f-2'),
    (3+13,'1f-3'),
    (4+13,'1f-4'),
    (5+13,'1f-5'),
    (6+13,'1f-6'),
    (7+13,'1f-7'),
    (8+13,'1f-8'),
    (9+13,'1f-9'),
    (10+13,'1f-10'),
    (11+13,'1f-11'),
    (12+13,'1f-12'),
    (0+26,'2f-0'),
    (1+26,'2f-1'),
    (2+26,'2f-2'),
    (3+26,'2f-3'),
    (4+26,'2f-4'),
    (5+26,'2f-5'),
    (6+26,'2f-6'),
    (7+26,'2f-7'),
    (8+26,'2f-8'),
    (9+26,'2f-9'),
    (10+26,'2f-10'),
    (11+26,'2f-11'),
    (12+26,'2f-12'),
    (0+39,'3f-0'),
    (1+39,'3f-1'),
    (2+39,'3f-2'),
    (3+39,'3f-3'),
    (4+39,'3f-4'),
    (5+39,'3f-5'),
    (6+39,'3f-6'),
    (7+39,'3f-7'),
    (8+39,'3f-8'),
    (9+39,'3f-9'),
    (10+39,'3f-10'),
    (11+39,'3f-11'),
    (12+39,'3f-12'),
]


from django import forms

class PhotoForm(forms.Form):
    image = forms.ImageField()

class PassForm(forms.Form):
    pass

class SerachForm(forms.Form):
    start = forms.ChoiceField(label='Start Point', choices=LOCALE_CHOICES, initial=0)
    end = forms.ChoiceField(label='End Point', choices=LOCALE_CHOICES, initial=0)
