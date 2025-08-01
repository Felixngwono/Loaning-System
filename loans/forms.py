from django import forms
from .models import  Loan, Repayment, User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):   
    class Meta:
        model = User
        fields = ['name', 'username', 'email','gender','phone_number','age','address','profession','profile','is_enduser']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise forms.ValidationError("This email is already taken.")
        return email
        


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'

class RepaymentForm(forms.ModelForm):
    class Meta:
        model = Repayment
        fields = ['amount', 'method']


