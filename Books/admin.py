from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, BorrowedBook, Review

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Roles', {'fields': ('is_admin', 'is_librarian', 'is_member')}),
    )

    list_display = ('username', 'email', 'is_admin', 'is_librarian', 'is_member', 'is_staff')
    list_filter = ('is_admin', 'is_librarian', 'is_member', 'is_staff')
    search_fields = ("username", "email")

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date", "price", "user", "is_available","image")
    list_filter = ("is_available", "published_date")
    search_fields = ("title", "author")
    fields = ("title", "author", "published_date", "price", "user", "is_available", "image")

# BorrowedBook Admin Configuration
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "borrowed_date", "due_date", "returned", "is_overdue")
    list_filter = ("returned", "due_date")
    search_fields = ("user__username", "book__title")

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("user__username", "book__title")

admin.site.register(Review, ReviewAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BorrowedBook, BorrowedBookAdmin)