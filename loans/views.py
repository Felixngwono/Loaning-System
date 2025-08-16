from datetime import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from loans.forms import  ContactForm, DefaultRecordForm, LoanApplicationForm,  MyUserCreationForm, RepaymentForm, disbursementForm
from .models import Borrower, DefaultRecord, LoanApplication, LoanCondition, LoanDocument, LoanPurposeCategory, LoanSchedule, Repayment, ReviewCart,  TransactionLog, User, disbursement, loanapproval
from django.http import HttpResponse
from .models import Loan
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone


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
    
    if request.user.is_superuser:
        borrowerss = Loan.objects.all()
    else:
        borrowerss = Loan.objects.filter(borrower=request.user)

    #for pie chart
    

    borrowers_chart=  Loan.objects.all().count()
    defaulters_chart=DefaultRecord.objects.all().count()
    users_chart = User.objects.all().count()
    repayment_chart=Repayment.objects.all().count()
    disbursed_chart=disbursement.objects.all().count()
    defaulter_users = User.objects.filter(loan__defaultrecord__isnull=False).distinct().count()


    pie_labels=['borrowers_chart','defaulters_chart','users_chart','repayment_chart','disbursed_chart','defaulter_users']
    pie_data=[borrowers_chart,defaulters_chart,users_chart,repayment_chart,disbursed_chart,defaulter_users]

#for mixed polar
    polar_borrower=Loan.objects.all().count()
    polar_defaulters=DefaultRecord.objects.all().count()
    polar_users=User.objects.all().count()
    polar_repayment=Repayment.objects.all().count()
    polar_defaulter_users=User.objects.filter(loan__defaultrecord__isnull=False).distinct().count()

    polar_label=['polar_borrower','polar_defaulters','polar_users','polar_repayment','polar_defaulter_users']
    polar_data=[polar_borrower,polar_defaulters,polar_users,polar_repayment,polar_defaulter_users]
    
   
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
             'borrowerss': borrowerss,
             'pie_labels':pie_labels,
             'pie_data':pie_data,
             'polar_label':polar_label,
             'polar_data':polar_data
             
             

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
    if not hasattr(request.user, 'is_enduser') or not request.user.is_enduser:
        # Redirect or show permission denied page
        messages.error(request, "You do not have permission to apply for a loan.")
        return redirect('index')  # Or render a "403.html" page
    
    show_modal = False
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.borrower = request.user
            loan.save()
            messages.success(request, 'Loan Application successful')
            show_modal = True
    else:
        form = LoanApplicationForm()

    return render(request, 'loans/apply.html', {'form': form, 'show_modal': show_modal})


def loan_success(request):
    return render(request, 'loans/success.html')


@login_required(login_url='login')
def borrower_loans(request):
    if request.user.is_superuser:
        borrower = Loan.objects.all()
    else:
        # Regular users see only their own loans
        borrower = Loan.objects.filter(borrower=request.user)

    return render(request, 'loans/borrower_loans.html', {'borrower':borrower})

@login_required(login_url='login')
def borrower_details(request, pk):
    borrower_det=get_object_or_404(Loan,id=pk)
    form=LoanApplicationForm(instance=borrower_det)
    if request.method=='POST':
        form=LoanApplicationForm(request.POST,request.FILES,instance=borrower_det)
        if form.is_valid():
            form.save()
            return redirect('borrower_loans')
    context={
        'borrower_det':borrower_det
    }
    return render(request, 'loans/borrower_details.html', context)

def base(request):
    
    return render(request, 'base.html')



@login_required(login_url='login')
def repayment(request):
    if request.user.is_superuser:
        repayments = Repayment.objects.select_related('loan', 'loan__borrower')
    else:
        # Regular user sees only their repayments
        repayments = Repayment.objects.filter(loan__borrower=request.user).select_related('loan')

    return render(request, 'repayment/list.html', {'repayments': repayments})
    
@login_required(login_url='login')
def add_payment(request):
    # Check if user has any loan
    user_loans = Loan.objects.filter(borrower=request.user)

    if not user_loans.exists():
        messages.error(request, "You have not borrowed any loan, so you cannot make a repayment.")
        return redirect('repayment')

    if request.method == 'POST':
        form = RepaymentForm(request.POST)
        if form.is_valid():
            repayment = form.save(commit=False)
            repayment.save()
            messages.success(request, "Payment added successfully.")
            return redirect('repayment')
    else:
        form = RepaymentForm()

    context = {'form': form}
    return render(request, 'repayment/payment.html', context)

@login_required(login_url='login')
def loan_payment(request):
    user_loans = Loan.objects.filter(borrower=request.user)

    if not user_loans.exists():
        messages.warning(request, "You do not have any loans to repay.")
        return redirect('repayment')

    if request.method == 'POST':
        loan_id = request.POST.get('loan')
        method = request.POST.get('method')

        if loan_id and method:
            request.session['loan_id'] = loan_id
            request.session['method'] = method
            return redirect('add_payment')  # Redirect to Step 2

        messages.error(request, "Please select a loan and payment method.")

    return render(request, 'repayment/loan_payment.html', {'user_loans': user_loans})


@login_required(login_url='login')
def defaulted_loans(request):
    if request.user.is_superuser:
        user_loans = Loan.objects.all()
    else:
        user_loans = Loan.objects.filter(borrower=request.user)

    defaults = DefaultRecord.objects.filter(loan__in=user_loans)

    return render(request, 'defaults/list.html', {'defaults': defaults})

def add_defaulter_admin(request):
    if request.method == 'POST':
        form = DefaultRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('defaulters')  
    else:
        form = DefaultRecordForm()

    return render(request, 'defaults/add_defaulter.html', {'form': form})
 

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
    if request.user.is_superuser:
        cart_items = Loan.objects.all()  # Superusers see all loan items
    else:
        cart_items = Loan.objects.filter(status='pending', borrower=request.user)  # Normal users see only their pending items

    return render(request, 'admin/loan_cart.html', {'cart_items': cart_items,'cart_count': cart_items.count()})



@login_required(login_url='login')
def qualify_applicant(request, pk, status):
    if request.method == 'POST':
        app = get_object_or_404(LoanApplication, pk=pk)

        if status in ['approved', 'rejected']:
            app.status = status
            app.save()

    return redirect('loan_cart')

@staff_member_required (login_url='login')
def add_to_cart(request, application_id):
    application = get_object_or_404(LoanApplication, id=application_id)
    ReviewCart.objects.get_or_create(officer=request.user, application=application)
    return redirect('view_cart')
  

@staff_member_required(login_url='login')
def review_cart_view(request):
    if request.user.is_superuser:
        review_items = Borrower.objects.select_related('user', 'creditscore').all()
    else:
        # Staff users see only their own
        review_items = Borrower.objects.select_related('application').filter(officer=request.user)

    return render(request, 'admin/review_cart.html', {'review_items': review_items, 'review_count': review_items.count()})

@staff_member_required (login_url='login')
def view_cart(request):
    cart_items = ReviewCart.objects.filter(officer=request.user)
    return render(request, 'admin_cart/cart.html', {'cart_items': cart_items})

@staff_member_required (login_url='login')
def decide_loan(request, application_id, decision):
    if request.method == 'POST':
        application = get_object_or_404(LoanApplication, id=application_id)

        if decision.lower() in ['approved', 'rejected']:
            application.status = decision.lower()
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
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  
    return render(request, 'contact.html', {'form': form})

@login_required(login_url='login')
def disbursement_list(request):
    if request.user.is_superuser:
        disbursements = disbursement.objects.select_related('loan', 'loan__borrower')
    else:
        loans = Loan.objects.filter(borrower=request.user)
        disbursements = disbursement.objects.filter(loan__in=loans).select_related('loan')
    
    return render(request, 'disbursement/list.html', {'disbursements': disbursements})
def add_disbersement(request):
    form = disbursementForm()
    show_modal = False

    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('disbursement_list')  # safer to redirect than render modal for unauthorized users

    if request.method == 'POST':
        form = disbursementForm(request.POST, request.FILES)
        show_modal = True  
        if form.is_valid():
            form.save()
            messages.success(request, "Disbursement added successfully.")
            return redirect('disbursement_list')  # PRG pattern to avoid resubmission
        else:
            messages.error(request, "There was an error in the form.")

    disbursements = disbursement.objects.all()
    context = {
        'form': form,
        'disbursements': disbursements,
        'show_modal': show_modal
    }
    return render(request, 'disbursement/add_disbersment.html', context)

@login_required(login_url='login')
def loan_approval_list(request):
    if not request.user.is_superuser:
        
        return render(request, 'loanapproval/403.html') 

    approvals = loanapproval.objects.select_related('loan', 'approved_by').order_by('-approval_date')
    return render(request, 'loanapproval/list.html', {'approvals': approvals})

def setting(request):
    return render(request,'settings.html')

