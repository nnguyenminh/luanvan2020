from django.shortcuts import render

# Create your views here.


def articleView(request):

	return render(request, 'article/article.html')