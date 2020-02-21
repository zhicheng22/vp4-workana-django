from django.shortcuts import render, redirect
from register.models import BaseUser
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Complaint_Model, Category, Type
from .forms import Create_Complaint_Form
from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin


class Member(ListView):
    model = Complaint_Model
    template_name = 'member.html'
    context_object_name = 'complaint_list'
    paginate_by = 1
    def get_queryset(self):
        return Complaint_Model.objects.filter(user_id=self.request.user.pk)

@login_required
def profile_page(request):
    return redirect('personal_information', pk=request.user.baseuser.pk)


@login_required
def personal_information(request, pk):
    user = User.objects.get(username=request.user.username)
    baseuser = BaseUser.objects.get(user=user)
    return render(request, 'personal_information.html', {'user': user, 'baseuser': baseuser})

class Profile_Edit(UpdateView):
    model = BaseUser
    fields = ['logo_cover', 'mobile_number', 'house_number', 'street_address', 'subdivision', 'city', 'zip_code']
    template_name = "profile_edit.html"
    success_url = reverse_lazy('profile_page')

class Complaint_List_View(ListView):
    model = Complaint_Model
    template_name = 'my_complaint.html'
    context_object_name = 'complaint_list'
    paginate_by = 1
    def get_queryset(self):
        return Complaint_Model.objects.filter(user_id=self.request.user.pk)

class Complaint_Update_View(UpdateView):
    model = Complaint_Model
    template_name = "complaint_update.html"
    form_class = Create_Complaint_Form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Complaint_Update_View, self).form_valid(form)
    success_url = reverse_lazy('my_complaint')


class Complaint_Detail_View(DetailView):
    model = Complaint_Model
    fields = ['respondent_first_name', 'respondent_last_name', 'respondent_address', 'category', 'type', 'subject', 'complain']
    template_name = 'complaint_detail.html'
    context_object_name = 'form'


class Create_Complaint_View(CreateView):
    model = Complaint_Model
    form_class = Create_Complaint_Form
    template_name = 'complaint_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Create_Complaint_View, self).form_valid(form)
    success_url = reverse_lazy('my_complaint')

@login_required
def load_types(request):
    category_id = request.GET.get('category')
    types = Type.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'type_dropdown_list_options.html', {'types': types})

class Generate_Pdf(PDFTemplateResponseMixin, DetailView):
    model = Complaint_Model
    fields = ['respondent_first_name', 'respondent_last_name', 'respondent_address', 'category', 'type', 'subject',
              'complain']
    template_name = 'complaint_pdf.html'
    context_object_name = 'form'
    show_content_in_browser = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        complaint_data = Complaint_Model.objects.filter(pk=self.kwargs['pk'])
        context['qr_content'] = "Respondent First Name: " + complaint_data[0].respondent_first_name + "\n"\
                                + "Respondent Last Name: " + complaint_data[0].respondent_last_name + "\n"\
                                + "Respondent_address: " + complaint_data[0].respondent_address + "\n"\
                                + "Category: " + str(complaint_data[0].category) + "\n"\
                                + "Type: " + str(complaint_data[0].type) + "\n"\
                                + "Subject: " + str(complaint_data[0].subject) + "\n"\
                                + "Complain: " + str(complaint_data[0].complain) + "\n"\
                                + "Date: " + str(complaint_data[0].created_date) + "\n"\
                                + "Time: " + str(complaint_data[0].created_time)
        return context

def canceling(request, pk):
    Complaint_Model.objects.filter(pk=pk).update(is_canceled='True')
    return redirect('my_complaint')
