from django.urls import path
from . import views

app_name = 'uetfood'
urlpatterns = [
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('food/all', views.ListFoodView.as_view()),
    path('food', views.ListCreateFoodView.as_view()),
    path('food/<int:pk>', views.UpdateDeleteFoodView.as_view()),
    path('shopping-cart', views.ShoppingCartCreateAndDelete.as_view()),
    path('shopping-cart/<str:s>', views.ShoppingCartView.as_view()),
    path('order', views.OrderCreateView.as_view()),
    path('order/all', views.ListOrderView.as_view()),
    path('order-shipper', views.OrderShipperPostView.as_view()),
    path('order-shipper/<int:pk>/<str:s>', views.OrderStatusView.as_view()),
    path('order/shipper/<str:s>', views.OrderShipperGetView.as_view()),
    path('order/user/<str:s>', views.OrderUserGetView.as_view()),
    path('question', views.QuestionPostView.as_view()),
    path('question/all', views.ListQuestionView.as_view()),
    path('question/<str:s>', views.ListQuestionUserView.as_view()),
    path('answer', views.AnswerPostView.as_view()),
    path('comment', views.CommentPostView.as_view()),
    path('comment/all', views.ListCommentView.as_view()),
]
