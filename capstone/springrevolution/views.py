from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template import loader
from django.http import JsonResponse
from django.db.models import F
from datetime import date
import datetime


from .util import password_validation, mail_service
from .models import User, Link, Message

def index(request, email_status=''):
    return render(request, 'springrevolution/index.html', {
        "email_status":email_status
    })

def show_page(request, page):
    # request=request is essential for csrf_token to work!
    html_content = loader.render_to_string(f'springrevolution/{page}.html', request=request)
    return HttpResponse(html_content)

global_credentials = []
def register(request):
    if request.method == "POST":
        nickname = request.POST.get("nickname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Checking for username duplication
        username_list = User.objects.values_list('username', flat=True)
        if nickname in username_list:
            return render(request, 'springrevolution/register.html',{
                "error1":"Nickname already taken"
            })

        # Checking for email duplication
        email_list = User.objects.values_list('email', flat=True)
        if email in email_list:
            return render(request, 'springrevolution/register.html',{
                "error2":"Email already taken"
            })

        # Checking for passwords length, lowercase, and uppercase
        if password_validation(password) is False:
            return render(request, 'springrevolution/register.html',{
                "error3":"At least 8 characters and both uppercase & lowercase letters are required."
            })

        # Ensure password matches confirmation
        if password != confirm_password:
            return render(request, 'springrevolution/register.html',{
                "error4":"Passwords must match."
            })

        # If all inputs are valid, send confirmation email
        global global_credentials
        global_credentials.extend([nickname, email, password])

        subject = 'Please Confirm the Registration'
        message = ''
        email_from = settings.EMAIL_HOST_USER
        recipient_lists = [email]
        html_message = loader.render_to_string('springrevolution/confirmation_email.html', {
            "name": nickname
        })

        send_mail(subject, message, email_from, recipient_lists, fail_silently=False, html_message=html_message)
        return render(request, 'springrevolution/email_sent.html',{
            "email":email,
            "reset_password":False
        })

    else:
        return render(request, 'springrevolution/register.html')

def confirm_registration(request):
    # create a user in the database
    user = User.objects.create_user(global_credentials[0], global_credentials[1], global_credentials[2])
    user.save()
    global_credentials.clear()

    return render(request, 'springrevolution/login.html',{
        "success1":"You have been successfully registered!"
    })

global_reset_email = None
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        reset_email = request.POST.get("reset_email")

        user = authenticate(request, username=username, password=password)

        # if authentication is successful
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # else if it is resetting email instead of loggin in
        elif reset_email:
            subject = 'Resetting Password for the Account'
            message = ''
            email_from = settings.EMAIL_HOST_USER
            recipient_lists = [reset_email]
            html_message = loader.render_to_string('springrevolution/reset_password.html',{
                "email":reset_email
            })

            global global_reset_email
            global_reset_email = reset_email

            send_mail(subject, message, email_from, recipient_lists, fail_silently=False, html_message=html_message)
            return render(request, 'springrevolution/email_sent.html',{
                "email":reset_email,
                "reset_password":True
            })
        # if authentication fails
        else:
            return render(request, 'springrevolution/login.html',{
                "error":"Invalid username and/or password"
            })
    else:
        return render(request, 'springrevolution/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def reset_password(request):
    if request.method == "POST":
        email_address = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Checking for passwords length, lowercase, and uppercase
        if password_validation(password) is False:
            return render(request, 'springrevolution/reset.html',{
                "error1":email_address
            })

        # Ensure password matches confirmation
        if password != confirm_password:
            return render(request, 'springrevolution/reset.html',{
                "error2":"Passwords must match."
            })

        # update the password
        u = User.objects.get(email=email_address)
        u.set_password(password)
        u.save()
        return render(request, 'springrevolution/login.html', {
            "success2":"Your password has been successfully updated!"
        })

    else:
        global global_reset_email
        email = global_reset_email
        global_reset_email = None

        return render(request, 'springrevolution/reset.html',{
            "email":email
        })

def add_link(request):
    name = request.POST.get("name")
    url = request.POST.get("url")
    description = request.POST.get("description")
    category = request.POST.get("category")
    date = request.POST.get("date")

    # general way of deciding source
    if 'facebook.com' in url:
        source="facebook"
    elif 'twitter.com' in url:
        source="twitter"
    elif 'instagram.com' in url:
        source="instagram"
    else:
        source="website"

    # checking if the submitted URL is already in the database
    url_list = Link.objects.values_list('url', flat=True)
    if url.strip() in url_list:
        email_status = "1" # fail message
        return HttpResponseRedirect(reverse('index', args=(email_status,)))        

    # if not, send email to the developer
    subject = 'Link Proposal'
    message = ''
    email_from = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    recipient_lists = ["kyawyethumc2022017@gmail.com"]
    html_message = loader.render_to_string('springrevolution/approve.html',{
        "link_proposal":True,
        "name":name,
        "url":url,
        "description":description,
        "category":category,
        "source":source,
        "date":date
    })

    send_mail(subject, message, email_from, recipient_lists, fail_silently=False, html_message=html_message)

    email_status = "2" # success message
    return HttpResponseRedirect(reverse('index', args=(email_status,)))

def approve_link(request):
    name = request.GET.get("name")
    url = request.GET.get("url")
    description = request.GET.get("description")
    category = request.GET.get("category")
    source = request.GET.get("source")
    date = request.GET.get("date")

    # add link into the database
    link = Link(name=name, url=url, description=description, category=category, source=source, date=date)
    link.save()

    return HttpResponseRedirect(reverse('index'))

def request_links(request, buttonid):
    # which button represents which category
    if buttonid == 'button1':
        category = 'CDM'
    elif buttonid == 'button2':
        category = 'CRPH'
    elif buttonid == 'button3':
        category = 'Refugees'
    elif buttonid == 'button4':
        category = 'Revolutionaries'
    elif buttonid == 'button5':
        category = 'Agents'
    elif buttonid == 'button6':
        category = 'Others'
    
    # collect links given category and return as JSON format
    links = Link.objects.filter(category=category)
    links = links.all().order_by(F('source').desc(nulls_first=True), F('date').desc(nulls_first=True), F('name').asc())
    return JsonResponse([link.serialize() for link in links], safe=False)

def report(request):
    nickname = request.POST.get('nickname')
    email = request.POST.get('email')
    message = request.POST.get('message')

    subject = 'Report From User'
    message = f'{nickname} {email} {message}'
    email_from = settings.EMAIL_HOST_USER
    recipient_lists = ["kyawyethumc2022017@gmail.com"]

    send_mail(subject, message, email_from, recipient_lists, fail_silently=False)
    
    email_status = "3" # success message
    return HttpResponseRedirect(reverse('index', args=(email_status,)))

def subscribe(request):
    username = request.user.username
    interval = request.POST.get('interval')

    # the first day user will receive email is (interval) days after the date of user's subscription
    today = date.today()
    receiving_date = today + datetime.timedelta(days=int(interval))
    
    user = User.objects.get(username=username)

    # See if user change subscription or newly subscribe
    already_subscribed = user.subscribe

    # set subscribe, time interval, receiving date given username
    user.subscribe = True
    user.time_interval = interval
    user.receiving_date = receiving_date
    user.save()
    
    # Response differently depending on start subscribing or change
    if already_subscribed is False:
        # send email as soon as the user has subscribed
        mail_service(user.email, username)

        email_status = "4"
        return HttpResponseRedirect(reverse('index', args=(email_status,)))
    else:
        email_status = "5"
        return HttpResponseRedirect(reverse('index', args=(email_status,)))     

def unsubscribe(request):
    username = request.user.username
    user = User.objects.get(username=username)
    user.subscribe = False
    user.time_interval = None
    user.receiving_date = None
    user.save()

    email_status = "6" # unsubscribe message
    return HttpResponseRedirect(reverse('index', args=(email_status,)))

# this function will be triggered only by the admin
def start_mail(request):
    today = date.today()
    users = User.objects.filter(receiving_date=today).values_list('username', 'email')
    
    # sending email to each email address
    for user in users:
        mail_service(user[1], user[0])
    
    # creating a list of recipient usernames
    username_list = []
    for user in users:
        username_list.append(user[0])

    # setting the receiving date of each username into another date according to their time interval
    for user in username_list:
        u = User.objects.get(username=user)
        interval = u.time_interval
        u.receiving_date = today + datetime.timedelta(days=int(interval))
        u.save()

    return HttpResponseRedirect(reverse('index'))

def leave_message(request):
    creator = request.user.username
    text = request.POST.get("message")

    subject = 'Message Proposal'
    message = ''
    email_from = settings.EMAIL_HOST_USER
    recipient_lists = ["kyawyethumc2022017@gmail.com"]
    html_message = loader.render_to_string('springrevolution/approve.html', {
        "message_proposal":True,
        "creator":creator,
        "message":text
    })

    send_mail(subject, message, email_from, recipient_lists, fail_silently=False, html_message=html_message)
    
    email_status = "7" # success message
    return HttpResponseRedirect(reverse('index', args=(email_status,)))
 

def approve_message(request):
    creator = request.GET.get("creator")
    message = request.GET.get("message")

    message = Message(creator=creator, message=message)
    message.save()

    return HttpResponseRedirect(reverse('index'))