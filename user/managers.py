from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Permission


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.user_type = 'admin'
        permissions = Permission.objects.all()
        for p in permissions:
            user.user_permissions.add(p)
        user.save(using=self._db)
        return user