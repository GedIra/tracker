from django.core.mail import EmailMessage

subject = "Verify your account"
username = "Irene Kalisa"
link = "https//:welcome.com"

body = "Hello " + username + "\nUse this link to complete your Berwa Legacy Company account registration\n" + "by clicking this link " + link


# def acc_verification_email(request):
#     pass

email = EmailMessage(
    subject=subject,
    body=body,
    from_email="irankundag65@gmail.com",
    to=["irenendizihiwe@gmail.com",]
)
email.send(fail_silently=True)