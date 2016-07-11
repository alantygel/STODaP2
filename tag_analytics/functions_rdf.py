from .models import GlobalTag, Dataset
from urllib import urlopen

def genRDF(class_,start=0, step=10000):

	if class_ == 'dataset' or class_ == 'tag':
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

def cleanStr():
	d = Dataset.objects.filter(id__gt = 439910)
	for dd in d:
		if type(dd.description) != type(None):
			dd.description = dd.description.replace('\x01','')
			dd.description = dd.description.replace('\x0b','')
			dd.description = dd.description.replace('\x0d','')
			dd.description = dd.description.replace('\x04','')
			dd.description = dd.description.replace('\x10','')
			dd.description = dd.description.replace('\x13','')
			dd.description = dd.description.replace('\x16','')
			dd.description = dd.description.replace('\x17','')
			dd.description = dd.description.replace('\x1d','')
		if type(dd.display_name) != type(None):
			dd.display_name = dd.display_name.replace('\x01','')
			dd.display_name = dd.display_name.replace('\x0b','')
			dd.display_name = dd.display_name.replace('\x0d','')
			dd.display_name = dd.display_name.replace('\x04','')
			dd.display_name = dd.display_name.replace('\x10','')
			dd.display_name = dd.display_name.replace('\x13','')
			dd.display_name = dd.display_name.replace('\x16','')
			dd.display_name = dd.display_name.replace('\x17','')
			dd.display_name = dd.display_name.replace('\x1d','')
      		dd.save()
		
# x01, x02, x0c
