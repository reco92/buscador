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

client = document_client.DocumentClient(host,{'masterKey': masterKey})

datab = list(client.ReadDatabases({'id' : 'probando'}))

collections = list(client.ReadCollections(datab[0]['_self']))

frase_busq = ""
paginator = ""
nro_resultados = 100

def index(request):

	infos = "Buscador"
	context = RequestContext(request, {
		'infos': infos,

	})
	#return HttpResponse(template.render(context))
	return render(request, 'buscador/index.html', context)

def consultar(request):
	titulo ="buscador"
	global nro_resultados
	#infos = Info.objects.all()
	global frase_busq
	global paginator

	if request.method == 'POST':
		consulta = request.POST['frase']
		
		if(frase_busq != consulta and consulta != ""):
			frase_busq = consulta
			
			#documents = list(client.ReadDocuments(collections[0]['_self']))
			documentos = list(client.QueryDocuments(
		    		collections[0]['_self'],
					{
		            	'query': 'SELECT * FROM probando i',
					}))

			nro_resultados = len(documentos)

			paginator = Paginator(documentos, 8) 

			page = request.GET.get('page')
			try:
				documentos = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				documentos = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				documentos = paginator.page(paginator.num_pages)



			context = RequestContext(request, {
				'infos': documentos,
				'titulo':titulo,
				'nro_resul' : nro_resultados,
				'consulta' : frase_busq,
			})
			return render(request, 'buscador/buscador.html',context)

	if(frase_busq != ""):		 

		page = request.GET.get('page')
		try:
			documentos = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			documentos = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			documentos = paginator.page(paginator.num_pages)

		context = RequestContext(request, {
			'infos': documentos,
			'titulo':titulo,
			'nro_resul' : nro_resultados,
			'consulta' : frase_busq,
		})
		return render(request, 'buscador/buscador.html',context)

	return HttpResponseRedirect('/main/')

def consultarlink(request,palabra):
	titulo ="buscador"
	global nro_resultados
	#infos = Info.objects.all()
	global frase_busq
	global paginator

	if request.method == 'GET':
		consulta = palabra
		
		if(frase_busq != consulta and consulta != ""):
			frase_busq = consulta
			 
			#documents = list(client.ReadDocuments(collections[0]['_self']))
			documentos = list(client.QueryDocuments(
		    		collections[0]['_self'],
					{
		            	'query': 'SELECT * FROM probando i',
					}))

			nro_resultados = len(documentos)

			paginator = Paginator(documentos, 8) 

			page = request.GET.get('page')
			try:
				documentos = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				documentos = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				documentos = paginator.page(paginator.num_pages)



			context = RequestContext(request, {
				'infos': documentos,
				'titulo':titulo,
				'nro_resul' : nro_resultados,
				'consulta' : frase_busq,
			})
			return render(request, 'buscador/buscador.html',context)

	if(frase_busq != ""):		 

		page = request.GET.get('page')
		try:
			documentos = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			documentos = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			documentos = paginator.page(paginator.num_pages)

		context = RequestContext(request, {
			'infos': documentos,
			'titulo':titulo,
			'nro_resul' : nro_resultados,
			'consulta' : frase_busq,
		})
		return render(request, 'buscador/buscador.html',context)

	return HttpResponseRedirect('/main/')