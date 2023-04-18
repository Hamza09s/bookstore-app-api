"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()  # serializer for user object
        # will also tell what model to serialize in as model is defined
        fields = ["email", "password", "name"]  # only allow fields
        # that user will be able to change with api,not admin related things
        # like is_staff
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        # extra meta data to tell the django rest framework whether
        # we want the data to be read/write only
        # write means they can only write the password not read it

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    # override create from serializer so only create if validation is passed

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop("password", None)
        # basically checks if user has passed password to be updated
        user = super().update(instance, validated_data)
        # model instance,validated data that has passed serializer
        # we are overriding here because default behavior is sending
        # clear text not hashed passwords also model instance means
        # get_user_model()

        if password:
            user.set_password(password)
            user.save()

        return user


# class AuthJwtSerializer(serializers.Serializer):
#     """Serializer for the user auth token."""

#     email = serializers.EmailField()
#     password = serializers.CharField(
#         style={"input_type": "password"},
#         # want input type to be a password so text is hidden
#         # even though you only use browsable api for testing and development
#         trim_whitespace=False,
#         # incase user wants space in their password
#     )

#     def validate(self, attrs):
#         """Validate and authenticate the user."""
#         email = attrs.get("email")
#         password = attrs.get("password")
#         user = authenticate(
#             request=self.context.get("request"),
#             username=email,
#             password=password,
#         )
#         if not user:
#             msg = _("Unable to authenticate with provided credentials.")
#             raise serializers.ValidationError(msg, code="authorization")

#         attrs["user"] = user
#         return attrs
