from datetime import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from loans.forms import  ContactForm, LoanApplicationForm, MyUserCreationForm, RepaymentForm
from .models import Borrower, DefaultRecord, Guarantor, LoanApplication, LoanCondition, LoanDocument, LoanOfficer, LoanPurposeCategory, LoanSchedule, Repayment, ReviewCart, SupportTicket, TransactionLog, User, disbursement, loanapproval
from django.http import HttpResponse
from .models import Loan
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db.models import Sum


# Create your views here.
def signup(request):
    show_modal = False  
    
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.info(request, 'Registration successful, login to continue to main page')

            show_modal = True
            return redirect('login')
        
        else:
            messages.warning(request, 'An error occurred during registration')
            show_modal = True

    return render(request, 'signup.html', {'form': form, 'show_modal': show_modal})

def loginpage(request):
    show_modal = False 

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, 'User does not exist')
            show_modal = True
            return render(request, 'sign-in.html', {'show_modal': show_modal})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            show_modal = True
            return render(request, 'sign-in.html', {'show_modal': show_modal})
        else:
            messages.warning(request, 'Wrong username or password')
            show_modal = True

    return render(request, 'sign-in.html', {'show_modal': show_modal})

def logoutuser(request):
    if not request.user.is_authenticated:
        return HttpResponse("You are not logged in.", status=401)
    logout(request)
    messages.info(request, "It's sad to see you leave. Welcome again!")
    return redirect('login')

@login_required(login_url='login')
def index(request):
    users=User.objects.all().count
    users_since_lastmonth = User.objects.filter(date_joined__gte=timezone.now().date() - timezone.timedelta(days=30)).count()
    borrowers=Loan.objects.filter(borrower=request.user).count()
    todays_loans = Loan.objects.filter(application_date=timezone.now().date()).count()
    yesterdays_loans = Loan.objects.filter(application_date=timezone.now().date() - timezone.timedelta(days=1)).count()
    yesterday_loan_count = Loan.objects.filter(application_date=timezone.now().date() - timezone.timedelta(days=1)).count()
    new_applications = Loan.objects.filter(application_date=timezone.now().date()).count()
    last_week_loan_count = Loan.objects.filter(application_date__gte=timezone.now().date() - timezone.timedelta(days=7)).count()
    disbursed_loans = disbursement.objects.filter(loan__borrower=request.user).count()
    last_month_loan_count = Loan.objects.filter(application_date__month=timezone.now().month).count()
    active_loans = Loan.objects.filter(status='active').count()
    active_since_lastweek = Loan.objects.filter(application_date__gte=timezone.now().date() - timezone.timedelta(days=7)).count()
    pending_approvals = Loan.objects.filter(status='pending').count()
    pending_approval_since_lastweek = Loan.objects.filter(application_date__gte=timezone.now().date() - timezone.timedelta(days=7), status='pending').count()
    total_repaid_loans = Repayment.objects.filter(loan__borrower=request.user).aggregate(Sum('amount'))['amount__sum'] or 0.0
    total_repaid_loans_since_lastweek = Repayment.objects.filter(payment_date__gte=timezone.now().date() - timezone.timedelta(days=7), loan__borrower=request.user).aggregate(Sum('amount'))['amount__sum'] or 0.0
    defaulted_loans = DefaultRecord.objects.filter(loan__borrower=request.user).count()
    defaulters_since_lastmonth = DefaultRecord.objects.filter(marked_date__gte=timezone.now().date() - timezone.timedelta(days=30), loan__borrower=request.user).count()
    context={'users':users,
             'users_since_lastmonth': users_since_lastmonth,
             'borrowers':borrowers,
             'todays_loans':todays_loans,
             'yesterdays_loans':yesterdays_loans,
             'yesterday_loan_count':yesterday_loan_count,
             'new_applications':new_applications,
             'last_week_loan_count':last_week_loan_count,
             'disbursed_loans':disbursed_loans,
             'last_month_loan_count':last_month_loan_count,
             'active_loans':active_loans,
             'active_since_lastweek':active_since_lastweek,
             'pending_approvals':pending_approvals,
             'pending_approval_since_lastweek':pending_approval_since_lastweek,
             'total_repaid_loans': total_repaid_loans,
             'total_repaid_loans_since_lastweek': total_repaid_loans_since_lastweek,
             'defaulted_loans': defaulted_loans,
             'defaulters_since_lastmonth': defaulters_since_lastmonth,
             }
    return render(request, 'index.html',context)



def welcoming(request):
    return render(request, 'welcoming.html')

@login_required(login_url='login')
def profile(request,pk):
    userprofile=get_object_or_404(User, id=pk)
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile', pk=request.user.id)
        else:
            messages.error(request, 'Error updating profile')
    else:
        form = MyUserCreationForm(instance=userprofile)
    context = {
        'form': form,
        'userprofile': userprofile
    }
    return render(request, 'profile.html', context)
    
def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile', pk=user.id)
        else:
            messages.error(request, 'Error updating profile')
    else:
        form = MyUserCreationForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})

@login_required(login_url='login')  
def chart(request):
   
    return render(request, 'charts.html', )


@login_required(login_url='login')
def apply_for_loan(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.borrower = request.user
            loan.save()
            return redirect('loan_success')  # Create a template for this
    else:
        form = LoanApplicationForm()
    return render(request, 'loans/apply.html', {'form': form})

def loan_success(request):
    return render(request, 'loans/success.html')


@login_required(login_url='login')
def borrower_loans(request):
    borrower=Loan.objects.all()
    loans = Loan.objects.filter(borrower=request.user)
    return render(request, 'loans/borrower_loans.html', {'loans': loans,'borrower':borrower})

@login_required(login_url='login')
def borrower_details(request, pk):
    borrower_det = Loan.objects.filter(borrower=request.user).first()

    context = {
        'borrower_det': borrower_det,
        'borrower': request.user
    }
    return render(request, 'loans/borrower_details.html', context)

def base(request):
    
    return render(request, 'base.html')


@login_required(login_url='login')
def loan_table_view(request):
    if request.user.is_staff or request.user.is_superuser:
        # Admins see all loan applications
        loan_table = Loan.objects.select_related('borrower').order_by('-approval_date')
    else:
        # Regular users see only their own
        loan_table = Loan.objects.filter(borrower=request.user).order_by('-approval_date')

    return render(request, 'loans/table.html', {'loan_table': loan_table})

@login_required (login_url='login')
def loan_applications(request):
    borrower = get_object_or_404(Borrower, user=request.user)
    applications = LoanApplication.objects.filter(borrower=borrower)
    
    return render(request, 'loan/list.html', {'applications': applications})

@login_required(login_url='login')
def create_loan_application(request):
    if request.method == 'POST':
        borrower = get_object_or_404(Borrower, user=request.user)
        amount = request.POST.get('amount')
        purpose = request.POST.get('purpose')
        LoanApplication.objects.create(
            borrower=borrower,
            amount_requested=amount,
            purpose=purpose,
        )
        messages.success(request, "Application submitted.")
        return redirect('loan_applications')
    return render(request, 'loan/create.html')


@login_required(login_url='login')
def loan_list(request):
    loans = Loan.objects.filter(borrower=request.user)
    return render(request, 'loan/list.html', {'loans': loans})

@login_required(login_url='login')
def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, borrower=request.user)
    return render(request, 'loan/detail.html', {'loan': loan})


@login_required(login_url='login')
def repayment(request):
    loans = Loan.objects.filter(borrower=request.user)
    repayments = Repayment.objects.filter(loan__in=loans)
    return render(request, 'repayment/list.html', {'repayments': repayments})

@login_required(login_url='login')
def guarantors(request):
    borrower = get_object_or_404(Borrower, user=request.user)
    records = Guarantor.objects.filter(borrower=borrower)
    return render(request, 'guarantor/list.html', {'guarantors': records})

@login_required(login_url='login')
def defaulted_loans(request):
    user_loans = Loan.objects.filter(borrower=request.user)
    defaults = DefaultRecord.objects.filter(loan__in=user_loans)
    return render(request, 'defaults/list.html', {'defaults': defaults})

@login_required(login_url='login')
def my_officer(request):
    try:
        officer = LoanOfficer.objects.get(user=request.user)
    except LoanOfficer.DoesNotExist:
        officer = None
    return render(request, 'officer/profile.html', {'officer': officer})

@login_required(login_url='login')
def loan_schedule(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, borrower=request.user)
    schedule = LoanSchedule.objects.filter(loan=loan)
    return render(request, 'loan/schedule.html', {'schedule': schedule, 'loan': loan})

@login_required (login_url='login')
def my_documents(request):
    borrower = get_object_or_404(Borrower, user=request.user)
    documents = LoanDocument.objects.filter(borrower=borrower)
    return render(request, 'document/list.html', {'documents': documents})


@login_required(login_url='login')
def loan_purpose_categories(request):
    categories = LoanPurposeCategory.objects.all()
    return render(request, 'category/list.html', {'categories': categories})

@login_required(login_url='login')
def support_tickets(request):
    borrower = get_object_or_404(Borrower, user=request.user)
    tickets = SupportTicket.objects.filter(borrower=borrower)
    return render(request, 'support/list.html', {'tickets': tickets})

@login_required(login_url='login')
def create_ticket(request):
    if request.method == "POST":
        borrower = get_object_or_404(Borrower, user=request.user)
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        SupportTicket.objects.create(borrower=borrower, subject=subject, message=message)
        messages.success(request, "Support ticket submitted.")
        return redirect('support_tickets')
    return render(request, 'support/create.html')

@login_required(login_url='login')
def support_tickets(request):
    borrower = get_object_or_404(Borrower, user=request.user)
    tickets = SupportTicket.objects.filter(borrower=borrower)
    return render(request, 'support/list.html', {'tickets': tickets})

@login_required(login_url='login')
def create_ticket(request):
    if request.method == "POST":
        borrower = get_object_or_404(Borrower, user=request.user)
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        SupportTicket.objects.create(borrower=borrower, subject=subject, message=message)
        messages.success(request, "Support ticket submitted.")
        return redirect('support_tickets')
    return render(request, 'support/create.html')

@login_required(login_url='login')
def transaction_logs(request):
    logs = TransactionLog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'transaction/list.html', {'logs': logs})

@login_required(login_url='login')
def loan_conditions(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, borrower=request.user)
    try:
        condition = LoanCondition.objects.get(loan=loan)
    except LoanCondition.DoesNotExist:
        condition = None
    return render(request, 'loan/conditions.html', {'loan': loan, 'condition': condition})

@login_required(login_url='login')
def loan_cart(request):
    cart_items = Loan.objects.filter(status='PENDING').select_related('borrower')
    return render(request, 'admin/loan_cart.html', {'cart_items': cart_items})


@login_required(login_url='login')
def qualify_applicant(request, pk, status):
    app = get_object_or_404(LoanApplication, pk=pk)
    if status in ['QUALIFIED', 'UNQUALIFIED']:
        app.qualification_status = status
        app.save()
    return redirect('loan_cart')


@staff_member_required (login_url='login')
def add_to_cart(request, application_id):
    application = get_object_or_404(LoanApplication, id=application_id)
    ReviewCart.objects.get_or_create(officer=request.user, application=application)
    return redirect('view_cart')
    

@staff_member_required (login_url='login')
def view_cart(request):
    cart_items = ReviewCart.objects.filter(officer=request.user)
    return render(request, 'admin_cart/cart.html', {'cart_items': cart_items})

@staff_member_required (login_url='login')
def decide_loan(request, application_id, decision):
    application = get_object_or_404(LoanApplication, id=application_id)
    if decision.upper() in ['APPROVED', 'REJECTED']:
        application.status = decision.upper()
        application.reviewed_at = timezone.now()
        application.save()
        ReviewCart.objects.filter(application=application).delete()

    return redirect('view_cart')
    

@login_required(login_url='login')
def ContactPage(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Normally you'd handle form logic here (save or send email)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Use your URL name
    return render(request, 'contact.html', {'form': form})

@login_required(login_url='login')
def disbursement_list(request):
    if request.user.is_superuser:
        disbursements = disbursement.objects.select_related('loan', 'loan__borrower')
    else:
        loans = Loan.objects.filter(borrower=request.user)
        disbursements = disbursement.objects.filter(loan__in=loans).select_related('loan')
    
    return render(request, 'disbursement/list.html', {'disbursements': disbursements})



@login_required(login_url='login')
def loan_approval_list(request):
    if not request.user.is_superuser:
        return render(request, 'loanapproval/403.html') 

    approvals = loanapproval.objects.select_related('loan', 'approved_by').order_by('-approval_date')
    return render(request, 'loanapproval/list.html', {'approvals': approvals})
