from django.shortcuts import render

from account.models import Account

# Create your views here.
def homeScreenView(request):
	context = {}

	accounts = Account.objects.all()

	context['accounts'] = accounts

	return render(request,'personal/home.html',context)



# Create your views here.
def article_view(request):
	return render(request,'personal/article.html')



# Create your views here.
def about_view(request):
	# context = {}

	# accounts = Account.objects.all()

	# context['accounts'] = accounts

	return render(request,'personal/about.html')

# Create your views here.
def contact_view(request):
	# context = {}

	# accounts = Account.objects.all()

	# context['accounts'] = accounts

	return render(request,'personal/contact.html')
