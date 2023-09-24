from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator


class PremiumPlan(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    price = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

    longtime = models.DurationField()

    def __str__(self):
        return self.name


class PremiumOrder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='premium_orders')
    plan = models.ForeignKey('PremiumPlan', on_delete=models.SET_NULL, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)
    paid_count = models.IntegerField()
    tracking_code = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        ordering = ('paid', '-datetime_modified')

    def __str__(self):
        return f'{self.user} - {str(self.id)}'


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
