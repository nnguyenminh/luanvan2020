from django.shortcuts import render

# Create your views here.

context = {}

def blogView(request):

	context['blog'] = 'blog'

	return render(request, 'blog/blog.html', context)