# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render,RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import django

@login_required
def index(request):
    return render_to_response('index.html',{},context_instance=RequestContext(request))


def host_xn(request):

    return render_to_response('xn_host.html')



def acc_login(request):
    if request.method == "POST":

        username = request.POST.get('email')
        print username
        password = request.POST.get('password')
        print("********************")
        print password
        user = auth.authenticate(username=username,password=password)


        if user is not None:
            if user.valid_end_time!=None:

                if django.utils.timezone.now() > user.valid_begin_time\
                        and django.utils.timezone.now()  < user.valid_end_time:
                    auth.login(request,user)
                    request.session.set_expiry(60*30)
                    #print 'session expires at :',request.session.get_expiry_date()
                    return HttpResponseRedirect('/')
                else:
                    return render(request,'login.html',{'login_err': 'User account is expired,please contact your IT guy for this!'})
            else:
                auth.login(request,user)
                request.session.set_expiry(60*30)
                #print 'session expires at :',request.session.get_expiry_date()
                return HttpResponseRedirect('/')
        else:
            return render(request,'login.html',{'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'login.html')




def logout_view(request):
  auth.logout(request)
  # Redirect to a success page.
  return HttpResponseRedirect("/accounts/login/")