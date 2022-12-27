from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from PIL import Image
import datetime
import zoneinfo


class Category(models.Model):
    CATEGORY_TYPE = (("-", "outcome"), ("+", "income"))
    title = models.CharField(max_length=100, default="")
    image = models.ImageField(default='default_finance.png', upload_to='categories_pics')
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE, default="income")

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
        img.save(self.image.path)


# class Income(Category):
#     type = "+"
#     pass
#
#
# class Outcome(Category):
#     type = "-"
#     pass


class Transaction(models.Model):
    CATEGORY_TYPE = {"income": 1, "outcome": -1}
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    abs_balance_change = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    # currency = models.TextField(default='UAH')
    date = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('transaction-detail', kwargs={'pk': self.pk})


# class IncomeTransaction(Transaction):
#     category = models.ForeignKey(Income, on_delete=models.SET_NULL, blank=True, null=True)
#     pass
#
#
# class OutcomeTransaction(Transaction):
#     pass


class Filter(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # categories = models.Lis
    kyiv_tz = zoneinfo.ZoneInfo("Europe/Kyiv")
    current_year = datetime.datetime.now().year
    start_date = models.DateTimeField(default=datetime.datetime(current_year, 1, 1, 2, 0, tzinfo=kyiv_tz))
    end_date = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)

    def all_categories():
        category_list = Category.objects.all()
        return category_list

    categories = models.ManyToManyField(Category, through='FilterToCategories', default=all_categories)


class FilterToCategories(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
