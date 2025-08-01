from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ContactPage,  add_to_cart,  base, borrower_details, decide_loan, defaulted_loans, disbursement_list, loan_approval_list, loan_cart, loan_table_view, qualify_applicant, repayment, signup,loginpage, index, view_cart, welcoming, profile,logoutuser, chart , apply_for_loan , loan_success , borrower_loans

urlpatterns = [
    path('', welcoming, name='welcoming'),

    path('signup/', signup, name='signup'),
    path('login/', loginpage, name='login'),
    path('logout/', logoutuser, name='logout'),
    path('profile/<str:pk>/', profile, name='profile'),

    path('index/', index, name='index'),

    path('chart/', chart, name='chart'),

    path('apply/', apply_for_loan, name='apply_for_loan'),
    path('loan_success/', loan_success, name='loan_success'),
    path('borrowers/', borrower_loans, name='borrower_loans'),
    path('borrower/<int:pk>/', borrower_details, name='borrower_details'),    
    
    path('base/', base, name='base'),


    path('loan-cart/', loan_cart, name='loan_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('admin/cart/add/<int:application_id>/', add_to_cart, name='add_to_cart'),
    path('admin/cart/decide/<int:application_id>/<str:decision>/', decide_loan, name='decide_loan'),

    path('repayment/', repayment, name='repayment'),
    path('defaulters/', defaulted_loans, name='defaulters'),
    path('disbursement/', disbursement_list, name='disbursement_list'),
    path('loan-approvals/', loan_approval_list, name='loan_approval_list'),

    path('contact/', ContactPage, name='contact'),

    
    path('qualify/<int:pk>/<str:status>/', qualify_applicant, name='qualify_applicant'),

    path('loan-tables/', loan_table_view, name='loan_tables'),

]

# Serve media and static files only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
