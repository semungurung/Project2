from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user import views
from .views import Dashboard
from client import views as cview
from vendor import views as vview
from product import views as pview


app_name = 'dashboard'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('dispatch-ntf', pview.DispatchNtf.as_view(), name='dispatch_nt'),

    ##############################################################################
    ###################### Admin User Manage URLS ################################
    ##############################################################################
    path('client-user/', views.UserList.as_view(), name='usr_list'),
    path('client-delete/<int:pk>/',
         views.UserDelete.as_view(), name='usr_delete'),
    path('vendors/', views.VendorList.as_view(), name='vnd_list'),
    path('vendor-update/<int:pk>/',
         views.VendorUpdate.as_view(), name='vd_update'),
    path('vendor-delete/<int:pk>/',
         views.VendorDelete.as_view(), name='vd_delete'),

    ##############################################################################
    ################ Admin Manage eWaste Category URLS ###########################
    ##############################################################################
    path('waste-category/', cview.WasteCategoryList.as_view(),
         name='wst_catg_list'),
    path('waste-category-add/',
         cview.WasteCategoryCreate.as_view(), name='wst_catg_add'),
    path('waste-category-update/<int:pk>/',
         cview.WasteCategoryUpdate.as_view(), name='wst_catg_update'),
    path('waste-category-delete/<int:pk>/',
         cview.WasteCategoryDelete.as_view(), name='wst_catg_delete'),

    ##############################################################################
    ###################### Client Manage eWaste URLS #############################
    ##############################################################################
    path('my-ewastes/', cview.WasteList.as_view(), name='wst_list'),
    path('add-waste/', cview.AddWaste.as_view(), name='wst_add'),
    path('update-waste/<int:pk>/',
         cview.UpdateWaste.as_view(), name='wst_update'),
    path('find-buyer/<int:pk>/',
         cview.FindBuyerWaste.as_view(), name='wst_sell'),
    path('make-order/<int:wst_id>/<v_id>/',
         cview.MakeOrderWaste.as_view(), name='wst_order'),
    path('price/<int:w_id>/<v_id>/',
         cview.CategoryPriceView.as_view(), name='wst_catg_price'),

    ##############################################################################
    ###################### Client Manage eWaste Order URLS #######################
    ##############################################################################
    path('my-orders/', cview.MyOrderList.as_view(),
         name='myorder_list'),
    path('history-my-orders/', cview.MyHistoryOrderList.as_view(),
         name='history_myorder_list'),
    path('my-orders/cancel/<int:pk>/',
         cview.MyOrderCancel.as_view(), name='myorder_cancel'),
    path('my-orders/<int:pk>/',
         cview.MyOrderDetail.as_view(), name='myorder_detail'),

    ##############################################################################
    ###################### Vendor Manage eWaste Order URLS #######################
    ##############################################################################
    path('orders/', vview.OrderList.as_view(), name='order_list'),
    path('history-orders/', vview.HistoryOrderList.as_view(), name='history_order_list'),
    path('orders/sold/<int:pk>/',
         vview.OrderSold.as_view(), name='order_sold'),
    path('orders/<int:pk>/', vview.OrderDetail.as_view(),
         name='order_detail'),
    ##############################################################################
    ################ Vendor Manage eWaste Category Price URLS ###########################
    ##############################################################################
    path('category-price/', vview.CatgPriceList.as_view(),
         name='catg_prc_list'),
    path('category-price-add/',
         vview.CatgPriceCreate.as_view(), name='catg_prc_add'),
    path('category-price-update/<int:pk>/',
         vview.CatgPriceUpdate.as_view(), name='catg_prc_update'),
    path('category-price-delete/<int:pk>/',
         vview.CatgPriceDelete.as_view(), name='catg_prc_delete'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
      urlpatterns += static(settings.STATIC_URL,
                            document_root=settings.STATIC_ROOT)
