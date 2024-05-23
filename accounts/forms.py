from django.contrib.auth.forms import UserCreationForm
from .models import User

class signUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2')