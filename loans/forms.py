from django import forms
from .models import  DefaultRecord, Loan, LoanOfficer, Repayment, ReviewCart, User, disbursement
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
        fields = ['loan', 'amount', 'amount_paid', 'transaction_reference', 'method', 'status']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered.")
        return email
    
class ReviewCartForm(forms.ModelForm):
    
    class Meta:
        model = ReviewCart
        fields = '__all__'

class LoanOfficerForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        label="Officer Account",
        help_text="Select a staff user to assign as a loan officer"
    )

    class Meta:
        model = LoanOfficer
        fields = ['user', 'staff_id']

class DefaultRecordForm(forms.ModelForm):
    class Meta:
        model = DefaultRecord
        fields = ['loan', 'reason']

class disbursementForm(forms.ModelForm):
    
    class Meta:
        model = disbursement
        fields = '__all__'
