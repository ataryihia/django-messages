from django import forms
from django.contrib.auth.models import User
from basic_app.models import MessagesInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput())


    class Meta():
        model = User
        fields = ('username','email','password',)

class MessageForm(forms.ModelForm):

    class Meta:
        model = MessagesInfo
        fields = ('reciver_msg','subject','message_body',)