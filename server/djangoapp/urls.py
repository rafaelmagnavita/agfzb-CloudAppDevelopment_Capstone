from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    path(route='about', view=views.about, name='about'),

    path(route='contact', view=views.contact, name='contact'),

    path('registration/', views.registration_request, name='registration'),
    path(route='login', view=views.login_request, name='login'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path(route='index', view=views.get_dealerships, name='index'),
    path(route='', view=views.get_dealerships, name='index'),
    path('admin/', admin.site.urls),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
 + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)