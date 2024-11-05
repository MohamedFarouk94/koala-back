from django.utils import timezone


def termiante_follow(follow_instance):
	follow_instance.date_terminated = timezone.now()
	follow_instance.save()
	return follow_instance
