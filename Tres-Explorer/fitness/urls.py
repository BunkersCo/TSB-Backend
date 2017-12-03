"""fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include

, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include


from django.contrib import admin
from . import views

# added for rest_framework
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from aggregator.models import Studioentry

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Serializers define the API representation.
class StudioentrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Studioentry
        fields = ('name','slug','address')

# ViewSets define the view behavior.
class StudioentryViewSet(viewsets.ModelViewSet):
    queryset = Studioentry.objects.all()
    serializer_class = StudioentrySerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'studios', StudioentryViewSet)

urlpatterns = [
	url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
	url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
	url(r'^home/', 'fitness.views.home', name='home'),
	url('', include('social.apps.django_app.urls', namespace='social')),
	url('', include('django.contrib.auth.urls', namespace='auth')),
	url('', include('aggregator.urls', namespace='aggregator')),

    url(r'^api/', include(router.urls)),

    # for browsable api
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # for clients to obtain a token given the username and password
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),

    # create new user
    # curl -H 'Accept: application/json; indent=4' -u admin:password123 -X POST 'http://127.0.0.1:8000/signup/' --data '{"username":"t12312322", "pwd": "71"}'


    url('^signup/$',views.signup,name='signup'),#ajax sign up
    url('^signin/$',views.signin,name='signin'),#ajax sign in
    # url('^fb-signin/$',views.fb_signin,name='fb_signin'),#ajax sign in

    # url('^post_text/$',views.post_text,name='post_text'),#ajax sign in
    # url('^search_user/$',views.searchUser,name='searchUser'),#ajax sign in
]
