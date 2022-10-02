from django.shortcuts import render,redirect
from .models import Contact,User
import random
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def index(request):
	return render(request,'index.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			remarks=request.POST['remarks'])
		msg="Contact Saved Successfully"
		contacts=Contact.objects.all().order_by('-id')[:5]
		return render(request,'contact.html',{'msg':msg, 'contacts':contacts})
	elif request.method=="GET":
		contacts=Contact.objects.all().order_by('-id')[:5]
		return render(request,'contact.html',{'contacts':contacts})
	else:
		return render(request,'contact.html',{'msg': "Sorry, Your request cann't match."})

def signup(request): 
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg' :msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					gender=request.POST['gender'],
					password=request.POST['password'],
					profile_pic=request.FILES['profile_pic']
					)
				msg="User Sign up Successfully"
				return render(request,'login.html',{'msg style="color:green;': msg})
			else:
				msg="Password and confirm password does not matched"
				return render(request,'signup.html',{'msg': msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(
				email=request.POST['email'],
				password=request.POST['password']
				)
			request.session['email']=user.email
			request.session['fname']=user.fname
			request.session['profile_pic']=user.profile_pic.url
			return render(request,'index.html')
		except:
			msg="Email or password is incorrect"
			return render(request,'login.html',{'msg' :msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New password and Confirm new password does not matched"
				return render(request,'change_password.html',{'msg' :msg})
		else:
			msg="Old password is incorrect"
			return render(request,'change_password.html',{'msg' :msg})
	else:
		return render(request,'change_password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject = 'OTP for forgot password'
			message = 'Hello, '+user.fname+" Your OTP For Fogot Password Is "+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'otp.html',{'otp':otp,'email':user.email})
		except:
			msg="Email not Registered"
			return render(request,'forgot_password.html',{'msg': msg})

	else:
		return render(request,'forgot_password.html')

def verify_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	email=request.POST['email']

	if otp==uotp:
		return render(request,'new_password.html',{'email':email})
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'otp':otp,'email':email,'msg':msg})

def new_password(request):
	email=request.POST['email']
	p=request.POST['new_password']
	cp=request.POST['cnew_password']

	if p==cp:
		user=User.objects.get(email=email)
		user.password=p
		user.save()
		return redirect('login')
	else:
		msg="Password and confirm password does not matched"
		return render(request,'new_password.html',{'email':email,'msg':msg})

def profile(request):
	user=User.objects.get(email=request.session['email'])

	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		user.gender=request.POST['gender']
		try:
			user.profile_pic=request.FILES['profile_pic']

		except:
			pass
		user.save()
		request.session['profile_pic']=user.profile_pic.url
		return render(request,'profile.html',{'user':user})

	else:	
		return render(request,'profile.html',{'user':user})