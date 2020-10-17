from django.shortcuts import render
from personal.models import Question

# Create your views here.
def homeScreenView(request):
	
	context = {}
	questions = Question.objects.all()
	context['questions'] = questions

	return render(request,'personal/home.html',context)