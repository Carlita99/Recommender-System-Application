from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^movies/mostRecent[/]?$', views.getMostRecentMovies, name='mostRecentMovies'),
    url(r'^movies/mostPopular[/]?$', views.getMostPopularMovies, name='mostPopularMovies'),
    url(r'^user/guest/signup[/]?$', views.signup, name='signup'),
    url(r'^user/guest/login[/]?$', views.login, name='login'),
    url(r'^user/guest/refreshToken[/]?$', views.refreshToken, name='refreshToken'),
    url(r'^user/guest/editProfile[/]?$', views.editProfile, name='editProfile'),
    url(r'^user/guest/logout[/]?$', views.logout, name='logout'),
]
