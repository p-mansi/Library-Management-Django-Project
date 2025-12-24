from django.urls import path
from .views import book_list, book_create, book_update, book_delete, register, user_login, user_logout,borrow_book, return_book, list_reviews, add_or_edit_review, delete_review, book_detail
from django.contrib.auth.views import PasswordChangeView
urlpatterns = [
    path('', book_list, name='book_list'),
    path('create/', book_create, name='book_create'),
    path('update/<int:pk>/', book_update, name='book_update'),
    path('delete/<int:pk>/', book_delete, name='book_delete'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('return/<int:borrowed_id>/', return_book, name='return_book'),
    path('book/<int:pk>/', book_detail, name='book_detail'),
    path("books/<int:book_id>/reviews/", list_reviews, name="list_reviews"),
    path("books/<int:book_id>/review/add/", add_or_edit_review, name="add_review"),
    path("books/<int:book_id>/review/delete/", delete_review, name="delete_review"),
    path('admin/password-change/', PasswordChangeView.as_view(template_name='admin/password_change.html'), name='admin_password_change'),

]
