from django.urls import path
# a module to bring the views
from . import views


# call the view functions by their names
urlpatterns = [
    path("dashboard/", views.pageStart, name='pageStart'),
    # we choose to put name the same as the view function name to make it easy
    # reduce the amount of names
    path("", views.login_view, name='login_view'),
    path("register/", views.registration_view, name='registration_view'),


]

handler404 = 'client_account.views.error_404'
handler500 = 'client_account.views.error_500'