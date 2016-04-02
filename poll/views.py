from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import F
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Question,Choices,Voted

# Create your views here.

def login(request):
	if request.method=='POST':
		user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
	else:
		return render(request,'poll/login.html')
	if user is not None and user.is_active:
		auth.login(request, user)
		return HttpResponseRedirect(reverse('index'))
	else:
		return render(request,'poll/login.html',{'error_message': 'Invalid user/password'})

def index(request):
	if request.user.is_authenticated():
		question_list = Question.objects.order_by('-pub_date')
		context = {
			'question_list': question_list,
			'user': request.user
		}
		return render(request,'poll/index.html',context)
	else:
		return HttpResponseRedirect(reverse('login'))

def detail(request, question_id):
	if request.user.is_authenticated():
		question = get_object_or_404(Question,pk=question_id)
		try:
			voted = Voted.objects.get(user_id=request.user.pk,question_id=question_id)
		except (KeyError, Voted.DoesNotExist):
			return render(request, 'poll/detail.html', {'question': question, 'user': request.user})
		else:
			return HttpResponseRedirect(reverse('results', args=(question.id,)))
	else:
		return HttpResponseRedirect(reverse('login'))

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'poll/results.html', {'question': question, 'user': request.user})

def vote(request, question_id):
	if request.user.is_authenticated():
		question = get_object_or_404(Question, pk=question_id)
		try:
			selected_choice = question.choices_set.get(pk=request.POST['choice'])
		except (KeyError, Choices.DoesNotExist):
			return render(request, 'poll/detail.html', {
			    'question': question,
			    'error_message': "You didn't select a choice.",
			    'user': request.user
			})
		else:
			selected_choice.votes = F('votes') + 1
			selected_choice.save()
			vote = Voted(user_id=request.user.pk, question_id=question_id)
			vote.save()
			return HttpResponseRedirect(reverse('results', args=(question.id,)))
	else:
		return HttpResponseRedirect(reverse('login'))

def ques(request, question_id = None):
	if request.user.is_authenticated():
		if request.method=='POST':
			if question_id:
				question = get_object_or_404(Question, pk=question_id, user=request.user.pk)
			else:
				question = Question()
			question.question_text = request.POST['question_text']
			question.user_id = request.user.pk
			question.save()
			try:
				choices = Choices.objects.filter(question_id=question.id)
			except (KeyError, Choices.DoesNotExist):
				pass
			else:
				choices.delete()
			for c in request.POST.getlist('choice[]'):
				choice = Choices(question_id=question.id, choice_text=c)
				choice.save()
			return HttpResponseRedirect(reverse('index'))
		if question_id:
			question = get_object_or_404(Question, pk=question_id, user=request.user.pk)
			return render(request, 'poll/ques.html', {'question': question, 'choices': question.choices_set.all(), 'user': request.user})
		else:
			return render(request, 'poll/ques.html', {'choices': [Choices()]*2, 'user': request.user})
	else:
		return HttpResponseRedirect(reverse('login'))

def signup(request):
	if request.method=='POST':
		if request.POST['password']==request.POST['repeat']:
			try:
				User.objects.get(username=request.POST['username'])
			except (KeyError, User.DoesNotExist):
				user = User.objects.create_user(
					username=request.POST['username'],
					email=request.POST['email'],
					password=request.POST['password']
				)
				user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
				auth.login(request,user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return render(request, 'poll/signup.html', {'error_message': 'Username already registered'})
		else:
			return render(request, 'poll/signup.html', {'error_message': 'Passwords do not match'})
	return render(request, 'poll/signup.html')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('login'))
