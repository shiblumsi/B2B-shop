from django.contrib.auth.base_user import BaseUserManager


class CustomMerchantManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None, **extra_fields):
        if not email:
            raise ValueError("Email Required!!!")
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)