from django.contrib import admin

# Register your models here.
from uetfood.models import User, Food, ShoppingCart, OrderComposition, Order, OrderFood, OrderShipper, Answer, Question, \
    QuestionAnswer, Comment

admin.site.register(User)
admin.site.register(Food)
admin.site.register(ShoppingCart)
admin.site.register(OrderComposition)
admin.site.register(Order)
admin.site.register(OrderFood)
admin.site.register(OrderShipper)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(Comment)
