from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404


class Is_AdminType_Mixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        permission = user.user_type == 'admin'
        return permission


class Is_ClientType_Mixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        permission = user.user_type == 'user'
        return permission


class Is_VendorType_Mixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        permission = user.user_type == 'vendor'
        return permission


class Is_AdminOrClientType(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        permission = user.user_type == 'admin' or user.user_type == 'user'
        return permission

# class SameUserOnlyMixin(object):
#
#     def has_permissions(self):
#         # Assumes that your Article model has a foreign key called `auteur`.
#         return self.get_object().auteur == self.request.user
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permissions():
#             raise Http404('You do not have permission.')
#         return super(SameUserOnlyMixin, self).dispatch(
#             request, *args, **kwargs)
