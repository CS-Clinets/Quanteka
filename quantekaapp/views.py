import os

from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Report, ReportCategory
from .powerbi_utils import Utils
from .forms import CreateUserForm
from quantekaapp.services.pbiembedservice import PbiEmbedService

import math, random
from django.contrib.auth.models import User

# Create your views here.
def mailtrigger(params):
    subject = 'Trigger From: ' + params.get('formname', '')
    mydict = {'fullname': params.get('fullname', ''), 'email': params.get('email', ''), 'mobileno': params.get('mobileno', ''),
              'user_subject': params.get('user_subject', ''), 'user_message': params.get('user_message', ''), 'subject': subject}
    html_template = 'register_email.html'
    html_message = render_to_string(html_template, context=mydict)
    email_from = settings.EMAIL_HOST_USER
    # recipient_list = ['']
    recipient_list = ['quanteka@quanteka.com']
    message = EmailMessage(subject, html_message,
                           email_from, recipient_list)
    message.content_subtype = 'html'
    message.send()


# Redirect to login.
def accountlogin(request):
    # Get the current query string
    q = request.META['QUERY_STRING']
    return redirect(reverse('login') + '?' + q)


# Create your views here.
def index(request):
    if request.method == 'POST':
        formname = request.POST.get('form_name')
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        mobileno = request.POST.get('number')
        user_message = request.POST.get('message')

        # Calling Trigger Mail Function
        if formname:
            params = {'formname': formname, 'fullname': fullname, 'email': email, 'mobileno': mobileno,
                      'user_message': user_message}
            mailtrigger(params)
    return render(request, 'index.html')


def about(requests):
    return render(requests, 'about.html')


def contact(request):
    if request.method == 'POST':
        formname = request.POST.get('form_name')
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        mobileno = request.POST.get('number')
        user_subject = request.POST.get('subject')
        user_message = request.POST.get('message')
        # Calling Trigger Mail Function
        if formname:
            params = {'formname': formname, 'fullname': fullname, 'email': email, 'mobileno': mobileno,
                      'user_subject': user_subject, 'user_message': user_message}
            mailtrigger(params)

    return render(request, 'contact.html')


def footer(request):
    if request.method == 'POST':
        formname = request.POST.get('form_name')
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        mobileno = request.POST.get('number')

        # Calling Trigger Mail Function
        if formname:
            params = {'formname': formname, 'fullname': fullname,
                      'email': email, 'mobileno': mobileno}
            mailtrigger(params)

    return redirect(request, 'index.html')

def services(requests):
    return render(requests, 'services.html')


def onepage(requests):
    return render(requests, 'one-page.html')

# login


def loginPage(request):
    if request.method == 'POST':
        login_redirect = request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if login_redirect:
                return redirect(login_redirect)
            else:
                return redirect('/dashboard')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'login.html', context)

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_otp(request):
    email = request.POST.get("email")
    otp = generateOTP()
    htmlgen = '<p>Your OTP is <strong>' +otp+ '</strong></p>'
    send_mail('OTP request', otp, 'quanteka@quanteka.com', [email], fail_silently=False, html_message=htmlgen)
    return otp


# otp2
def otp2(request):
    return render(request,'otp_verify2.html')


# register
def register(request):
    login_redirect = request.POST.get('next')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            otp = send_otp(request)
            request.session['username'] = request.POST.get('username')
            request.session['email'] = request.POST.get('email')
            request.session['password'] = request.POST.get('password1')
            request.session['sent_otp'] = otp
            return redirect('/verify-otp/?next=' + str(login_redirect))
    context={'form':form}
    return render(request,'register.html',context)

def register_final(request):
    login_redirect = request.POST.get('next') 
    if request.method == 'POST':
        otp = request.POST.get("otp")
        sent_otp = request.session.get('sent_otp')
        if otp==sent_otp:
            username = request.session.get('username')
            password = request.session.get('password')
            email = request.session.get('email')
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()
            messages.success(request, 'Account was created for ' + username )
            return redirect('/login/?next=' + str(login_redirect))
        else:
            messages.error(request, "Please Enter Valid OTP.")
            return redirect('/verify-otp/?next=' + str(login_redirect))
    return render(request,'otp_verify.html')


def mylogout(request):
    request.user = None
    logout(request)
    return redirect('/')


# dashboard page

def dashboard(requests):
    reports = Report.objects.all()
    categories = ReportCategory.objects.all()
    context = {
        'reports': reports,
        'categories': categories
    }
    return render(requests, 'dashboard.html', context)

# Overview page


def overview(requests):
    return render(requests, 'overview.html')


@login_required
def get_embed_info(request):
    '''Returns report embed configuration'''

    config_result = Utils.check_config()
    
    if config_result is not None:
        return JsonResponse({'errorMsg': config_result}, status=500)

    try:
        reportID = request.GET.get('r_id', None)
        print(reportID)
        embed_info = PbiEmbedService().get_embed_params_for_single_report(
            report_id=reportID, workspace_id=os.environ['WORKSPACE_ID']
        )
        print(embed_info)
        return JsonResponse(embed_info, safe=False)
    except Exception as ex:
        return JsonResponse({'errorMsg': str(ex)}, status=500)

@login_required
def report_detail(request):
    r_id = request.GET.get('reportId', None)
    report = get_object_or_404(Report, report_id=r_id)
    return render(request, "report-detail.html", {"report": report})
