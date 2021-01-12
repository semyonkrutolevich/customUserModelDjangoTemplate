import email
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q, fields

User = get_user_model()

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user


class UserLoginForm(forms.ModelForm):
    
    query = forms.CharField(label="Имя пользователя / Почта")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ["query", "password"]

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
            Q(username__iexact=query) |
            Q(email__iexact=query)
        ).distinct()

        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Данные введены не верно, либо данного пользователя не существует")
        
        user_object = user_qs_final.first()
        if not user_object.check_password(password):
            raise forms.ValidationError("Неверные логин или пароль")
        
        self.cleaned_data['user_object'] = user_object
        return super(UserLoginForm, self).clean(*args, **kwargs)