from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.template.backends import django
from django.utils import timezone


class User(AbstractUser):
    last_login = None

    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=10, default='user')
    nickname = models.CharField(max_length=20)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Food(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    price = models.IntegerField(default=0)


class OrderComposition(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default=None)
    phone = models.CharField(max_length=20, default=None)
    note = models.CharField(max_length=255, default=None)
    totalPrice = models.IntegerField(default=0)
    date = models.CharField(max_length=20, default=None)
    status = models.CharField(max_length=50, default='Đã đặt hàng')
    listOrderComposition = models.ManyToManyField(OrderComposition, through='OrderFood')


class OrderFood(models.Model):
    orderComposition = models.ForeignKey(OrderComposition, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['orderComposition', 'order']]


class OrderShipper(models.Model):
    shipper = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['shipper', 'order']]


class ShoppingCart(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['food', 'user']]


class Answer(models.Model):
    text = models.CharField(max_length=2000, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=20, default=None)


class Question(models.Model):
    text = models.CharField(max_length=2000, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=20, default=None)
    listAnswer = models.ManyToManyField(Answer, through='QuestionAnswer')


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['question', 'answer']]


class Comment(models.Model):
    text = models.CharField(max_length=2000, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=20, default=None)
    rate = models.FloatField(default=0.0)
