from rest_framework import serializers
from .models import User, Food, OrderComposition, Order, Question, Answer, Comment


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'role', 'nickname']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = User(
            username=self.validated_data['username'],

        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        role = self.validated_data['role']
        nickname = self.validated_data['nickname']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})
        user.set_password(password)
        user.role = role
        user.nickname = nickname
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name', 'image', 'description', 'price')


class ShoppingCartSerializer(serializers.Serializer):
    foodId = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)


class OrderCompositionSerializer(serializers.ModelSerializer):
    food = FoodSerializer()

    class Meta:
        model = OrderComposition
        fields = ('food', 'quantity')


class OrderSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    listOrderComposition = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    note = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname')
        depth = 1


class OrderSerializerGet(serializers.ModelSerializer):
    listOrderComposition = OrderCompositionSerializer(many=True)
    user = UserSerializer(required=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'address', 'phone', 'totalPrice', 'date', 'status', 'listOrderComposition', 'note')


class OrderShipperSerializer(serializers.Serializer):
    orderId = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)


class QuestionSerializerPost(serializers.Serializer):
    username = serializers.CharField(required=True)
    text = serializers.CharField(required=True)


class AnswerSerializerPost(serializers.Serializer):
    username = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    questionId = serializers.IntegerField(required=True)


class AnswerSerializerGet(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Answer
        fields = ('id', 'text', 'user', 'date')


class QuestionSerializerGet(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    listAnswer = AnswerSerializerGet(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'user', 'date', 'listAnswer')


class CommentSerializerPost(serializers.Serializer):
    username = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    rate = serializers.FloatField(required=True)


class CommentSerializerGet(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'user', 'date', 'rate')

