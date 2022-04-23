from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    realname = models.CharField(max_length=100)
    wid = models.AutoField(primary_key=True)
    man = models.BooleanField()
    birth = models.DateField()

    def __str__(self):
        return self.realname

class Book(models.Model):
    ISBN = models.CharField(max_length=20, primary_key=True, null=False)
    name = models.CharField(max_length=50)
    public = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    amount = models.PositiveIntegerField(default=0)

    def __str(self):
        return self.name

class Import(models.Model):
    iid = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    amount = models.PositiveIntegerField(default=0)
    status = models.IntegerField(default=0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class Bill(models.Model):
    bid = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    operator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    earn_cost = models.DecimalField(max_digits=9, decimal_places=2)