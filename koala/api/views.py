from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from database.models import Profile, Question, Follow
from database.creators import create_question, create_answer, create_follow
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


@api_view(['GET'])
def hello_world(request, **kwargs):
	return Response({'details': 'hello world'})


@api_view(['GET'])
def get_profile(request, **kwargs):
	try:
		profile = Profile.objects.get(user__username=kwargs['username'])
		return Response(profile.to_dict())
	except ObjectDoesNotExist:
		return HttpResponseNotFound('{"details": "User not found."}')


@api_view(['GET'])
def get_answers(request, **kwargs):
	try:
		profile = Profile.objects.get(user__username=kwargs['username'])
		answers = profile.get_answers(kwargs['page'])
		return Response([answer.to_dict() for answer in answers])
	except ObjectDoesNotExist:
		return HttpResponseNotFound('{"details": "User not found."}')


@api_view(['GET'])
def login(request, **kwargs):
	try:
		username, password = request.data['username'], request.data['password']
		profile = Profile.objects.get(user__username=username)
		assert profile.user.check_password(password)
		return Response({'token': f'Token {Token.objects.get_or_create(user=profile.user)[0].key}'})
	except KeyError:
		return HttpResponseBadRequest('{"details": "Not valid request."}')
	except ObjectDoesNotExist:
		return HttpResponseNotFound('{"details": "User not found."}')
	except AssertionError:
		return HttpResponse('{"details": "Password is not correct."}', status=401)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def handshake(request, **kwargs):
	return Response({'username': request.user.username})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_my_questions(request, **kwargs):
	profile = Profile.objects.get(user=request.user)
	questions = profile.get_unanswered_questions(kwargs['page'])
	return Response([question.to_dict() for question in questions])


@api_view(['POST'])
def ask_unauth(request, **kwargs):
	try:
		to_x = Profile.objects.get(user__username=kwargs['username'])
		question = create_question(to_x, request.data['text'])
		return Response(question.to_dict())
	except KeyError:
		return HttpResponseBadRequest('{"details": "Not valid request."}')
	except ObjectDoesNotExist:
		return HttpResponseNotFound('{"details": "User not found."}')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ask_auth(request, **kwargs):
	try:
		to_x = Profile.objects.get(user__username=kwargs['username'])
		text = request.data['text']
		from_x = Profile.objects.get(user=request.user)
		is_anon = request.data['is_anon']
		question = create_question(
			to_x,
			text,
			from_x=from_x,
			is_anon=is_anon)
		return Response(question.to_dict())
	except KeyError:
		return HttpResponseBadRequest('{"details": "Not valid request."}')
	except ObjectDoesNotExist:
		return HttpResponseNotFound('{"details": "User not found."}')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def answer(request, **kwargs):
	try:
		question = Question.objects.get(id=kwargs['qid'])
		assert question.to_x.user == request.user
		text = request.data['text']
		answer = create_answer(question, text)
		return Response(answer.to_dict())
	except KeyError:
		return HttpResponseBadRequest('{"details": "Not valid request."}')
	except ObjectDoesNotExist:
		return HttpResponseNotFound('{"details": "Question not found."}')
	except AssertionError:
		return HttpResponse('{"details": "You are not authorized to answer this question."}', status=403)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def follow(request, **kwargs):
	try:
		following = Profile.objects.get(user__username=kwargs['username'])
		follower = Profile.objects.get(user=request.user)
		assert not Follow.objects.filter(follower=follower, following=following, date_terminated__isnull=True).exists()
		follow_instance = create_follow(follower, following)
		return Response(follow_instance.to_dict())
	except KeyError:
		return HttpResponseBadRequest('{"details": "Not valid request."}')
	except ObjectDoesNotExist:
		return HttpResponseNotFound('{"details": "User not found."}')
	except AssertionError:
		return HttpResponse('{"details": "Following instance already exists."}', status=409)
