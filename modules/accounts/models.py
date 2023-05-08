from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        """
        Creates and saves a User with the given email, full name
        and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        """
        Creates and saves a superuser with the given email, full name
        and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_doctor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    consulting_fees = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Specialization(models.Model):
    DISEASE_CHOICES = (
        ("Acne", "Acne"),
        ("Impetigo", "Impetigo"),
        ("Arthritis", "Arthritis"),
        ("Pneumonia", "Pneumonia"),
        ("Heart Attack,Allergy", "Heart Attack,Allergy"),
        ("Hyperthyroidism", "Hyperthyroidism"),
        ("Common Cold", "Common Cold"),
        ("Typhoid", "Typhoid"),
        ("Fungal infection", "Fungal infection")
    )

    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="specializations"
    )
    disease = models.CharField(max_length=100, choices=DISEASE_CHOICES)

    class Meta:
        db_table = "specializations"

    def __str__(self) -> str:
        return self.disease


class Slot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = "slots"

    def __str__(self) -> str:
        return str(self.id)
