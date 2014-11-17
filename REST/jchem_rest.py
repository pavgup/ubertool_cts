"""
Access to jchem web services
(np)
"""

import requests
import json
import logging
import views.misc
from django.http import HttpResponse
from django.http import HttpRequest
from xml.sax.saxutils import escape
import datetime
import pytz


headers = {'Content-Type' : 'application/json'}


class Urls:

	jchemBase = 'http://pnnl.cloudapp.net/webservices' # old ws location 
	efsBase = 'http://pnnl.cloudapp.net/efsws' # metabolizer base
	# base = 'http://134.67.114.2/webservices'
	# base = 'http://134.67.114.2/efsws/rest' # antiquated, but functioning, WS

	# jchem ws urls:
	exportUrl = '/rest-v0/util/calculate/molExport'
	detailUrl = '/rest-v0/util/detail'
	# standardizerUrl = '/rest-v0/util/convert/standardizer'

	metabolizerUrl = '/rest/metabolizer'
	standardizerUrl = '/rest/standardizer'


def doc(request):
	"""
	API Documentation Page
	"""

	text_file2 = open('REST/doc_text.txt','r')

	xx = text_file2.read()

	response = HttpResponse()
	response.write(xx)

	return response


def getChemDeats(request):
	"""
	getChemDeats

	Inputs:
	chem - chemical name (format: iupac, smiles, or formula)
	Returns:
	The iupac, formula, mass, and smiles string of the chemical
	along with the mrv of the chemical (to display in marvinjs)
	"""

	queryDict = request.POST
	chem = queryDict.get('chemical') # chemical name
	ds = Data_Structures()
	data = ds.chemDeatsStruct(chem) # format request to jchem
	data = json.dumps(data) # convert dict to json string
	url = Urls.jchemBase + Urls.detailUrl
	return web_call(url, request, data)


def smilesToImage(request):
	"""
	smilesToImage

	Returns image (.png) url for a 
	given SMILES
	"""

	smiles = request.POST.get('smiles')
	imageWidth = request.POST.get('width')
	imageHeight = request.POST.get('height')
	request = {
		"structures": [
			{"structure": smiles}
		],
		"display": {
			"include": ["image"],
			"parameters": {
				"image": {
					"width": imageWidth,
					"height": imageHeight
				}
			}
		}
	}
	data = json.dumps(request) # to json string
	url = Urls.jchemBase + Urls.detailUrl
	imgData = web_call(url, request, data) # get response from jchem ws
	return imgData # return dict of image data


def mrvToSmiles(request):
	"""
	mrvToSmiles

	Gets SMILES string for chemical drawn
	in Marvin Sketch. Also calls getChemDeats
	to get chemical info (should probably not 
	tie these together)
	"""

	queryDict = request.POST
	chemStruct = queryDict.get('chemical') # chemical in <cml> format (marvin sketch)
	request = {
		"structure" : chemStruct,
		"inputFormat" : "mrv",
		"parameters" : "smiles"
	}
	data = json.dumps(request) # serialize to json-formatted str
	url = Urls.jchemBase + Urls.exportUrl
	smilesData = web_call(url, request, data) # get responset))
	return smilesData
	# data = json.loads(smilesData.content)
	# request = HttpRequest()
	# request.POST = { "chemical": data['structure'] }
	# return getChemDeats(request) # return smiles along with other info


def getChemSpecData(request):
	"""
	getChemSpecData

	Gets pKa values and microspecies distribution
	for a given chemical

	Inputs - data types to get (e.g., pka, tautomer, etc.),
	and all the fields from the 3 tables.
	"""

	ds = Data_Structures()
	data = ds.chemSpecStruct(request.POST) # format request to jchem
	data = json.dumps(data)
	url = Urls.jchemBase + Urls.detailUrl
	results = web_call(url, request, data)
	return results


def getTransProducts(request):
	"""
	Makes request to metabolizer on pnnl server
	"""

	url = Urls.efsBase + Urls.metabolizerUrl
	data = json.dumps(request.POST)
	results = web_call(url, request, data)
	return results


def standardizer(request):
	"""
	Standardizes a structure in any format 
	recognized by Marvin, and the actions to
	perfrom on the structure (e.g., aromatize, daromatize,
	clear stereo, tautomerize, add explicit H, remove
	explicit H, transform, and neutralize). 
	*Currently just uses aromatize by default.*

	Returns molecule in mrv format
	"""
	url = Urls.efsBase + Urls.standardizerUrl
	structure = request.POST.get('chemical')

	# logging.warning(structure)
	# data = json.dumps({"structure": structure})
	data = {
		"structure": structure,
		"actions": [
			"aromatize"
		]
	}
	data = json.dumps(data)
	results = web_call(url, request, data)
	# logging.warning(results.content)
	return results


def web_call(url, request, data):
	"""
	Makes the request to a specified URL
	and POST data. Returns an http response.
	"""

	callback_response = HttpResponse()
	message = '\n' + "URL: " + '\n' + url + '\n\n'
	message = message + "POST Data: " + '\n' + str(data) + '\n\n'
	try:
		# logging.warning("trying to get response...")
		response = requests.post(url, data=data, headers=headers, timeout=60)
		# logging.warning("success.")
		message = message + "Response: " + '\n' + response.content + '\n\n'
		callback_response.write(response.content)
		return callback_response
	except:
		logging.warning("Error in web call")
		callback_response.write(message)
		return callback_response


class Data_Structures:

	def chemDeatsStruct(self, chemical):
		# return json data for chemical details
		chemDeatsDict =  {
			"structures": [
				{ "structure": chemical }
			],
			"display": {
				"include": [
					"structureData"
				],
				"additionalFields": {
					"formula": "chemicalTerms(formula)",
					"iupac": "chemicalTerms(name)",
					"mass": "chemicalTerms(mass)",
					"smiles": "chemicalTerms(molString('smiles'))"
				},
				"parameters": {
					"structureData": "mrv"
				}
			}
		}
		return chemDeatsDict


	def chemSpecStruct(self, dic):

		# don't forget about pKa_decimal

		keys = ["isoelectricPoint", "pKa", "majorMicrospecies", "stereoisomer", "tautomerization"]

		structures = []
		if 'chem_struct' in dic:
			structures = [ { "structure": dic["chem_struct"] } ]

		includeList = []
		paramsDict = {} # dict of dict where latter dict has key of param and vals of param vals

		for key, value in dic.items():
			if key in keys:
				includeList.append(key) # add parameter to "include" list
				paramsDict.update({key: value})

		display = {"include": includeList, "parameters": paramsDict}
		dataDict = {"structures": structures, "display": display}

		return dataDict


def gen_jid():
    ts = datetime.datetime.now(pytz.UTC)
    localDatetime = ts.astimezone(pytz.timezone('US/Eastern'))
    jid = localDatetime.strftime('%Y%m%d%H%M%S%f')
    return jid