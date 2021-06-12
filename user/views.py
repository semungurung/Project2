from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import (ListView, CreateView, UpdateView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import View

from ewmis.permission import Is_AdminType_Mixin
from .forms import ClientUserCreationForm, VendorUserCreationForm
from .models import ClientUser, Vendor, User
from .forms import VendorChangeForm
from django_email_verification import send_email


def index(request):
    return render(request, 'dashboard/dashboard.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=username, password=password)

        if user is not None:
            auth.login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('dashboard:dashboard')

        else:
            messages.error(request, "Error wrong username/password OR You're not verified Yet")
    return render(request, 'auth/login.html')


def Logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    return redirect('index')


def signup_client(request):
    template = 'auth/signup-client.html'
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = ClientUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(email=email, password=raw_password)
            user.is_active = False
            user.save()
            send_email(user)
            client = ClientUser.objects.get(user=user)
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            client.first_name = fname
            client.last_name = lname
            client.save()
            if user is not None:
                messages.success(request, 'Client User Sign Up Successfully')
                return redirect('login')
        else:
            messages.error(
                request, 'Please Enter Valid Values Or User Already Exist')
    else:
        form = ClientUserCreationForm()
    return render(request, template, {'form': form})


def signup_vendor(request):
    template = 'auth/signup-vendor.html'
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = VendorUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(email=email, password=raw_password)
            vendor = Vendor.objects.get(user=user)
            company_name = form.cleaned_data.get('company_name')
            address = form.cleaned_data.get('address')
            contact = form.cleaned_data.get('contact')
            vendor.company_name = company_name
            vendor.address = address
            vendor.contact = contact
            vendor.save()
            if user is not None:
                if user.user_type == "vendor" and user.vendor.verified:
                    messages.success(request, 'Vendor Sign Up Successfully')
                    return redirect('login')
                messages.success(
                    request, 'Vendor Sign Up Successfully but your not verified yet ')
                return redirect('login')
        else:
            messages.error(
                request, 'Please Enter Valid Values Or User Already Exist')
    else:
        form = VendorUserCreationForm()
    return render(request, template, {'form': form})


#########################################################
###### Admin User and Vendor List, Update, Delete  ######
#########################################################

class UserList(LoginRequiredMixin, Is_AdminType_Mixin, ListView):
    template_name = 'dashboard/user/user-list.html'
    model = ClientUser
    context_object_name = 'users'

    def get_queryset(self):
        queryset = ClientUser.objects.exclude(user__user_type='admin')
        return queryset


class UserDelete(LoginRequiredMixin, Is_AdminType_Mixin, View):

    def post(self, request, *args, **kwargs):
        u_id = self.kwargs['pk']
        cusr = ClientUser.objects.get(id=u_id)
        usr = User.objects.get(id=cusr.user.id)
        usr.delete()
        messages.success(request, 'User Delete Successfully')
        return redirect('dashboard:usr_list')


class VendorList(LoginRequiredMixin, Is_AdminType_Mixin, ListView):
    template_name = 'dashboard/user/vendor-list.html'
    model = Vendor
    context_object_name = 'vendors'


class VendorUpdate(LoginRequiredMixin, Is_AdminType_Mixin, View):
    template_name = 'dashboard/user/vendor-update.html'

    def get(self, request, *args, **kwargs):
        v_id = self.kwargs['pk']
        vd = Vendor.objects.get(id=v_id)
        form = VendorChangeForm(request.POST or None,
                                request.FILES or None, instance=vd)
        return render(request, self.template_name, {'form': form, 'vd': vd})

    def post(self, request, *args, **kwargs):
        v_id = self.kwargs['pk']
        vd = Vendor.objects.get(id=v_id)
        form = VendorChangeForm(request.POST or None,
                                request.FILES or None, instance=vd)
        form.save()
        messages.success(request, 'Vendor Update Successfully')
        return redirect('dashboard:vnd_list')


class VendorDelete(LoginRequiredMixin, Is_AdminType_Mixin, View):

    def post(self, request, *args, **kwargs):
        v_id = self.kwargs['pk']
        vd = Vendor.objects.get(id=v_id)
        usr = User.objects.get(id=vd.user.id)
        usr.delete()
        messages.success(request, 'Vendor Delete Successfully')
        return redirect('dashboard:vnd_list')


