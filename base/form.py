from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from base.models import Room
from base.models import User


class RoomForms(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['image','name', 'bio','username','email','password']
