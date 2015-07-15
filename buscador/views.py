from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


import pydocumentdb.documents as documents
import pydocumentdb.document_client as document_client


from buscador.models import Info


# Create your views here.

masterKey = 'FbMRtRHcfnfYzMfzrUVZyHnp3LNm1D700epMelXqa4NcvvM6Y10PsuPsxeJdihYl2emm5guyKk49/bV92ZPOpw=='
host = 'https://topicosbd.documents.azure.com:443/'

client = document_client.DocumentClient(host,{'masterKey': masterKey})

datab = list(client.ReadDatabases({'id' : 'internacional'}))

collections = list(client.ReadCollections(datab[1]['_self']))

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
		            	'query': 'SELECT i.tag, i.titulo  FROM internacional i',
					}))

			print len(documentos)

			array = []
			array.append(frase_busq)
			for i in documentos:
				palabra = i['titulo']

				tags = ''
				for t in i['tag']:
					tags += ' ' + t

				palabra = palabra + tags
				array.append(palabra)



			tfidf_vectorizer = TfidfVectorizer()
			tfidf_matrix_train = tfidf_vectorizer.fit_transform(array)  #finds the tfidf score with normalization
			resultado = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)  #here the first element of tfidf_matrix_train is matched with other three elements
			ntotal = len(resultado[0])

			#print resultado

			i = 1
			grupo = {}
			while i < ntotal:
				if resultado[0][i] > 0:
					grupo[ resultado[0][i] ] = documentos[i-1]
				i = i + 1

			listado = grupo.items()
			listado.sort(reverse=True)
			documentos = []
			for par in listado:
				documentos.append(par[1])

			nro_resultados = len(documentos)

			print nro_resultados

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
		            	'query': 'SELECT * FROM internacional i',
					}))

			array = []
			array.append(frase_busq)
			for i in documentos:
				array.append(i['titulo'])

			print array

			tfidf_vectorizer = TfidfVectorizer()
			tfidf_matrix_train = tfidf_vectorizer.fit_transform(array)  #finds the tfidf score with normalization
			print "cosine scores ==> ",cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)  #here the first element of tfidf_matrix_train is matched with other three elements

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