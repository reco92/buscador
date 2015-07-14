from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import pydocumentdb.documents as documents
import pydocumentdb.document_client as document_client


from buscador.models import Info


# Create your views here.

masterKey = 'FbMRtRHcfnfYzMfzrUVZyHnp3LNm1D700epMelXqa4NcvvM6Y10PsuPsxeJdihYl2emm5guyKk49/bV92ZPOpw=='
host = 'https://topicosbd.documents.azure.com:443/'

def index(request):

	infos = "Buscador"
	context = RequestContext(request, {
		'infos': infos,

	})
	#return HttpResponse(template.render(context))
	return render(request, 'buscador/index.html', context)

def buscador(request):
	titulo ="buscador"
	nro_resultados = 100
	#infos = Info.objects.all()


	client = document_client.DocumentClient(host,{'masterKey': masterKey})

	datab = list(client.ReadDatabases({'id' : 'probando'}))

	collections = list(client.ReadCollections(datab[0]['_self']))
	#documents = list(client.ReadDocuments(collections[0]['_self']))
	documents = list(client.QueryDocuments(
    		collections[0]['_self'],
			{
            	'query': 'SELECT * FROM probando i',
			}))

	nro_resultados = len(documents)

	paginator = Paginator(documents, 8) 

	page = request.GET.get('page')
	try:
		documents = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		documents = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		documents = paginator.page(paginator.num_pages)



	context = RequestContext(request, {
		'infos': documents,
		'titulo':titulo,
		'nro_resul' : nro_resultados,
		'consulta' : 'consulta'
	})
	return render(request, 'buscador/buscador.html',context)



def consultar(request):
	titulo ="buscador"
	nro_resultados = 100
	#infos = Info.objects.all()

	if request.method == 'POST':
		consulta = request.POST['frase']

		if(consulta != ""):

			client = document_client.DocumentClient(host,{'masterKey': masterKey})

			datab = list(client.ReadDatabases({'id' : 'probando'}))

			collections = list(client.ReadCollections(datab[0]['_self']))
			#documents = list(client.ReadDocuments(collections[0]['_self']))
			documents = list(client.QueryDocuments(
		    		collections[0]['_self'],
					{
		            	'query': 'SELECT * FROM probando i',
					}))

			nro_resultados = len(documents)

			paginator = Paginator(documents, 8) 

			page = request.GET.get('page')
			try:
				documents = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				documents = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				documents = paginator.page(paginator.num_pages)



			context = RequestContext(request, {
				'infos': documents,
				'titulo':titulo,
				'nro_resul' : nro_resultados,
				'consulta' : consulta,
			})
			return render(request, 'buscador/buscador.html',context)

	return HttpResponseRedirect('/main/')
