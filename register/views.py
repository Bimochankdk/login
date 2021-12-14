from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


# def index(request):
# 	form = AuthenticationForm(data=request.POST or None)
# 	return render(request, 'registration/login.html', {'form': form })

# def index(request):
# 	return render(request,'register/index.html')


def register(response):
	if response.method == "POST":
		form = RegisterForm(response.POST)
		if form.is_valid():
			form.save()
			return redirect("/")

	else:
		form = RegisterForm()  
	return render(response,'register/register.html',{"form":form})


def show_users(request):
	user = User.objects.all()
	return render(request,'register/index.html',{"user":user})


def login_view(request):
	if request.method == "POST":
		fm = AuthenticationForm(request=request,data=request.POST)
		if fm.is_valid():
			uname = fm.cleaned_data['username']
			upass = fm.cleaned_data['password']
			user= authenticate(username=uname,password= upass)
			if user:
				login(request,user)
				return redirect("/show_users")
			else:
				messages.info(request, "username or password not valid.")
				return redirect("/")
		else:
			messages.info(request, fm.error_messages)
			return redirect("/")
	else:
		fm = AuthenticationForm()
		return render(request,'registration/login.html',{'form':fm})



# def show_users(request):
# 	username = request.POST['username']
# 	print(username)
# 	password = request.POST['password']
# 	user = authenticate(request,username=username,password=password)
# 	if user is not None:
# 		show = User.objects.all()
# 		return render(request, 'register/index.html', {'show':show})
# 	else:
# 		return redirect("/login")
# 	# print('----------------------')
# 	# if request.method == 'POST' and :
# 	# 	show = User.objects.all()
# 	# 	return render(request, 'register/index.html', {'show':show})
# 	# else:
# 	# 	return redirect("/login")
# 	# else:
# 	# 	messages.error(request, 'You need to login first')
		


# def create_user(response):
# 	if response.method == "POST":
# 		form = RegisterForm(response.POST)
# 		if form.is_valid():
# 			form.save()
# 			return redirect("/show_users")

# 	else:
# 		form = RegisterForm()  
	
# 	return render(response,'register/register.html',{"form":form})


def logout_view(request):
	print("??????????????")
	logout(request)
	return redirect("/")


def delete_user(request, pk):
	user = User.objects.all()
	if User.objects.filter(id=pk):
		user_obj = User.objects.get(pk=pk)
		user_obj.delete()
		return redirect("/show_users")
	return render(request,'register/delete.html',{'user': user})

# def search_user(request):
# 	if request.GET.get('searched'):
# 		searched = request.GET.get('searched')
# 		try:
# 			us = User.objects.filter(username__icontains = searched)
# 			return render(request, "register/search.html", {'us':us})
# 		except:
# 			return render(request, "register/search.html", {'us':us})	
# 	else:
# 		return render(request, "register/search.html", {})


from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "register/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					try:
						text_content = "Reset Password"
						template_name = "register/password_reset_email.html"
						subject = "Reset Password"
						from_email = settings.DEFAULT_FROM_EMAIL
						recipients = [user.email]
						html_content = render_to_string(template_name, c)
						email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
						email.attach_alternative(html_content, "text/html")
						email.send()
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="register/password_reset.html", context={"password_reset_form":password_reset_form})