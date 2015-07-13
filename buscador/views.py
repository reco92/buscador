from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from buscador.models import Info


# Create your views here.

def index(request):

	infos = "Hello  world"
	template = loader.get_template('buscador/index.html')
	context = RequestContext(request, {
		'infos': infos,

	})
	#return HttpResponse(template.render(context))
	return render(request, 'buscador/index.html', context)


def buscador(request):
	titulo ="buscador"
	nro_resultados = 100
	infos = Info.objects.all()

	paginator = Paginator(infos, 3) 

	page = request.GET.get('page')
	try:
		infos = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		infos = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		infos = paginator.page(paginator.num_pages)		

	context = RequestContext(request, {
		'infos': infos,
		'titulo':titulo,
		'nro_resul' : nro_resultados,
	})
	return render(request, 'buscador/buscador.html',context)
