from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book,BorrowedBook, CustomUser,Review
from django.contrib.auth import get_user_model

User = get_user_model()

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['book', 'due_date']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_date", "price", "image"]
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ("member", "Member"),
        ("librarian", "Librarian"),
        ("admin", "Admin"),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)  # Role selection

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "role"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
