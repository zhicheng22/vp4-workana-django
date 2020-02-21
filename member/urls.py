from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('member/', login_required(views.Member.as_view()), name='member'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('personal_information/<int:pk>', views.personal_information, name='personal_information'),
    path('profile_edit/<int:pk>', login_required(views.Profile_Edit.as_view()), name='profile_edit'),
    path('my_complaint/', login_required(views.Complaint_List_View.as_view()), name='my_complaint'),
    path('complaint_detail/<int:pk>', login_required(views.Complaint_Detail_View.as_view()), name='complaint_detail'),
    path('complaint_update/<int:pk>', login_required(views.Complaint_Update_View.as_view()), name='complaint_update'),
    path('generate_pdf/<int:pk>', login_required(views.Generate_Pdf.as_view()), name='generate_pdf'),
    path('complaint_form/', login_required(views.Create_Complaint_View.as_view()), name='complaint_form'),
    path('ajax/load-types/', views.load_types, name='ajax_load_types'),
    path('canceling/<int:pk>', views.canceling, name='canceling')
]
