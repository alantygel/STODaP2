from .models import GlobalTag
from urllib import urlopen

def genRDF(class_,start=0, step=0):

	if class_ == 'dataset':
		rdf = urlopen("http://127.0.0.1:8000/" + class_ + "/" + str(start) + "/" + str(step) + "/rdf")
	else:
		rdf = urlopen("http://127.0.0.1:8000/" + class_ + ".rdf")
	rdf = rdf.read()	
	rdf.splitlines()
	rdf_file = open( class_ + "_" + str(start) + '.rdf', 'w')
	rdf_file.write("".join(rdf))
	rdf_file.close()

def genSemGroupRDF():
	gt = GlobalGroup.objects.filter()
	all_rdf = []
	for g in gt:
		rdf = urlopen("http://127.0.0.1:8000/semanticgroup/" + str(g.id) + ".rdf")
		rdf = rdf.read()
		rdf.splitlines()
		all_rdf.append("".join(rdf))

	rdf_file = open('SemGroup.rdf', 'w')
	rdf_file.write("".join(all_rdf))
	rdf_file.close()


