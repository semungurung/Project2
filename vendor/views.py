from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from user.models import Vendor
from .forms import PriceForm

from ewmis.permission import Is_VendorType_Mixin
from vendor.models import Order, WasteCategoryPrice


class OrderList(LoginRequiredMixin, Is_VendorType_Mixin, View):
    template_name = 'dashboard/vendor/orders.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['orders'] = Order.objects.filter(
            vendor__user=request.user, status='onhold').order_by('created')
        return render(request, self.template_name, context)


class HistoryOrderList(LoginRequiredMixin, Is_VendorType_Mixin, View):
    template_name = 'dashboard/vendor/orders.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['orders'] = Order.objects.filter(
            vendor__user=request.user).exclude(status='onhold').order_by('created')
        return render(request, self.template_name, context)


class OrderDetail(LoginRequiredMixin, Is_VendorType_Mixin, View):
    template_name = 'dashboard/vendor/order-detail.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['order'] = get_object_or_404(Order, id=kwargs['pk'])
        return render(request, self.template_name, context)


class OrderSold(View):

    def post(self, request, *args, **kwargs):
        o_id = self.kwargs['pk']
        od = Order.objects.get(id=o_id)
        od.status = "sold"
        od.save()
        messages.success(request, 'Order Sold Successfully')
        return redirect('dashboard:order_list')


class CatgPriceList(LoginRequiredMixin, Is_VendorType_Mixin, ListView):
    template_name = 'dashboard/vendor/price-list.html'
    model = WasteCategoryPrice
    context_object_name = 'prices'

    def get_queryset(self):
        if self.request.user.user_type == 'vendor':
            queryset = WasteCategoryPrice.objects.filter(
                vendor__user=self.request.user)
        else:
            queryset = WasteCategoryPrice.objects.all()
        return queryset


#########

class CatgPriceCreate(LoginRequiredMixin, Is_VendorType_Mixin, View):
    template_name = 'dashboard/vendor/price-create.html'

    def get(self, request, *args, **kwargs):
        form = PriceForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        print("@@@@@@@@@@@@")
        form = PriceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            vendor = Vendor.objects.get(user=request.user)
            wst = form.save(commit=False)
            wst.vendor = vendor
            try:
                wst.save()
                messages.success(request, 'Category Price Create Successfully')
                return redirect('dashboard:catg_prc_list')
            except Exception as e:
                messages.error(request, 'Category Price Already exist')
                return redirect('dashboard:catg_prc_list')

        else:
            messages.error(
                request, "Vendor Can't be Update Something went wrong")
            return render(request, self.template_name, {'form': form})


class CatgPriceUpdate(LoginRequiredMixin, Is_VendorType_Mixin, View):
    template_name = 'dashboard/vendor/price-update.html'

    def get(self, request, *args, **kwargs):
        p_id = self.kwargs['pk']
        pp = WasteCategoryPrice.objects.get(id=p_id)
        form = PriceForm(instance=pp)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        p_id = self.kwargs['pk']
        pp = WasteCategoryPrice.objects.get(id=p_id)
        form = PriceForm(request.POST or None,
                         request.FILES or None, instance=pp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Price Update Successfully')
            return redirect('dashboard:catg_prc_list')
        else:
            messages.error(
                request, "Category Price Can't be Update Something went wrong")
            return render(request, self.template_name, {'form': form})


class CatgPriceDelete(LoginRequiredMixin, Is_VendorType_Mixin, View):

    def post(self, request, *args, **kwargs):
        c_id = self.kwargs['pk']
        cp = WasteCategoryPrice.objects.get(id=c_id)
        cp.delete()
        messages.success(request, 'Category Price Delete Successfully')
        return redirect('dashboard:catg_prc_list')
