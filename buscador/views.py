from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.

def index(request):
	infos = "Hello  world"
	template = loader.get_template('buscador/index.html')
	context = RequestContext(request, {
		'infos': infos,
	})
	#return HttpResponse(template.render(context))
	return render(request, 'buscador/index.html', context)
