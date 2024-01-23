from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    # birth_date = serializers.DateField()
    # first_name = serializers.CharField(max_length=128)
    # last_name = serializers.CharField(max_length=128)
    # 'first_name', 'last_name', 'birth_date'

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'phone_number', 'email', 'password']