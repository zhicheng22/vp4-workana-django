from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib import messages
from .tokens import account_activation_token
from .forms import *
from django.core.mail import EmailMessage
from .models import BaseUser

def customer_register(request):
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        baseForm = BaseForm(request.POST)

        if userForm.is_valid() and baseForm.is_valid():
            user = userForm.save(commit=False)
            user.email = userForm.cleaned_data['email']
            user.set_password(userForm.cleaned_data['password'])
            user.is_active = False
            user.save()

            mobile_number = baseForm.cleaned_data['mobile_number']
            house_number = baseForm.cleaned_data['house_number']
            street_address = baseForm.cleaned_data['street_address']
            subdivision = baseForm.cleaned_data['subdivision']
            city = baseForm.cleaned_data['city']
            zip_code = baseForm.cleaned_data['zip_code']
            baseuser = BaseUser(user=user, mobile_number=mobile_number, house_number=house_number, street_address=street_address,
                                subdivision=subdivision, city=city, zip_code=zip_code)
            baseuser.save()

            current_site = get_current_site(request)
            subject = 'Activate your Account'
            # create Message
            # message = render_to_string('accounts/account_activation_email.txt', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
            #     'token': account_activation_token.make_token(user),
            # })

            html_message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = userForm.cleaned_data.get('email')
            email = EmailMessage(subject, html_message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
        else:
            messages.error(request, ('Please correct the error below.'))

    else:
        userForm = UserForm()
        baseForm = BaseForm()
    return render(request, 'registration/register.html', {'userForm': userForm, 'baseForm': baseForm})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return HttpResponse('Your account has been activate successfully')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')
