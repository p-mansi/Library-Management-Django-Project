from django.core.mail import send_mail
from django.conf import settings

# Email notification for due/overdue books
def send_due_book_notification(user_email, book_title, due_date):
    subject = "Library Book Due Reminder"
    message = f"Hello,\n\nThe book '{book_title}' is due on {due_date}. Please return it on time.\n\nThank you!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])

