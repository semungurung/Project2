import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from django.views.generic.base import View
from user.models import Vendor, ClientUser
from product.models import Waste, WasteCategory
from product.forms import WasteAddForm, WasteCategoryForm
from ewmis.permission import Is_AdminOrClientType, Is_ClientType_Mixin, Is_AdminType_Mixin
from vendor.models import Order, WasteCategoryPrice


##########################################################################
######################## Waste Category CRUD View #########################
##########################################################################


class WasteCategoryList(LoginRequiredMixin, Is_AdminType_Mixin, ListView):
    template_name = 'dashboard/waste/waste-catg-list.html'
    model = WasteCategory
    context_object_name = 'categories'


class WasteCategoryCreate(LoginRequiredMixin, Is_AdminType_Mixin, CreateView):
    model = WasteCategory
    template_name = 'dashboard/waste/add-waste-catg.html'
    form_class = WasteCategoryForm

    def form_invalid(self, form):
        messages.error(self.request, "Waste Category Can't be Create Something Went Wrong")
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        messages.success(self.request, 'Waste Category Create Successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard:wst_catg_list')


class WasteCategoryUpdate(LoginRequiredMixin, Is_AdminType_Mixin, UpdateView):
    template_name = 'dashboard/waste/update-waste-catg.html'
    model = WasteCategory
    form_class = WasteCategoryForm

    def form_invalid(self, form):
        messages.error(self.request, "Waste Category Can't be Update Something Went Wrong")
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        messages.success(self.request, 'Category Data Update Successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard:wst_catg_list')


class WasteCategoryDelete(View):

    def post(self, request, *args, **kwargs):
        wc_id = self.kwargs['pk']
        usr = WasteCategory.objects.get(id=wc_id)
        usr.delete()
        messages.success(request, 'Category Delete Successfully')
        return redirect('dashboard:wst_catg_list')


##########################################################################
######################## Waste CRUD View #########################
##########################################################################


class WasteList(LoginRequiredMixin, Is_AdminOrClientType, View):
    template_name = 'dashboard/waste/waste-list.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        print(request.user)
        if request.user.user_type == 'admin':
            context['wastes'] = Waste.objects.all().order_by('-created')
        else:
            context['wastes'] = Waste.objects.filter(owner=request.user)
        return render(request, self.template_name, context)


class AddWaste(LoginRequiredMixin, Is_ClientType_Mixin, View):
    template_name = 'dashboard/waste/add-waste.html'

    def get(self, request, *args, **kwargs):
        form = WasteAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = WasteAddForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            wst = form.save(commit=False)
            wst.owner = request.user
            wst.save()
            messages.success(self.request, 'Waste Create Successfully')
            return redirect('dashboard:wst_list')
        else:
            messages.error(self.request, "Waste Can't be Create Something Went Wrong")
            return render(request, self.template_name, {'form': form})


class UpdateWaste(LoginRequiredMixin, Is_ClientType_Mixin, View):
    template_name = 'dashboard/waste/update-waste.html'

    def get(self, request, *args, **kwargs):
        w_id = self.kwargs['pk']
        waste = Waste.objects.get(id=w_id)
        form = WasteAddForm(instance=waste)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        w_id = self.kwargs['pk']
        waste = Waste.objects.get(id=w_id)
        form = WasteAddForm(request.POST or None, request.FILES or None, instance=waste)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Waste Update Successfully')
            return redirect('dashboard:wst_list')
        else:
            messages.error(self.request, "Waste Can't be Update Something Went Wrong")
            return render(request, self.template_name, {'form': form})


class FindBuyerWaste(LoginRequiredMixin, Is_ClientType_Mixin, View):
    radius = 20
    template_name = 'dashboard/waste/sell-waste.html'

    def get(self, request, *args, **kwargs):
        waste = get_object_or_404(Waste, pk=kwargs['pk'])
        wst_loc = Point(waste.location_long, waste.location_lat, srid=4326)
        vendors = Vendor.objects.filter(geom__distance_lt=(wst_loc, Distance(km=self.radius)), verified=True)[:6]
        geojson = serialize('geojson', vendors,
                            geometry_field='geom',
                            fields=('company_name', 'pk', 'address', 'contact'))
        # wst_buffer = wst_loc.buffer(self.radius)
        # print(type(wst_buffer))
        # print(wst_buffer.contains(Point(waste.location_long, waste.location_lat, srid=4326)))
        context = dict()
        context['waste'] = waste
        context['waste_lat'] = waste.location_lat
        context['waste_long'] = waste.location_long
        context['geojson'] = geojson
        if vendors.exists():
            messages.success(self.request, 'Vendor Fetch Successfully')
        else:
             messages.error(self.request, "Sorry We're not able to find vendor in this area !")
        return render(request, self.template_name, context)


class MakeOrderWaste(LoginRequiredMixin, Is_ClientType_Mixin, View):
    template_name = 'dashboard/waste/order-waste.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        waste = get_object_or_404(Waste, id=kwargs['wst_id'])
        vendor = get_object_or_404(Vendor, id=kwargs['v_id'])
        print(waste, vendor)
        context['waste'] = waste
        context['vendor'] = vendor
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = dict()
        waste = get_object_or_404(Waste, id=kwargs['wst_id'])
        vendor = get_object_or_404(Vendor, id=kwargs['v_id'])
        client = get_object_or_404(ClientUser, user=request.user)
        try:
            order = Order(client=client, waste=waste, vendor=vendor)
            order.save()
            messages.success(self.request, 'Waste Order Successfully')
            return redirect('dashboard:myorder_list')
        except Exception as e:
            messages.error(self.request, 'You Already Make an Order for this Waste')
            return HttpResponse("You Already Make an Order for this Waste")


class MyOrderList(LoginRequiredMixin, Is_ClientType_Mixin, View):
    template_name = 'dashboard/waste/my-orders.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['orders'] = Order.objects.filter(client__user=request.user, status='onhold').order_by('-created')
        return render(request, self.template_name, context)


class MyHistoryOrderList(LoginRequiredMixin, Is_ClientType_Mixin, View):
    template_name = 'dashboard/waste/my-orders.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['orders'] = Order.objects.filter(client__user=request.user).exclude(status='onhold').order_by('-created')
        return render(request, self.template_name, context)


class MyOrderDetail(LoginRequiredMixin, Is_ClientType_Mixin, View):
    template_name = 'dashboard/waste/my-order-detail.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['order'] = get_object_or_404(Order, id=kwargs['pk'])
        return render(request, self.template_name, context)


class MyOrderCancel(View):

    def post(self, request, *args, **kwargs):
        o_id = self.kwargs['pk']
        od = Order.objects.get(id=o_id)
        od.status = "canceled"
        od.save()
        messages.success(request, 'Order Cancel Successfully')
        return redirect('dashboard:myorder_list')


class CategoryPriceView(View):

    def get(self, request, *args, **kwargs):
        w_id = self.kwargs['w_id']
        v_id = self.kwargs['v_id']
        waste = get_object_or_404(Waste, id=w_id)
        w_catg_id = waste.category.id
        catg = WasteCategoryPrice.objects.get(category_id=w_catg_id, vendor_id=v_id)
        data = {
            'pk': catg.id,
            'category': catg.category.id,
            'price': catg.price,
            'vendor': catg.vendor.id
        }
        return HttpResponse(json.dumps(data))
