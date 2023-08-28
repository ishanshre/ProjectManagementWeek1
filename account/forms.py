from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "department"]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "email", "department"]
