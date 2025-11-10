from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    ]
    MEDICAL_SPECIALIZATIONS = [
        ("CARD", "Cardiology"),
        ("DERM", "Dermatology"),
        ("NEUR", "Neurology"),
        ("ORTH", "Orthopedics"),
        ("PSYC", "Psychiatry"),
        ("PED", "Pediatrics"),
        ("ONCO", "Oncology"),
        ("GYNE", "Gynecology"),
        ("ENT", "Otolaryngology (ENT)"),
        ("OPHTH", "Ophthalmology"),
        ("SURG", "General Surgery"),
        ("UROL", "Urology"),
        ("NEPH", "Nephrology"),
        ("GAST", "Gastroenterology"),
        ("ENDO", "Endocrinology"),
        ("HEMA", "Hematology"),
        ("IMM", "Immunology"),
        ("RHEU", "Rheumatology"),
        ("PULM", "Pulmonology"),
        ("ANES", "Anesthesiology"),
        ("EMER", "Emergency Medicine"),
        ("PATH", "Pathology"),
        ("RAD", "Radiology"),
        ("FAM", "Family Medicine"),
        ("INT", "Internal Medicine"),
        ("DENT", "Dentistry"),
        ("PSUR", "Plastic Surgery"),
        ("REHAB", "Rehabilitation Medicine"),
        ("NEON", "Neonatology"),
        ("GERI", "Geriatrics"),
        ("TROP", "Tropical Medicine"),
        ("NUCL", "Nuclear Medicine"),
        ("SPORT", "Sports Medicine"),
        ("OCCU", "Occupational Medicine"),
    ]
    
    email = models.EmailField(max_length=255, verbose_name="Email Address", unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role =  models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='user/avatar/')
    medical_spesification = models.CharField(choices=MEDICAL_SPECIALIZATIONS, null=True, blank=True)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=255, null=True, blank=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return super().has_module_perms(app_label)
