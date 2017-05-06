import datetime
from itertools import chain
from django.shortcuts import render
from database.models import Project, Document
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from database.forms import ZmenProjekt, PridajDokument



@login_required(login_url='login')
def database(request):
	projects = Project.objects.all()
	return render(request, 'database/dtb.html', {'database': projects})

@login_required(login_url='login')
def projekty(request, id_input):
  project = Project.objects.get(id=id_input)
  if request.method == 'POST':
    dokument = PridajDokument(request.POST, request.FILES)
    if dokument.is_valid():
      subor = Document(dokument = request.FILES['projekt'])
      subor.save()
      project.document = subor
      project.save()
      subor.save()
  else:
    dokument = PridajDokument()
  return render(request, 'database/project.html', {'project': project, 'user':request.user, 'dokument': dokument})

@login_required(login_url='login')
def sortby(request, attr):
  if attr == "id":
    projects = Project.objects.order_by("id")
  elif attr == "nid":
    projects = Project.objects.order_by("-id")
  elif attr == "nazov":
    projects = Project.objects.order_by("title")
  elif attr == "nnazov":
    projects = Project.objects.order_by("-title")
  elif attr == "rok":
    projects = Project.objects.order_by("-registration_date")
  elif attr == "nrok":
    projects = Project.objects.order_by("registration_date")
  else:
    raise Http404("Spôsob zoradenia neexistuje")
  return render(request, 'database/dtb.html', {'database': projects})


@login_required(login_url='login')
def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        projects = Project.objects.filter(title__icontains=q)
    else:
        projects = None
    return render(request, 'database/dtb.html', {'database': projects})

@login_required(login_url='login')
def my_projects(request):
  user = request.user
  auth_projects = user.projects.all().order_by("-registration_date")
  cons_projects = Project.objects.filter(consultant = user).order_by("-registration_date")
  return render(request, 'database/my_dtb.html', {'konzultovane': cons_projects, 'napisane': auth_projects})

@login_required(login_url='login')
def new_project(request):
  if request.method == 'POST':
    form = ZmenProjekt(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      autori = []
      try:
        autori.append(User.objects.get(username = data['autor1']))
        autori.append(User.objects.get(username = data['autor2']))
        autori.append(User.objects.get(username = data['autor3']))
      except User.DoesNotExist:
        pass

      projekt = Project()
      projekt.save()
      projekt.title = data['nazov']
      projekt.consultant = User.objects.get(username = data['konzultant'])
      projekt.description = data['popis']
      projekt.authors = autori
      projekt.save()
      return HttpResponseRedirect('/database/projekty/' + str(projekt.id))
  else :
    form = ZmenProjekt(initial={'autor1':request.user.username})
  return render(request, 'database/zmenit_projekt.html', {'form':form, 'nazov':'Vytvoriť projekt', 'tlacidlo':'Vytvor!'})


@login_required(login_url='login')
def zmen_projekt(request, id_input):
  projekt = Project.objects.get(pk=id_input)
  if projekt not in request.user.projects.all():
    raise Http404("Meniť projeky smú len ich autori")
  if request.method == 'POST':
    form = ZmenProjekt(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      autori = []
      try:
        autori.append(User.objects.get(username = data['autor1']))
        autori.append(User.objects.get(username = data['autor2']))
        autori.append(User.objects.get(username = data['autor3']))
      except User.DoesNotExist:
        pass

      projekt.title = data['nazov']
      projekt.consultant = User.objects.get(username = data['konzultant'])
      projekt.authors = autori
      projekt.description = data['popis']
      projekt.save()
      return HttpResponseRedirect('/database/projekty/' + str(projekt.id))

  else:
    autori_obj = projekt.authors.all()
    pocet_autorov = projekt.authors.count()
    autori = []
    for autor in autori_obj:
      autori.append(autor.username)
    for i in range(pocet_autorov,3):
      autori.append(None)
    popis = projekt.description
    form = ZmenProjekt(initial = {'nazov':projekt.title, 'konzultant':projekt.consultant, 'popis':popis,
     'oponent':projekt.oponent, 'autor1':autori[0], 'autor2':autori[1], 'autor3':autori[2]})
  return render(request, 'database/zmenit_projekt.html', {'form':form, 'nazov':'Upraviť projekt', 'tlacidlo':'Uprav!'})

@login_required(login_url='login')
def projekt_download(request, id_input):
  projekt = Project.objects.get(pk=id_input)

