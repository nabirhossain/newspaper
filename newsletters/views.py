from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMultiAlternatives
# Same App importing
from newsletters.models import NewsLetterUsers
from newsletters.forms import NewsLetterUsersSignUpForm

from news.models import Category, Post
# Create your views here.


def newsletter_subscribe(request):
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    cat = Category.objects.all()
    """Subscription"""
    form = NewsLetterUsersSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsLetterUsers.objects.filter(email=instance.email).exists():
            messages.warning(request, 'Email already exists!',
                             'alert alert-warning alert-dismissible')
        else:
            instance.save()
            messages.success(request, 'Email has been submitted!',
                             'alert alert-success alert-dismissible')
            subject = 'Thank you for joining my Newsletter!'
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]

            with open(settings.BASE_DIR + '/templates/newsletters/subscribe_email_message.txt') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(subject=subject, body=signup_message,
                                             from_email=from_email, to=to_email)
            html_template = get_template('newsletters/subscribe_email_message.html').render()
            message.attach_alternative(html_template, 'text/html')
            message.send()

            # Hard coding, But also works fine
            # signup_message = 'Welcome to my Portfolio! If you would like to unsubscribe visit, http://127.0.0.1:8000/newsletter/unsubscribe'
            # send_mail(subject=subject, from_email=from_email, recipient_list=to_email,
            #           message=signup_message, fail_silently=False)

    context = {
        'form': form,
        'breaking' : breaking,
        'cat' : cat,
    }
    template = 'newsletters/subscribe.html'
    return render(request, template, context)


def newsletter_unsubscribe(request):
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    cat = Category.objects.all()
    """Un-subscription"""
    form = NewsLetterUsersSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsLetterUsers.objects.filter(email=instance.email).exists():
            NewsLetterUsers.objects.filter(email=instance.email).delete()
            messages.success(request, 'Email has been removed!',
                             'alert alert-success alert-dismissible')
            subject = 'You have been Unsubscribed!'
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]

            with open(settings.BASE_DIR + '/templates/newsletters/unsubscribe_email_message.txt') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(subject=subject, body=signup_message,
                                             from_email=from_email, to=to_email)
            html_template = get_template('newsletters/unsubscribe_email_message.html').render()
            message.attach_alternative(html_template, 'text/html')
            message.send()

            # Hard coding, But also works fine
            # signup_message = 'Sorry to see you go! Let us know if there is an issue with my service.'
            # send_mail(subject=subject, from_email=from_email, recipient_list=to_email,
            #           message=signup_message, fail_silently=False)

        else:
            messages.warning(request, 'Email is not in the Database!',
                             'alert alert-warning alert-dismissible')

    context = {
        'form': form,
        'breaking': breaking,
        'cat': cat,
    }
    template = 'newsletters/unsubscribe.html'
    return render(request, template, context)