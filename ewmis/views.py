from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from user.models import User, ClientUser, Vendor
from user.forms import ClientUpdateForm, VendorUpdateForm
from product.models import WasteCategory, Waste
from vendor.models import Order


class IndexPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class Dashboard(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = dict()
        user = request.user
        if user.user_type == 'admin':
            context['users_count'] = User.objects.all().count()
            context['total_vendor'] = User.objects.filter(user_type="vendor").count()
            context['total_client'] = User.objects.filter(user_type="user").count()
            context['total_waste'] = Waste.objects.all().count()
            context['total_order'] = Order.objects.all().count()
            context['total_waste_catg'] = WasteCategory.objects.all().count()
        elif user.user_type == 'vendor':
            vendor = get_object_or_404(Vendor, user=user)
            context['form'] = VendorUpdateForm(instance=vendor)
        else:
            client = get_object_or_404(ClientUser, user=user)
            context['user_form'] = ClientUpdateForm(instance=client)

        return render(request, 'dashboard/dashboard.html', context)

    def post(self, request, *args, **kwargs):
        context = dict()
        user = request.user
        if user.user_type == 'admin':
            pass
        elif user.user_type == 'vendor':
            vendor = get_object_or_404(Vendor, user=user)
            form = VendorUpdateForm(request.POST or None, request.FILES or None, instance=vendor)
            if form.is_valid():
                lat = form.cleaned_data['location_lat']
                lng = form.cleaned_data['location_long']
                pnt = Point(lng, lat, srid=4326)
                vd = form.save(commit=False)
                vd.geom = pnt
                vd.save()
                messages.success(request, 'Update Successfully')
                return redirect('dashboard:dashboard')
            else:
                context['lat'] = form.cleaned_data['location_lat']
                context['lng'] = form.cleaned_data['location_long']
                context['form'] = form
                messages.error(request, "Can't be Update Something went wrong")
                return render(request, 'dashboard/dashboard.html', context)
        else:
            client = get_object_or_404(ClientUser, user=user)
            form = ClientUpdateForm(request.POST or None, request.FILES or None, instance=client)
            if form.is_valid():
                form.save()
                messages.success(request, 'Update Successfully')
                return redirect('dashboard:dashboard')
            else:
                context['form'] = form
                messages.error(request, "Can't be Update Something went wrong")
                return render(request, 'dashboard/dashboard.html', context)
