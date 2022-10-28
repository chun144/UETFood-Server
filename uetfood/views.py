import datetime

from django.contrib.auth import authenticate
from django.http import JsonResponse

# Create your views here.
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from uetfood.models import User, Food, ShoppingCart, Order, OrderComposition, OrderFood, OrderShipper, Question, \
    QuestionAnswer, Comment, Answer
from uetfood.serializers import UserRegistrationSerializer, UserLoginSerializer, FoodSerializer, ShoppingCartSerializer, \
    OrderSerializer, OrderSerializerGet, OrderShipperSerializer, QuestionSerializerPost, QuestionSerializerGet, \
    AnswerSerializerPost, AnswerSerializerGet, CommentSerializerPost, CommentSerializerGet


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Register successful!'
            data['username'] = user.username

            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This username has already exist!',
                'error_code': 409,
            }, status=status.HTTP_409_CONFLICT)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                user = User.objects.get(username=serializer.validated_data['username'])
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                    'username': serializer.validated_data['username'],
                    'role': user.role,
                    'nickname': user.nickname
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'username or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_message': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


class ListFoodView(ListCreateAPIView):
    permission_classes = [AllowAny]
    model = Food
    serializer_class = FoodSerializer

    def get_queryset(self):
        return Food.objects.all()


class ListCreateFoodView(ListCreateAPIView):
    model = Food
    serializer_class = FoodSerializer

    def create(self, request, *args, **kwargs):
        serializer = FoodSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Create a new Food unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteFoodView(RetrieveUpdateDestroyAPIView):
    model = Food
    serializer_class = FoodSerializer

    def put(self, request, *args, **kwargs):
        food = get_object_or_404(Food, id=kwargs.get('pk'))
        serializer = FoodSerializer(food, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Update Food unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        food = get_object_or_404(Food, id=kwargs.get('pk'))
        food.delete()

        return JsonResponse({
            'message': 'Delete Food successful!'
        }, status=status.HTTP_200_OK)


class ShoppingCartCreateAndDelete(APIView):

    def post(self, request):
        serializer = ShoppingCartSerializer(data=request.data)

        if serializer.is_valid():
            food = get_object_or_404(Food, id=serializer.data['foodId'])
            user = get_object_or_404(User, username=serializer.data['username'])
            try:
                ShoppingCart.objects.create(food=food, user=user)
            except Exception:
                return JsonResponse({
                    'message': 'Data already exists'
                }, status=status.HTTP_409_CONFLICT)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Data Invalid'
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = ShoppingCartSerializer(data=request.data)

        if serializer.is_valid():
            food = get_object_or_404(Food, id=serializer.data['foodId'])
            user = get_object_or_404(User, username=serializer.data['username'])
            shoppingCart = get_object_or_404(ShoppingCart, food=food, user=user)
            shoppingCart.delete()

            return JsonResponse({
                'message': 'Delete Food successful!'
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Data Invalid'
        }, status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartView(APIView):

    def get(self, request, s):
        user = get_object_or_404(User, username=s)
        shoppingCart = ShoppingCart.objects.filter(user=user)
        foods = []
        for i in shoppingCart:
            foods.append(i.food)

        serializer = FoodSerializer(foods, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class OrderCreateView(APIView):

    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            address = serializer.data['address']
            phone = serializer.data['phone']
            user = get_object_or_404(User, username=serializer.data['username'])
            note = serializer.data['note']
            date = datetime.date.today()
            order = Order.objects.create(user=user, address=address, phone=phone, note=note, date=date)

            listOrderComposition = serializer.data['listOrderComposition'].split(",")
            totalPrice = 0
            for i in listOrderComposition:
                orderComposition = i.split("-")
                food = get_object_or_404(Food, id=int(orderComposition[0]))
                quantity = int(orderComposition[1])
                totalPrice += food.price * quantity
                orderComposition = OrderComposition.objects.create(food=food, quantity=quantity)
                OrderFood.objects.create(orderComposition=orderComposition, order=order)

            order.totalPrice = totalPrice
            order.save()

            orderSerializer = OrderSerializerGet(order)
            return Response(data=orderSerializer.data, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Data Invalid'
        }, status=status.HTTP_400_BAD_REQUEST)


class ListOrderView(ListCreateAPIView):
    model = Order
    serializer_class = OrderSerializerGet

    def get_queryset(self):
        return Order.objects.all()


class OrderView(APIView):

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        serializer = OrderSerializerGet(order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class OrderShipperPostView(APIView):

    def post(self, request):
        serializer = OrderShipperSerializer(data=request.data)

        if serializer.is_valid():
            get_object_or_404(Order, id=serializer.data['orderId'])
            order = Order.objects.get(id=serializer.data['orderId'])
            shipper = get_object_or_404(User, username=serializer.data['username'])
            try:
                OrderShipper.objects.get(order=order)
                return JsonResponse({
                    'message': 'The order has been received'
                }, status=status.HTTP_406_NOT_ACCEPTABLE)
            except OrderShipper.DoesNotExist:
                try:
                    OrderShipper.objects.create(order=order, shipper=shipper)
                    order.status = 'Đang giao hàng'
                    order.save()
                except Exception:
                    return JsonResponse({
                        'message': 'Data already exists'
                    }, status=status.HTTP_409_CONFLICT)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Data Invalid'
        }, status=status.HTTP_400_BAD_REQUEST)


class OrderStatusView(APIView):

    def put(self, request, pk, s):
        s = s.strip()
        order = get_object_or_404(Order, pk=pk)
        if s == 'shipped':
            order.status = 'Đã giao hàng'
        elif s == 'canceled':
            order.status = 'Đã hủy đơn hàng'
        else:
            return JsonResponse({
                'message': 'status false'
            }, status=status.HTTP_400_BAD_REQUEST)

        order.save()

        serializer = OrderSerializerGet(order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class OrderShipperGetView(APIView):

    def get(self, request, s):
        shipper = get_object_or_404(User, username=s)
        orderShipper = OrderShipper.objects.filter(shipper=shipper)
        listOrder = []
        for i in orderShipper:
            listOrder.append(i.order)

        serializer = OrderSerializerGet(listOrder, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class OrderUserGetView(APIView):

    def get(self, request, s):
        user = get_object_or_404(User, username=s)
        listOrder = Order.objects.filter(user=user)

        serializer = OrderSerializerGet(listOrder, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class QuestionPostView(APIView):

    def post(self, request):
        serializer = QuestionSerializerPost(data=request.data)

        if serializer.is_valid():
            user = get_object_or_404(User, username=serializer.data['username'])
            text = serializer.data['text']
            date = datetime.date.today()
            question = Question.objects.create(user=user, text=text, date=date)

            questionSerializer = QuestionSerializerGet(question)
            return Response(data=questionSerializer.data, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Data Invalid'
        }, status=status.HTTP_400_BAD_REQUEST)


class ListQuestionView(ListCreateAPIView):
    model = Question
    serializer_class = QuestionSerializerGet

    def get_queryset(self):
        return Question.objects.all()


class QuestionView(APIView):

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        serializer = QuestionSerializerGet(question)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListQuestionUserView(APIView):

    def get(self, request, s):
        user = get_object_or_404(User, username=s)
        listQuestion = Question.objects.filter(user=user)

        serializer = QuestionSerializerGet(listQuestion, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AnswerPostView(APIView):

    def post(self, request):
        serializer = AnswerSerializerPost(data=request.data)

        if serializer.is_valid():
            user = get_object_or_404(User, username=serializer.data['username'])
            question = get_object_or_404(Question, id=serializer.data['questionId'])
            text = serializer.data['text']
            date = datetime.date.today()
            answer = Answer.objects.create(user=user, text=text, date=date)
            try:
                QuestionAnswer.objects.create(question=question, answer=answer)
            except Exception:
                return JsonResponse({
                    'message': 'Data already exists'
                }, status=status.HTTP_409_CONFLICT)

            answerSerializer = AnswerSerializerGet(answer)
            return Response(data=answerSerializer.data, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Data Invalid'
        }, status=status.HTTP_400_BAD_REQUEST)


class CommentPostView(APIView):

    def post(self, request):
        serializer = CommentSerializerPost(data=request.data)

        if serializer.is_valid():
            user = get_object_or_404(User, username=serializer.data['username'])
            text = serializer.data['text']
            rate = serializer.data['rate']
            date = datetime.date.today()
            comment = Comment.objects.create(user=user, text=text, date=date, rate=rate)

            commentSerializer = CommentSerializerGet(comment)
            return Response(data=commentSerializer.data, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Data Invalid'
        }, status=status.HTTP_400_BAD_REQUEST)


class ListCommentView(ListCreateAPIView):
    model = Comment
    serializer_class = CommentSerializerGet

    def get_queryset(self):
        return Comment.objects.all()
