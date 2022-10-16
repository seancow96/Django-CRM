from django import forms
from .models import Musician
from .models import Band, Category
from django.contrib.auth.forms import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()

class MusicianModelForm(forms.ModelForm):
 class Meta:
    model = Musician
    fields = (
        'first_name',
        'last_name',
        'age',
        'band'
    )



class MusicianForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

class AssignBandForm(forms.Form):
    band = forms.ModelChoiceField(queryset=Band.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        bands = Band.objects.filter(organisation=request.user.userprofile)
        super(AssignBandForm, self).__init__(*args, **kwargs)
        self.fields["band"].queryset = bands

class   MusicianCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Musician
        fields = (
            'category',
        )


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )

