# from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
# from rest_framework.reverse import reverse as api_reverse

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()




class StdUserRegisterSerializer(serializers.ModelSerializer):
    token               = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'sex',
            'phone',
            'first_name',
            'last_name',
            'password',
            'token',
            'stripe_customer_id',
        ]
        extra_kwargs={'password': {'write_only': True}}

    def get_token(self, obj): # instance of the model
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    # def create(self, validated_data):
    #     user_obj = User.objects.create(
    #         email=validated_data.get('email'),
    #         first_name=validated_data.get('first_name'),
    #         last_name=validated_data.get('last_name'),
    #         sex=validated_data.get('sex'),
    #         phone=validated_data.get('phone'),
    #         password=validated_data.get('password'))
    #     p = user_obj.password
    #     user_obj.set_password(p)
    #     user_obj.save()
    #     return user_obj

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'sex',
            'phone',
            # 'username',
            'first_name',
            'last_name',
            'password',
        ]
        extra_kwargs={'password': {'write_only': True}}

    def create(self, validated_data):
        user_obj = User.objects.create(
            email=validated_data.get('email'),
            # username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            sex=validated_data.get('sex'),
            phone=validated_data.get('phone'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj



class StdUserUpdaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'phone',
            'first_name',
            'last_name',
        ]





class StripeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model   = User
        fields  =[
            'id',
            'email',
            'phone',
            'first_name',
            'last_name',
            'stripe_customer_id',
        ]
        read_only_fields = [ 'stripe_customer_id']


