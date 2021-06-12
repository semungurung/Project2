from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from .models import Notification


class DispatchNtf(View):

    def get(self, request, *args, **kwargs):
        if 'id' in request.GET:
            id = request.GET['id']
            ntf = Notification.objects.get(id=id)
            ntf.seen = True;
            ntf.save()
            return JsonResponse({"message": "success"})
        return JsonResponse({"message": "Something went wrong"})
