from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import F
from django.views import generic

from .models import Question,Choices

# Create your views here.

def index(request):
	question_list = Question.objects.order_by('-pub_date')
	context = {
		'question_list': question_list,
	}
	return render(request,'poll/index.html',context)

def detail(request, question_id):
	question = get_object_or_404(Question,pk=question_id)
	return render(request, 'poll/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'poll/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choices_set.get(pk=request.POST['choice'])
	except (KeyError, Choices.DoesNotExist):
		return render(request, 'poll/detail.html', {
		    'question': question,
		    'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes = F('votes') + 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('results', args=(question.id,)))
