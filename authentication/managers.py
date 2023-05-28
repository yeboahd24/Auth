from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import  gettext_lazy as _
import phonenumbers


class CustomUserManager(BaseUserManager):
    """A custom manager for the custom user model"""

    def create_user(self, email_or_phone, password=None, **extra_fields):
        """Create and save a new user using email or phone"""
        if not email_or_phone:
            raise ValueError(_('The Email or Phone field is required'))

        # Normalize and validate email or phone number
        try:
            validate_email(email_or_phone)
            email_or_phone = self.normalize_email(email_or_phone)
        except:
            parsed_number = phonenumbers.parse(email_or_phone, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError(_('Invalid Email or Phone'))
            country_code = str(parsed_number.country_code)
            national_number = str(parsed_number.national_number)
            email_or_phone = '+' + country_code + national_number

        # Validate password
        validate_password(password)

        user = self.model(email_or_phone=email_or_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_or_phone, password=None, **extra_fields):
        """Create and save a new superuser with the given email or phone and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email_or_phone, password=password, **extra_fields)

    def get_by_natural_key(self, email_or_phone):
        """Retrieve a user by their email or phone number"""
        try:
            return self.get(email_or_phone=email_or_phone)
        except self.model.DoesNotExist:
            return None

    def email_or_phone_exists(self, email_or_phone):
        """Check if a given email or phone number already exists in the database"""
        try:
            self.get(email_or_phone=email_or_phone)
            return True
        except self.model.DoesNotExist:
            return False
