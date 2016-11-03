from django import forms
from .models import (
    Account, 
    Section, 
    Work, 
    Education, 
    SpecialSection,
    )
from django.contrib.auth import authenticate


class SignUpForm(forms.ModelForm):
    """
    """
    email = forms.EmailField()
    password = forms.CharField()
    confirm_password = forms.CharField()

    class Meta:
        model = Account
        fields = ("email", "password")

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        password = self.cleaned_data.get("password")

        if confirm_password != password:
            raise forms.ValidationError("Password did'nt match!")

        return confirm_password

    def save(self, commit=True):
        """saving password with hashed
        """
        instance = super(SignUpForm, self).save(commit=False)

        if commit:
            instance.set_password(self.cleaned_data.get('password'))
            instance.username = instance.email_as_username()
            instance.save()
            
        return instance



class LoginForm(forms.Form):
    """ Form for login view contains of two fields 
    """
    email = forms.EmailField()
    password = forms.CharField()

    def clean(self):
        """ To validate the email address and password
        """
        user_cache = None
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Invalid Email or Password')
        else:
            self.user_cache = user


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = (
            'email',
            'full_name', 
            )

    def save(self, commit=True):
        instance = super(AccountForm, self).save(commit=False)

        if commit:
            instance.username = instance.email_as_username()
            instance.save()
            
        return instance


class SectionForm(forms.ModelForm):

    name = forms.CharField()

    class Meta:
        model = Section
        fields = ('name',)


class SectionForm_(forms.ModelForm):

    class Meta:
        model = Section
        fields = '__all__'


class EducationForm(forms.ModelForm):

    class Meta:
        model = Education
        fields = '__all__'


class UploadForm(forms.ModelForm):

    class Meta:
        model = Section
        fields  = ('photo',)


class WorkForm(forms.ModelForm):

    class Meta:
        model = Work
        fields = '__all__'


class SpecialSectionForm(forms.ModelForm):

    class Meta:
        model = SpecialSection
        fields = '__all__'


class SpecialSectionForm_(forms.ModelForm):

    class Meta:
        model = SpecialSection
        fields = ('name',)

