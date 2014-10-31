import logging
import json
from django.http import HttpRequest
from REST import jchem_rest

"""
10-31-14 (np)
Recursively walks n-nested dictionary
in json format and restructures the data to
comply with the jquery flow chart library
used: jit (thejit.org)
"""

def recursive(jsonStr):
	jsonDict = json.loads(jsonStr)
	root = jsonDict['results']
	reDict = {}
	parent = root.keys()[0]
	reDict.update(traverse(root))
	return json.dumps(reDict)


metID = 0 # unique id for each node


def traverse(root):
	global metID
	metID += 1
	newDict ={}

	logging.warning(root.keys())

	if metID == 1:
		parent = root.keys()[0]
		# newDict.update({"id": metID, "name": parent, "data": {}, "children": []})
		# newDict.update({"id": metID, "name": '<img src="http://www.clipartbest.com/cliparts/niB/XxL/niBXxLaoT.png" width="30" height="30">', "data": {}, "children": []})
		newDict.update({"id": metID, "name": imgTemplate(parent), "data": {}, "children": []})
		root = root[parent]
	else:
		# newDict.update({"id": metID, "name": root['smiles'], "data": {}, "children": []})
		# newDict.update({"id": metID, "name": metID, "data": {}, "children": []})
		newDict.update({"id": metID, "name": imgTemplate(root['smiles']), "data": {}, "children": []})
		newDict['data'].update({"degradation": root['degradation']})

	for key, value in root.items():
		if isinstance(value, dict):
			for key2, value2 in root[key].items():
				root2 = root[key][key2]
				if len(root2) > 0: 
					newDict['children'].append(traverse(root2))

	return newDict


"""
Wraps image html tag around
the molecule's image source
"""
def imgTemplate(smiles):
	logging.warning(smiles)

	# 1. Get image from smiles
	post = {"smiles": smiles}
	request = HttpRequest()
	request.POST = post
	results = jchem_rest.smilesToImage(request)

	# 2. Get imageUrl out of results
	data = json.loads(results.content) # json string --> dict
	imageUrl = ''
	imageHeight = 0
	imageWidth = 0
	if 'data' in data:
		root = data['data'][0]['image']
		imageUrl = root['imageUrl']
		imageHeight = root['height']
		imageWidth = root['width'] 

	# 3. Wrap imageUrl with <img>
	html = """
	<img class="metabolite" alt="chemical" src="
	"""
	html += imageUrl
	html += '" height="' + str(imageHeight) + '"'
	html += 'width="' + str(imageWidth) + '"'
	html += """
	"></div>
	"""
	return html
