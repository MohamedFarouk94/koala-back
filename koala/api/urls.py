from django.urls import path
from . import views


urlpatterns = [
	path('', views.hello_world, name='hello_world'),
	path('login', views.login, name='login'),
	path('handshake', views.handshake, name='handshake'),
	path('profile/<str:username>/answers/<int:page>', views.get_answers, name='answers'),
	path('profile/<str:username>', views.get_profile, name='profile'),
	path('my-questions/<int:page>', views.get_my_questions, name='my_questions'),
	path('profile/<str:username>/ask-unauth', views.ask_unauth, name='ask_unauth'),
	path('profile/<str:username>/ask-auth', views.ask_auth, name='ask_auth'),
	path('question/<int:qid>/answer', views.answer, name='answer'),
	path('profile/<str:username>/follow', views.follow, name='follow'),
	path('profile/<str:username>/unfollow', views.unfollow, name='unfollow'),
]
