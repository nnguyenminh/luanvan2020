from django.shortcuts import render

# Create your views here.


def homeView(request):

	return render(request, 'techBlog/home.html')



def articleView(request):

	return render(request, 'techBlog/article.html')



def blogView(request):

	return render(request, 'techBlog/blog.html')



def contactView(request):

	return render(request, 'techBlog/contact.html')






