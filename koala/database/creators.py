from .models import Profile, Question, Answer
from django.contrib.auth.models import User
from datetime import datetime


def create_profile(username, password, gender, birthdate, bio=''):
	user = User.objects.create_user(
		username=username,
		password=password)

	return Profile.objects.create(
		user=user,
		gender=gender,
		birthdate=datetime.strptime(birthdate, '%d/%m/%Y'))


def create_question(to_x, text, from_x=None, is_anon=True, is_private=False):
	if is_anon:
		from_x = None
	elif not from_x:
		raise ValueError

	return Question.objects.create(
		to_x=to_x,
		from_x=from_x,
		text=text,
		is_anon=is_anon,
		is_private=is_private)


def create_answer(question, text):
	return Answer.objects.create(
		question=question,
		text=text)
