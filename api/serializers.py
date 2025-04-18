from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Role
'''
class AuthUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )

    def create(self, validated_data):
        email = validated_data.get('email')
        validated_data['created_by'] = email
        validated_data['modified_by'] = email
        validated_data['first_name'] = 'Pedro'
        validated_data['last_name'] = 'Mamani Choque'
        auth_user = User.objects.create_user(**validated_data)
        return auth_user
'''

class AuthUserRegistrationSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Role.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'roles', 
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        roles_data = validated_data.pop('roles', None)
        email = validated_data.get('email')

        validated_data['created_by'] = email
        validated_data['modified_by'] = email

        user = User.objects.create_user(**validated_data)

        if roles_data:
            user.roles.set(roles_data)
        else:
            
            cliente_role, _ = Role.objects.get_or_create(name="Cliente")
            user.roles.add(cliente_role)

        return user

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Role.objects.all()
    )

    class Meta:
        model = User
        fields = (
            'id', 'uid', 'email', 'first_name', 'last_name',
            'roles', 'date_joined', 'is_active', 'is_deleted',
            'created_date', 'modified_date', 'created_by', 'modified_by'
        )
        read_only_fields = ('uid', 'date_joined', 'created_date', 'modified_date')


class AuthUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    roles = serializers.ListField(child=serializers.CharField(), read_only=True)
    full_name = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'full_name': user.get_full_name(),
                'roles': [role.name for role in user.roles.all()],

            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")