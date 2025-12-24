
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, BorrowedBook, Review
from .forms import BookForm, RegisterForm
from .forms import BorrowBookForm, ReviewForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.timezone import now
from .utils import send_due_book_notification
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods





User = get_user_model()

@login_required
def book_list(request):
    query = request.GET.get('q', '')

    if request.user.is_admin or request.user.is_librarian:
        books = Book.objects.all() 
    else:
        books = Book.objects.filter(user=request.user) 

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    return render(request, "books/book_list.html", {"books": books, "query": query})



def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', pk=book.pk)

    return render(request, 'books/book_detail.html', {'book': book, 'review_form': review_form})


def is_librarian_or_admin(user):
    return user.is_authenticated and (user.is_admin or user.is_librarian)

@login_required
@user_passes_test(is_librarian_or_admin)
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            if request.user.is_authenticated:
                book.user = request.user 
            else:
                messages.error(request, "You must be logged in to create a book.")
                return redirect("login")
            book.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "books/book_form.html", {"form": form})



@login_required
@user_passes_test(is_librarian_or_admin)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)  
            if 'image' in request.FILES:
                book.image = request.FILES['image']
            book.save()  
            return redirect('book_list')
        
            
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})


@login_required
@user_passes_test(is_librarian_or_admin)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('book_list')
    return render(request, 'books/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def check_due_books():
    due_books = BorrowedBook.objects.filter(due_date__lte=now())
    
    for borrowed in due_books:
        send_due_book_notification(borrowed.user.email, borrowed.book.title, borrowed.due_date)


def is_member(user):
    return user.is_authenticated and user.is_member

@login_required
@user_passes_test(is_member)
def borrow_book(request, book_id):
    
    book = get_object_or_404(Book, id=book_id)

    
    if not request.user.is_authenticated:
        return HttpResponse("User is not authenticated", status=403)

    try:
        borrowed_book = BorrowedBook.objects.create(
            user=request.user,  # Ensure user is valid
            book=book,
        )

        book.is_available = False
        book.save()
        return redirect('book_list')
    except IntegrityError:
        return HttpResponse("<script> alert(Error: Cannot borrow this book due to a database constraint. press back) </script>", status=400)


@login_required
@user_passes_test(is_member)
def return_book(request, borrowed_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_id)

    if borrowed_book.user == request.user or request.user.is_staff:
        book = borrowed_book.book
        book.is_available = True  
        book.save()
        borrowed_book.delete()
        messages.success(request, f"You returned '{book.title}'.")
    else:
        messages.error(request, "You cannot return a book you didn't borrow.")

    return redirect('book_list')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  
            
            role = request.POST.get("role")
            if role == "admin":
                user.is_admin = True
            elif role == "librarian":
                user.is_librarian = True
            else:
                user.is_member = True 

            user.save()
            login(request, user)
            return redirect("book_list")
    else:
        form = RegisterForm()
    return render(request, "books/register.html", {"form": form})

@login_required
def list_reviews(request, book_id):
    """Fetch all reviews for a book"""
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all().values("user__username", "rating", "comment", "created_at")
    return JsonResponse({"reviews": list(reviews)})


@require_http_methods(["POST"])
@login_required
def add_or_edit_review(request, book_id):
    try:
        data = json.loads(request.body.decode("utf-8"))
        review_text = data.get("review")
        rating = data.get("rating")
        
        if not review_text or not rating:
            return JsonResponse({"error": "Missing review or rating"}, status=400)
        
        book = get_object_or_404(Book, id=book_id)
        
        existing_review = Review.objects.filter(book=book, user=request.user).first()
        
        if existing_review:
            existing_review.comment = review_text 
            existing_review.rating = int(rating)
            existing_review.save()
            message = "Review updated successfully"
        else:
            # Create new review
            Review.objects.create(
                book=book,
                user=request.user,
                comment=review_text,
                rating=int(rating)
            )
            message = "Review added successfully"
        
        return JsonResponse({"success": True, "message": message})
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@login_required
def delete_review(request, book_id):
    """Delete review (Only if the user wrote it)"""
    book = get_object_or_404(Book, id=book_id)
    review = get_object_or_404(Review, book=book, user=request.user)
    review.delete()
    return JsonResponse({"message": "Review deleted"})
