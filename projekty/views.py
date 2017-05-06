from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from projekty.forms import MakeProfile



#@login_required(login_url='/login')
def main(request):
  return render(request, 'main.html')


def register(request):
  if request.method == 'POST':
    form = MakeProfile(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      new_user = User.objects.create_user(data['username'], data['email'], data['password'],
        first_name = data['meno'], last_name = data['priezvisko'])
      login(request, new_user)
      return HttpResponseRedirect('/main')
  else :
    form = MakeProfile()
  return render(request, 'register.html', {'form':form})
