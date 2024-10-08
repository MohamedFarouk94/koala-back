from django.db import models
from django.contrib.auth.models import User


class Profile:
	# user containing:
	# username, first_name, last_name, email, password, date_joined, last_login
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=300, blank=True)

	def get_unanswered_questions(self):
		pass

	def get_answers(self):
		pass

	def get_n_unanswered_questions(self):
		pass

	def get_n_answers(self):
		pass

	def to_dict(self):
		return {
			'username': self.user.username,
			'first_name': self.user.first_name,
			'last_name': self.user.last_name,
			'email': self.user.email,
			'date_joined': self.user.date_joined,
			'last_login': self.user.last_login,
			'bio': self.bio,
			'n_answers': self.get_n_answers(),
			'n_unanswered_questions': self.get_n_unanswered_questions()
		}


class Question:
	id = models.BigAutoField(primary_key=True)
	from_ = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	to_ = models.ForeignKey(Profile, on_delete=models.CASCADE)
	text = models.CharField(max_length=600)
	is_anon = models.BooleanField(default=False)
	is_private = models.BigAutoField(default=False)
	date_asked = models.DateTimeField(auto_now_add=True)

	def is_answered(self):
		pass

	def get_answer(self):
		pass

	def to_dict(self):
		return {
			'from': self.from_.user.username if not self.is_anon else '?',
			'to': self.to_.user.username,
			'text': self.text,
			'date_asked': self.date_asked,
			'is_answered': self.is_answered(),
			'is_private': self.is_private,
			'answer': self.get_answer().text if self.is_answered() else '',
			'date_answered': self.get_answer().date_answered if self.is_answered() else '',
		}


class Answer:
	id = models.BigAutoField(primary_key=True)
	question = models.OneToOneField(Question, on_delete=models.CASCADE)
	text = models.TextField()
	date_answered = models.DateTimeField(auto_now_add=True)

	def to_dict(self):
		return {
			'asker': self.question.from_.user.username if self.question.is_anon else '?',
			'answerer': self.question.to_.user.username,
			'is_private': self.question.is_private,
			'question': self.question.text,
			'answer': self.text,
			'date_asked': self.question.date_asked,
			'date_answered': self.date_answered
		}
