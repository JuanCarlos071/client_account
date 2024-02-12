from django.urls import path
# a module to bring the views
from . import views


# call the view functions by their names
urlpatterns = [
    path("dashboard/", views.pageStart, name='pageStart'),
    # we choose to put name the same as the view function name to make it easy
    # reduce the amount of names
    path("", views.login_view, name='login_view'),
    path("logout/", views.login_view, name='logout_view'),
    path("register/", views.registration_view, name='registration_view'),
    path("edit_password/", views.edit_password, name='edit_password'),
    path("edit_profile/", views.edit_profile, name='edit_profile'),
    path("dashboard/credential_form/", views.credential_form, name='credential_form'),

]