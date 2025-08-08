from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    gender=[
        ('male','male'),
        ('female','female'),
        ('others','others')
    ]
    email=models.EmailField(unique=True,null=True, blank=True)
    name=models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    gender= models.CharField(max_length=10, choices=gender,default='male')
    age=models.CharField(max_length=10, null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    is_enduser=models.BooleanField(default=False)
    profession=models.CharField(max_length=100,null=True,blank=False)
    profile=models.FileField(null=True, blank=True, upload_to='profiles/', default="avatar.png")
    date_joined=models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS= ['name']

    class Meta:
        
        ordering = ['-date_joined']

def __str__(self):
    return self.email


class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    occupation = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Borrower'
        verbose_name_plural = 'Borrowers'
        ordering = ['-created_at']

    def __str__(self):
        return self.user.get_full_name()

class LoanApplication(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.TextField()
    status_choices = [
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Loan Application'
        verbose_name_plural = 'Loan Applications'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.borrower} - KES {self.amount_requested}"
    
class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term_months = models.PositiveIntegerField()
    interest_rate = models.FloatField()
    purpose = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    national_id = models.CharField(max_length=20, unique=True,null= True)
    phone = models.CharField(max_length=15,null=True)
    address = models.TextField(null=True)
    occupation = models.CharField(max_length=100, blank=True)

    application_date = models.DateField(auto_now_add=True)
    approval_date = models.DateField(null=True, blank=True)

    class Meta:
        
        ordering = ['-application_date']

    def __str__(self):
        return f"{self.borrower.username} - {self.amount} ({self.status})"


class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_date = models.DateField()
    transaction_reference = models.CharField(max_length=100, unique=True)
    method = models.CharField(max_length=50, default='cash', choices=[('cash', 'Cash'), ('mpesa', 'Mpesa'), ('bank', 'Bank Transfer')])
    status = models.CharField(max_length=20, default='pending', choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_date = models.DateField(auto_now_add=True)

    class Meta:
        
        ordering = ['-payment_date']

    def __str__(self):
        return f"Repayment of {self.amount_paid} on {self.payment_date}"

class Guarantor(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='guaranteed_loans')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Guarantor: {self.name} for Loan #{self.loan.id}"

class DefaultRecord(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE)
    reason = models.TextField()
    marked_date = models.DateField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering=['-marked_date']

    def __str__(self):
        return f"Defaulted: {self.loan}"

class LoanOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Officer"

class LoanSchedule(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE)
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Due: {self.due_date} - KES {self.amount_due}"

class LoanDocument(models.Model):
    borrower = models.ForeignKey('Borrower', on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=100)  # e.g. ID, Payslip, Bank Statement
    file = models.FileField(upload_to='loan_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_type} by {self.borrower}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username} - {'Read' if self.is_read else 'Unread'}"

class CreditScore(models.Model):
    borrower = models.OneToOneField('Borrower', on_delete=models.CASCADE)
    score = models.IntegerField(default=500)  # 300 - 850 range typical
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.borrower} - Score: {self.score}"

class LoanPurposeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class TransactionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    additional_info = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} - {self.action} @ {self.timestamp}"

class SupportTicket(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed')
    ], default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.status}"

class LoanCondition(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE)
    terms_text = models.TextField()
    agreed = models.BooleanField(default=False)
    agreed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Conditions for Loan #{self.loan.id}"


class ReviewCart(models.Model):
    officer = models.ForeignKey(User, on_delete=models.CASCADE)  # Loan officer/admin
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('officer', 'application')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.officer.username} reviewing {self.application}"
    
class LoanCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'loan_application')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.user.username} - {self.loan_application.amount_requested} in cart"
    
class disbursement(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    disbursed_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=[('bank', 'Bank Transfer'), ('mpesa', 'Mpesa'), ('cash', 'Cash')])

    def __str__(self):
        return f"Disbursement of {self.amount} for Loan #{self.loan.id} on {self.disbursed_at}"
    

class loanapproval(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approvals')
    approval_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Loan #{self.loan.id} approved by {self.approved_by.username} on {self.approval_date}"
