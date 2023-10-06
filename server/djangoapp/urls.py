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

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),
    path(route='about', view=views.about, name='about'),
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoap/urls.py')),
    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)