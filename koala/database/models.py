from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	# The following commented attributes are in 'user'
	# username (Primary Key)
	# first_name
	# last_name
	# email
	# password
	# date_joined
	# last_login
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=300, blank=True)
	gender = models.CharField(max_length=7, choices=[(x, x) for x in ['Male', 'Female', 'Other']])
	birthdate = models.DateField()

	def _get_all_unsnwered_questions(self):
		return [q for q in Question.objects.filter(to_x=self) if not q.is_answered()]

	def _get_all_answers(self):
		return Answer.objects.filter(question__to_x=self)

	def get_unanswered_questions(self, page):
		page = max(page, 1)
		return Question.objects.filter(to_=self, is_answered=False)[::-1][20 * (page - 1): 20 * page + 1]

	def get_answers(self, page):
		page = max(page, 1)
		return Answer.objects.filter(question__to_=self)[::-1][20 * (page - 1): 20 * page + 1]

	def get_n_unanswered_questions(self):
		return len(self._get_all_unsnwered_questions())

	def get_n_answers(self):
		return len(self._get_all_answers())

	def to_dict(self):
		return {
			'username': self.user.username,
			'first_name': self.user.first_name,
			'last_name': self.user.last_name,
			'email': self.user.email,
			'date_joined': self.user.date_joined,
			'last_login': self.user.last_login,
			'bio': self.bio,
			'gender': self.gender,
			'birthdate': self.birthdate,
			'n_answers': self.get_n_answers(),
			'n_unanswered_questions': self.get_n_unanswered_questions(),
		}


class Question(models.Model):
	id = models.BigAutoField(primary_key=True)
	from_x = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='questions_from')
	to_x = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions_to')
	text = models.CharField(max_length=600)
	is_anon = models.BooleanField(default=True)
	is_private = models.BooleanField(default=False)
	date_asked = models.DateTimeField(auto_now_add=True)

	def is_answered(self):
		try:
			self.answer
			return True
		except Answer.DoesNotExist:
			return False

	def get_answer(self):
		try:
			return self.answer
		except Answer.DoesNotExist:
			return ''

	def to_dict(self):
		return {
			'from': self.from_x.user.username if not self.is_anon else '?',
			'to': self.to_x.user.username,
			'text': self.text,
			'date_asked': self.date_asked,
			'is_answered': self.is_answered(),
			'is_private': self.is_private,
			'answer': self.get_answer().text if self.is_answered() else '',
			'date_answered': self.get_answer().date_answered if self.is_answered() else '',
		}


class Answer(models.Model):
	id = models.BigAutoField(primary_key=True)
	question = models.OneToOneField(Question, on_delete=models.CASCADE)
	text = models.TextField()
	date_answered = models.DateTimeField(auto_now_add=True)

	def to_dict(self):
		return {
			'asker': self.question.from_x.user.username if not self.question.is_anon else '?',
			'answerer': self.question.to_.user.username,
			'is_private': self.question.is_private,
			'question': self.question.text,
			'answer': self.text,
			'date_asked': self.question.date_asked,
			'date_answered': self.date_answered
		}
