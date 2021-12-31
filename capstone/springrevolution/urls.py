from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("index/<str:email_status>", views.index, name="index"),
    path("pages/<str:page>", views.show_page, name="show_page"),
    path("register", views.register, name="register"),
    path("confirm", views.confirm_registration, name="confirm_registration"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("reset", views.reset_password, name="reset_password"),
    path("add_link", views.add_link, name="add_link"),
    path("approve_link", views.approve_link, name="approve_link"),
    path("request_links/<str:buttonid>", views.request_links, name="request_links"),
    path("report", views.report, name="report"),
    path("subscribe", views.subscribe, name="subscribe"),
    path("unsubscribe", views.unsubscribe, name="unsubscribe"),
    path("start_mail", views.start_mail, name="start_mail"),
    path("leave_message", views.leave_message, name="leave_message"),
    path("approve_message", views.approve_message, name="approve_message")
]
