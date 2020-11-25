from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout
from .models import noticeModel,jobModel
from .models import applicantModel
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

#from .models import *
from .forms import CreateUserForm
# Create your views here.
def registerView(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        registerForm = CreateUserForm()
        if request.method == 'POST':
            registerForm = CreateUserForm(request.POST)
            if registerForm.is_valid():
                registerForm.save()
                user1 = registerForm.cleaned_data.get('username')
                messages.success(request,'Account was successfully created for ' + user1)
                return redirect('login')
    context = {'registerForm':registerForm}
    return render(request, 'accounts/register.html', context)

def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username,password)
            user = authenticate(request,username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request,'Inavlid Credentials..')
        context = {}
        return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
def homeView(request):
    jobs = jobModel.objects.filter().order_by('-lastDateToApply')
    jobPaginator = Paginator(jobs,6)
    page_number = request.GET.get('page')
    page_obj = jobPaginator.get_page(page_number)
    context = {'jobs':jobs,'page_obj':page_obj}
    return render(request, 'accounts/dashboard.html', context)

def logoutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def noticeView(request):
    notices = noticeModel.objects.filter().order_by('-date')
    noticePaginator = Paginator(notices,6)
    page_number = request.GET.get('page_number')
    page_obj = noticePaginator.get_page(page_number)
    context = {'notice': notices,'page_obj':page_obj}
    return render(request, 'accounts/notices.html', context)

@login_required(login_url='login')
def applicantView(request):
    print(request.user)
    application = applicantModel.objects.filter(user = request.user)
    if not application:
        print("no application found")
        return HttpResponse("There are no applications")
    context = {'applicant' : application}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def applyToJobView(request,jobId):
    condition1 = Q(user = request.user)
    condition2 = Q(jobId = jobId)
    checkIfApplied = applicantModel.objects.filter(condition1 & condition2)
    if len(checkIfApplied):
        messages.info(request,'Already applied...')
    else:
        applicant = applicantModel(user = request.user, jobId = jobModel(id = jobId), status = 'In Process')
        applicant.save()
        messages.success(request,'Applied successfully...')
    
    return redirect('home')