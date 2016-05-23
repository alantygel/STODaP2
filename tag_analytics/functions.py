from .models import LoadRound
from .models import Tag
from .models import GlobalTag
from .models import TagTranslation
from .models import TagMeaning
from .models import Coocurrence
from .models import Group
from .models import GlobalGroup
from .models import Dataset
from .models import OpenDataPortal

import numpy
from sklearn.metrics.pairwise import cosine_similarity
from unidecode import unidecode
import Levenshtein
import pycountry
import urllib
import json
import lib
import rdflib
from rdflib import URIRef
from rdflib import Graph
from haystack.query import SearchQuerySet

def MeaningAssocStats():

	main_tags = Tag.objects.filter(main_tag = True)
	meaning = 0

	weight_meaning = 0; weight_no_meaning = 0
	for i,t in enumerate(main_tags):
		if i%100 == 0: 
			print i
		if t.tagmeaning_set.count() > 0:
			meaning += 1
			weight_meaning += t.dataset_count()
		else:
			weight_no_meaning += t.dataset_count()

	print "Tags: " + str(len(Tag.objects.all()))
	print "Main Tags: " + str(len(main_tags))
	print "Tags With meaning: " + str(meaning)
	print "Tags With meaning weigted: " + str(weight_meaning)
	print "Tags With no meaning weigted: " + str(weight_no_meaning)

def CalculateStats(rounds):

	number_of_tags = sum(map(lambda x: x.number_of_tags(),rounds))
	number_of_datasets = sum(map(lambda x: x.number_of_datasets(),rounds))

	number_of_taggings = 0 
#	for o in rounds:
#		number_of_taggings += sum(filter(None,map(lambda x: x.n_tags ,o.dataset_set.all())))
		#imprecise > not taking real taggings

#	tag_per_dataset = numpy.array([o.tags_per_dataset() for o in rounds]).mean(axis=0)
#	datasets_per_group = numpy.array([o.datasets_per_group() for o in rounds]).mean(axis=0)

	all_tags, unique_tags = CalculateUniqueTags(rounds)

	stats = {'number_of_tags':number_of_tags,
			'number_of_datasets':number_of_datasets,
			'number_of_taggings':number_of_taggings,
#			'tag_per_dataset':tag_per_dataset,	
#			'datasets_per_group':datasets_per_group,
			'unique_tags':len(unique_tags),
			}

	return stats

def CalculateUniqueTags(rounds):

	all_tags = []
	unique_tags = []

	for o in rounds:
		for t in o.tag_set.all():
			all_tags.append(str(t.name.encode('utf-8')))

	srtd = sorted(all_tags,key=str.lower)

	unique_tags.append(srtd[0].lower().strip())

	for t in srtd:
		if t.lower().strip() != unique_tags[len(unique_tags)-1]:
			unique_tags.append(t.lower().strip())

	return all_tags, unique_tags

def CalculateCoocurrenceMatrix(r):

	for d in r.dataset_set.all():
		for t in d.tag_set.all():
			for tt in d.tag_set.all():
				if t != tt:
					try:
						c = Coocurrence.objects.get(tag_1 = t, tag_2 = tt)
						c.value += 1
					except:
						c = Coocurrence(tag_1 = t, tag_2 = tt, value=1)
					c.save()
	return


def CalculateSimilarityMatrix(r):

	tags = r.tag_set.all()

	v = []
	for t in tags:
		v.append(numpy.matrix(t.cooc_vector()))
#		print t

	for i,t in zip(range(len(tags)), tags):
		for ii,tt in zip(range(len(tags)), tags):
			if i != ii:
				if i < ii:
					try:
						c = Coocurrence.objects.get(tag_1 = t, tag_2 = tt)
						c.similarity = cosine_similarity(v[i],v[ii])
					except:
						c = Coocurrence(tag_1 = t, tag_2 = tt, similarity = cosine_similarity(v[i],v[ii]))
					c.save()
				if i > ii:
					c = Coocurrence.objects.get(tag_1 = tt, tag_2 = t)
					try:
						cc = Coocurrence.objects.get(tag_1 = t, tag_2 = tt)
						cc.similarity = c.similarity
					except:
						cc = Coocurrence(tag_1 = t, tag_2 = tt, similarity = c.similarity)
					cc.save()
				print t.name + ' - ' + tt.name + ' >> ' + str(c.similarity)
	return


def SyntacticSimilarity(tags):
	RANGE = 5
	tags = sorted(tags,key=lambda x:unidecode(x.display_name.lower()))
	similar_tags = []
	i = 0
	while i < len(tags)-1:
		j = 1
		# print i
		tags[i].similar_tags = []
		tags[i].main_tag = False
		while (j < RANGE) and (i+j < len(tags)):
			#check if difference is only on special chars or capitals
			if unidecode(tags[i].display_name.lower()) == unidecode(tags[i+j].display_name.lower()):
				# print tags[i]
				# print tags[i+j]	
				similar_tags.append([tags[i],tags[i+j]])
				tags[i].similar_tags.add(tags[i+j])
				tags.pop(i+j)
				j = j-1
			else:
				#check if difference is on edit distance, excluding tags with only numbers. tags containing numbers are already excluded
				if (Levenshtein.distance(unidecode(tags[i].display_name.lower()),unidecode(tags[i+j].display_name.lower())) < 2) and (tags[i].display_name.isdigit() == False):
					similar_tags.append([tags[i],tags[i+j]])
					# print tags[i]
					# print tags[i+j]	
					tags[i].similar_tags.add(tags[i+j])
					tags.pop(i+j)
					j = j-1
#				else:
			j += 1
		tags[i].main_tag = True
		tags[i].save()
		i+=1

	if	i == (len(tags)-1):
		tags[i].main_tag = True
		tags[i].save()


	#				grouped_tags.append(tags[i])

#	tags.save()
	i = 0
	while i < len(similar_tags)-1:
		if similar_tags[i][0] == similar_tags[i+1][0]:
			similar_tags[i].append(similar_tags[i+1][1])
			similar_tags.pop(i+1)
		i += 1

	return tags

def WriteCoocMatrix(r):

	tags = r.tag_set.all()

	csv_file = open('cooc_matrix.csv', 'w')
	csv_file.write ('source,target,interaction,directed,symbol,value,similarity'  + '\n')

	cooc = []
	for t in tags:
		print t.name
		cooc.append(Coocurrence.objects.filter(tag_1 = t))

	for i,t in zip(range(len(tags)),tags):
		for ii,tt in zip(range(len(tags)),tags):
			if ii > i:
				try:
					c = Coocurrence.objects.get(tag_1 = t, tag_2 = tt)
					if c.value > 0:
						csv_file.write (t.name.encode('utf-8') + ',' + tt.name.encode('utf-8') + ',coocurence,false,0,' + str(c.value) + ',' + str(c.similarity) +'\n')
				except:
					print erro
	
	csv_file.close
	return

def WriteTagGroupMatrix(r):

	csv_file = open('taggroup_matrix_nodes.csv', 'w')
	csv_file.write ('SUID;name;selected;shared name;type\n')

	tags = r.tag_set.all()
	for t in tags:
		csv_file.write ('' + str(t.ckan_id) + ';' + t.name.encode('utf-8') + ';false;' + t.name.encode('utf-8') + ';tag\n')

	groups = r.group_set.all()
	for g in groups:
		csv_file.write ('' + str(g.ckan_id) + ';' + g.display_name.encode('utf-8') + ';false;' + t.display_name.encode('utf-8') + ';group\n')

	csv_file.close

	csv_file = open('taggroup_matrix_edges.csv', 'w')
	csv_file.write ('source;target;interaction;directed;symbol\n')
	
	for t in tags:
		for d in t.datasets.all():
			for g in d.groups.all():
				csv_file.write ('' + t.ckan_id + ';' + g.ckan_id + ';belongsto;true;0\n')

	csv_file.close
	return

def WriteGroupCSV():

	csv_file = open('groups.csv', 'w')
	csv_file.write ('name;translated;tags\n')

	rounds = LoadRound.objects.filter(roundn=1, success=1)

	tags = []
	for r in rounds:
		groups = r.group_set.all()
		for g in groups:
			tr = g.translation if g.translation != None else g.display_name
			t = g.get_tags()
			tags += t
			csv_file.write ( '"' + g.display_name.encode('utf-8') + '";"' + tr.encode('utf-8') + '";"' + str(len(t)) + '"\n')
		tags = list(set(tags))

	print len(tags)			

	csv_file.close
	return

def LexicalCleaning(tag):
	''' Discard tags with low probability of representing concepts: tags not used, tags containing digits and letters, small tags and uppercase tags (may be acronyms) '''
	tag_name = tag.display_name
	
	MIN_LENGTH = 4

	nodigits_or_only_digits = False
	length = False
	uppercase = False
	not_used = False
	bad_format = False

	if tag.datasets.count() == 0:
		not_used = True
		# print "not_used"
	else:
		if (tag_name[0] == '.') or (tag_name[0] == ' ') or (tag_name[0] == '-') or \
			(len(tag_name.split(' ')) > 5) or (tag_name.isdigit() and (len(tag_name) != 4)):
			# print "bad_format"
			bad_format = True

		elif tag_name.isupper():
			# print "upp"
			uppercase = True

		if ([int(tag_name[i]) for i in range(0,len(tag_name)) if tag_name[i].encode('utf-8').isdigit()] == []) or \
		tag_name.encode('utf-8').isdigit():
			# print "nodigits_or_only_digits"
			nodigits_or_only_digits = True

		if len(tag_name) >= MIN_LENGTH:
			# print "length"
			length = True

	if nodigits_or_only_digits and length and not uppercase and not bad_format:
		# print "true"
		return True
	else:
		return False

def TranslateGroups():	

	rounds = LoadRound.objects.filter(roundn=1, success=1, id__gt = 122)

	for r in rounds:
		locale = r.odpmetadata_set.first().locale_default
		if (locale != "en") and (locale != None):
			for g in r.group_set.all():
				g.translation = TranslateYandex(g.display_name,locale.encode('utf-8'))
#				print g.display_name + " >> " + g.translation
				g.save()
	
def TranslateLexvo(word,lang):
	translation = URIRef("http://lexvo.org/ontology#translation")

	g = Graph()
	parse = True

	try:
#		print "http://www.lexvo.org/data/term/" + lang + "/" + urllib.quote(word.encode('utf-8').lower())
		g.parse("http://www.lexvo.org/data/term/" + lang + "/" + urllib.quote(word.encode('utf-8').lower()))
	except:
		parse = False

	translated = []

	if parse:
		for s,p,o in g.triples((None,translation,None)):
			#TODO UGLY - Dont do this!!!
			trans = str(o).split("/")[len(str(o).split("/"))-1]
			trans = urllib.unquote(trans).decode('utf8') 
#			print word + " === " + trans
#				raw_input("Press Enter to continue...")
			translated.append(trans)
	else:
		print 'failed'
		translated = None

	return translated

def GetMeaningsLexvo(word,lang):
	means = URIRef("http://lexvo.org/ontology#means")
	seeAlso = URIRef("http://www.w3.org/2000/01/rdf-schema#seeAlso")
	literal_form = URIRef("http://www.w3.org/2008/05/skos-xl#literalForm")

	g = Graph()
	parse = True	
	try:
		g.parse("http://www.lexvo.org/data/term/" + lang + "/" + urllib.quote(word.encode('utf-8').lower()))
	except:
		parse = False

	resources = []		

	if parse:
		for s,p,o in g.triples((None,means,None)):
			resources.append(o.encode('utf-8'))

		for s,p,o in g.triples((None,seeAlso,None)):
			resources.append(o.encode('utf-8'))
	else:
		resources = []

	return resources


def TranslateYandex(word,locale):

#	print word
	lang = locale[0:2]
	KEY = 'trnsl.1.1.20160329T142441Z.62a99f50a4ebc503.1b397557625c076bb4c3a7eb3c9d35420f48b5ba'
	page = lib.urlopen_with_retry("https://translate.yandex.net/api/v1.5/tr.json/translate?key=" + KEY + "&text=" + urllib.quote(word.encode('utf-8').lower()) + "&lang=" + lang + "-en")


	page_dict = json.loads(page.read())	
	translation = page_dict['text']

	return translation

def CleanTranslatedGroup():
	groups = Group.objects.all()

	for g in groups:
		if g.translation != None:
			if (g.translation[0] == '0') or (g.translation[0] == '1'):
				g.translation = g.translation.lstrip(' 0123456789')
				g.save()
			if g.translation[0:4].lower() == 'the ':
				g.translation = g.translation[4:]
				g.save()
			if g.translation[0:2].lower() == 'a ':
				g.translation = g.translation[2:]
			
			g.save()

def CleanTranslated():
	rounds = LoadRound.objects.filter(roundn=1, success=1)
	rounds_non_english = filter(lambda x: x.odpmetadata_set.first().locale_default[0:2] != 'en',rounds)
	all_tags_ = map(lambda x: x.tag_set.all(),rounds_non_english)
	all_tags = []
	for tags in all_tags_:
		for tag in tags:
			all_tags.append(tag)

	main_tags = filter(lambda x: x.main_tag == True and x.translation != None,all_tags)
	for t in main_tags:
		if t.translation[0:4].lower() == 'the ':
			t.translation = t.translation[4:]
			t.save()
	
		if t.translation[0:2].lower() == 'a ':
			t.translation = t.translation[2:]
			t.save()

def ProcessRoundTags(r):

	print "Starting " + r.open_data_portal.url
	tags = r.tag_set.all()
	
	print "CleanUp " + r.open_data_portal.url
	#1# Clean up
	clean_tags = []
	for t in tags:
		t.main_tag = False
		t.similar_tags = []
		t.save()
		if LexicalCleaning(t): 
			clean_tags.append(t)

	print "Syntactic Groupping " + r.open_data_portal.url
	#2# Syntactics Groupping
	gr = SyntacticSimilarity(clean_tags)

	print "Translating " + r.open_data_portal.url
	#3# Translation
	try:
		locale = r.odpmetadata_set.first().locale_default[0:2]
		locale = pycountry.languages.get(iso639_1_code=locale).iso639_3_code
	except:
		locale = 'eng'
	if (locale != "eng"):
		for t in r.tag_set.all():
			if t.main_tag:
				t.tagtranslation_set = []
				translations = TranslateLexvo(t.display_name,locale.encode('utf-8'))
#				print t.display_name + " >> " + str(translations)
				if translations:
					for trans in translations:
						tt = TagTranslation(tag = t,translation = trans).save()
					t.save()

	#4# Get Meanings
	print "Get Meanings " + r.open_data_portal.url
	for t in r.tag_set.all():
		meanings = []
		if t.main_tag:
			#test for original tag
			meanings = GetMeaningsLexvo(t.display_name,locale.encode('utf-8'))
			#test for similar tags
			if t.similar_tags.all() != None:
				for sim in t.similar_tags.all():
					meanings += GetMeaningsLexvo(sim.display_name,locale.encode('utf-8'))
			#test for translation
			if t.tagtranslation_set.all() != None:
				for trans in t.tagtranslation_set.all():
					meanings += GetMeaningsLexvo(trans.translation,'eng')

			meanings = set(meanings) #remove duplicates
#			print t.display_name
			t.tagmeaning_set.all().delete()	
			for m in meanings:
#				print ">>" + m
				TagMeaning(tag = t,meaning = m).save()

			t.save()

def MostUsedTags():
	rounds = LoadRound.objects.filter(roundn=1, success=1)
#	rounds_non_english = filter(lambda x: x.odpmetadata_set.first().locale_default[0:2] != 'en',rounds)
	all_tags_ = map(lambda x: x.tag_set.all(),rounds)#_non_english)
	all_tags = []
	for tags in all_tags_:
		for tag in tags:
			all_tags.append(tag)

	main_tags = filter(lambda x: x.main_tag == True,all_tags)

	main_tags = sorted(main_tags,key=lambda x:unidecode(x.display_name.lower()))

	global_tags = []	
	global_tags_count = []
	i = 0
	while i < (len(main_tags)-1):
		count = main_tags[i].datasets.count()
		same = True
		while (same == True) and (i < (len(main_tags)-1)):
			if SameTag(main_tags[i],main_tags[i+1]):
				count += main_tags[i+1].datasets.count()
				main_tags.pop(i+1)
			else:
				same = False

		global_tags.append([main_tags[i],count])
		
		i += 1
	return global_tags

def SameTag(t1,t2):
	tag1 = t1.translation if t1.translation else t1.display_name
	tag2 = t2.translation if t2.translation else t2.display_name
	if tag1 == tag2:
		return True
	else:
		return False


def Measures():
	all_dataset = []
	for r in rounds:
		all_dataset += r.dataset_set.all()
	print "All Datasets: " + str(len(all_dataset))

	dataset_in_groups = []
	for r in rounds:
		for g in r.group_set.all():
			dataset_in_groups += g.dataset_set.all()
	print "Datasets in Groups: " + str(len(set(dataset_in_groups)))

	tags_in_groups = []
	for d in dataset_in_groups:
		tags_in_groups += d.tag_set.all()
	print "Tags in Groups: " + str(len(set(tags_in_groups)))

	for r in rounds:
		all_tags += r.tag_set.all()
#	all_tags_s = sorted(all_tags,key=lambda x:x.datasets.count())

	print "Tags: " + str(len(all_tags))
	tag_0 = filter(lambda x: x.datasets.count() == 0,all_tags)
	print "Tags 0 datasets: " + str(len(tag_0))
	tag_1 = filter(lambda x: x.datasets.count() == 1,all_tags)
	print "Tags 1 datasets: " + str(len(tag_1))

	main_tags = filter(lambda x: x.main_tag == True,all_tags)	
	print "Main tags: " + str(len(main_tags))

	main_tags_meaning = filter(lambda x: len(x.tagmeaning_set.all()) > 0,main_tags)
	print "Tags with meaning: " + str(len(main_tags_meaning))

	datasets = []
	for t in main_tags_meaning:
		datasets += t.datasets.all()
	datasets = set(datasets)
	print "Datasets tagged with tags with meaning: " + str(len(datasets))

def GetRelatedMeanings(uri,ontology='gemet'):
	broader_uri = URIRef("http://www.w3.org/2004/02/skos/core#broader")
	narrower_uri = URIRef("http://www.w3.org/2004/02/skos/core#narrower")
	related_uri = URIRef("http://www.w3.org/2004/02/skos/core#related")
	narrower = []; broader = []; related = []

	g = Graph()
	
#	for m in tag.tagmeaning_set.all():
#		if ontology in m.meaning:
	parse = True	
	try:
		g.parse(uri)
	except:
		parse = False

#		print m.meaning
	if parse:
		for s,p,o in g.triples((None,broader_uri,None)):
#				print ">> " + str(o)
			broader.append(o.encode('utf-8'))

		for s,p,o in g.triples((None,narrower_uri,None)):
#				print ">> " + str(o)
			narrower.append(o.encode('utf-8'))

		for s,p,o in g.triples((None,related_uri,None)):
#				print ">> " + str(o)
			related.append(o.encode('utf-8'))


	broader = set(broader)
	narrower = set(narrower)
	related = set(related)
	m_broader = [];	m_narrower = []; m_related = []

	for b in broader:
		m_broader += TagMeaning.objects.filter(meaning=b)
	m_broader = list(set(map(lambda x: x.meaning,m_broader)))
	for n in narrower:
		m_narrower += TagMeaning.objects.filter(meaning=n)
	m_narrower = list(set(map(lambda x: x.meaning,m_narrower)))
	for r in related:
		m_related += TagMeaning.objects.filter(meaning=r)
	m_related = list(set(map(lambda x: x.meaning,m_related)))

	return m_broader, m_narrower, m_related

def WriteWiki():
#	https://datahub.io/api/3/action/package_search?fq=%28tags:popolazione%20OR%20tags:befolkning%29
	return False

def TranslateNotTranslated(no_translation):

#	main_tags = Tag.objects.filter(main_tag=True)
#	no_translation = filter(lambda x: (len(x.tagtranslation_set.all()) == 0) and (x.load_round.odpmetadata_set.first().locale_default[0:2] != 'en'),main_tags)

	for t in no_translation:
		locale = t.load_round.odpmetadata_set.first().locale_default[0:2]
		#locale = pycountry.languages.get(iso639_1_code=locale).iso639_3_code
		print t
		t.tagtranslation_set = []
		translations = TranslateYandex(t.display_name,locale.encode('utf-8'))

		if translations:
			if not(isinstance(translations, list)):
				translations = [translations]	
			for trans in translations:
#				print trans
				if trans[0:4] == 'the ':
					trans = trans[4:]
				if trans[0:2] == 'a ':
					trans = trans[2:]
				print trans.encode('utf-8')
				tt = TagTranslation(tag = t,translation = trans.encode('utf-8')).save()
			t.save()


def GetMeaningForNoMeaning():

	main_tags = Tag.objects.filter(main_tag=True)
	trans_no_meaning = filter(lambda x: (len(x.tagmeaning_set.all()) == 0) and (len(x.tagtranslation_set.all()) > 0),main_tags)


	for t in trans_no_meaning:
		print t
		meanings = []
		t.tagmeaning_set = []
		if t.main_tag:
			#test for original tag
			meanings = GetMeaningsLexvo(t.display_name,t.load_round.odpmetadata_set.first().locale_default.encode('utf-8'))
			#test for similar tags
			if t.similar_tags.all() != None:
				for sim in t.similar_tags.all():
					meanings += GetMeaningsLexvo(sim.display_name,t.load_round.odpmetadata_set.first().locale_default.encode('utf-8'))
			#test for translation
			if t.tagtranslation_set.all() != None:
				for trans in t.tagtranslation_set.all():
					meanings += GetMeaningsLexvo(trans.translation,'eng')

			meanings = set(meanings) #remove duplicates
#			print t.display_name
			for m in meanings:
				print ">>" + m
				TagMeaning(tag = t,meaning = m).save()

			t.save()

def CreateGlobalGroups():
	groups = Group.objects.all()
	groups = sorted(groups,key=lambda g: g.translation.lower() if g.translation != None else g.display_name.lower())

	global_groups = []
	i = 0
	while i < len(groups)-1:
		global_groups.append([groups[i],1])	
		while groups[i].translated().lower() in groups[i+1].translated().lower():
			groups.pop(i+1)
			global_groups[i][1] += 1
		i += 1

	sorted(global_groups,key=lambda g: g[1])
	most_frequent = filter(lambda x: x[1] > 2, global_groups)	

	most_frequent

	groups = Group.objects.all()

	for gg in most_frequent:
		gl_gr = GlobalGroup(name=gg[0].translated())
		gl_gr.save()
		for g in groups:
			if (g.translated().lower() in gg[0].translated().lower()) or (gg[0].translated().lower() in g.translated().lower()):
				gl_gr.groups.add(g) 
		gl_gr.save()

def DiscardMainTags():

	tags = Tag.objects.filter(main_tag = True)
	discarded = []
	for t in tags:
		name = t.get_translation()
		if (name[0] == '.') or (name[0] == ' ') or (name[0] == '-') or (len(name.split(' ')) > 5) or (name.isdigit() and (len(name) != 4)):
			t.main_tag = False
#			discarded.append(t)
			t.save()

	return discarded

def MeaningStats():

	ontologies = {
		'agclass',
		'wiktionary',
		'eurovoc',
		'id.loc.gov',
		'iso3166',
	 	'iso639-3',
	 	'iso639-5',
	 	'un_m49',
		'wordnet',
		'stitch',
		'sw.cyc.com',
	 	'opencyc.org',
	 	'astro.physik',
		'gemet',
		'agrovoc',
	 	'nlm.nih.gov'
		}

	meanings = TagMeaning.objects.all()

	tags = Tag.objects.all()
	count = [0]*len(ontologies)
	for t in tags:
		for i,o in enumerate(ontologies):
			for m in t.tagmeaning_set.all():
				if o in m.meaning:
					count[i] += 1
					break

	for i,o in enumerate(ontologies):
		result = TagMeaning.objects.raw("SELECT * FROM `tag_analytics_tagmeaning` WHERE `meaning` LIKE '%%" + o + "%%'")
		num = 0;meanings = []
		for r in result: meanings.append(r.meaning); num += 1		
		print o + ': ' + str(num) + "(" + str(len(set(meanings))) + ") >> in " + str(count[i]) + " tags"

#wiktionary: 55482(20472) >> in 42735 tags
#sw.cyc.com: 2(1) >> in 2 tags
#stitch: 244(185) >> in 236 tags
#gemet: 11225(2143) >> in 10102 tags
#eurovoc: 7581(1534) >> in 7344 tags
#id.loc.gov: 15954(3816) >> in 12141 tags
#opencyc.org: 65454(8960) >> in 28681 tags
#nlm.nih.gov: 6239(1474) >> in 6138 tags
#un_m49: 1(1) >> in 1 tags
#iso639-3: 5(4) >> in 5 tags
#iso639-5: 2(1) >> in 2 tags
#agrovoc: 9082(1962) >> in 8896 tags
#iso3166: 15(14) >> in 15 tags
#astro.physik: 2359(523) >> in 2309 tags
#wordnet: 149069(27053) >> in 30267 tags
#agclass: 9750(2694) >> in 9612 tags


def CreateGlobalTags(ontology):

	gg = GlobalTag.objects.all()
	if gg != []:
		for g in gg:
			g.delete()

	result = TagMeaning.objects.raw("SELECT * FROM `tag_analytics_tagmeaning` WHERE `meaning` LIKE '%%" + ontology + "%%'")
	tagmeanings = []
	for r in result: tagmeanings.append(r.meaning)
	tagmeanings = set(tagmeanings)

	for tm in tagmeanings:
		print tm
		name, description = GetNameAndDescription(tm, ontology=ontology)
		gt = GlobalTag(name=name,description=description,uri=tm)
		gt.save()

		tags = TagMeaning.objects.filter(meaning = tm)
		for t in tags:
			gt.tags.add(t.tag)
			for st in t.similar_tags.all():
				gt.tags.add(st)
		gt.save
	
def SetRelations():
	global_tag = GlobalTag.objects.all()

	for gt in global_tag:
		gt.broader = []
		gt.narrower = []
		gt.related = []

		b, n, r = GetRelatedMeanings(gt.uri,'gemet')
		if (b != []):
			for br in b:
				t = GlobalTag.objects.get(uri = br)
				gt.broader.add(t)
		if (n != []):
			for na in n:
				t = GlobalTag.objects.get(uri = na)
				gt.narrower.add(t)
		if (r != []):
			for re in r:
				t = GlobalTag.objects.get(uri = re)
				gt.related.add(t)

		gt.save()

def GetNameAndDescription(uri, ontology=None):

	g = Graph()
	definition = URIRef('http://www.w3.org/2004/02/skos/core#definition')
	name = URIRef('http://www.w3.org/2004/02/skos/core#prefLabel')

	if ontology == 'eurovoc':
		uri = "http://eurovoc.europa.eu/webservices/getLabelsByConceptURI?URI=" + uri + "&termType=prefLabel&lang=en&format=rdf"

	parse = True	
	try:
		g.parse(uri)
	except:
		parse = False

	nm = '';defn = ''
	if parse:
#		for s,p,o in g.triples((None,None,None)):
#			print str(p).encode('utf-8')

		for s,p,o in g.triples((None,definition,None)):
			if o.language == 'en': defn = o.value; break

		for s,p,o in g.triples((None,name,None)):
			if o.language == 'en': nm = o.value; break

	return nm, defn

def GlobalTagStats():
	global_tags = GlobalTag.objects.all()
	count = 0
	datasets = []
	for gt in global_tags:
		for t in gt.tags.all():
			count += 1
			datasets += t.datasets.all()
			for s in t.similar_tags.all():
				count += 1
				datasets += t.datasets.all()

	print "Global Tags: " + str(len(global_tags))
	print "Local Tags Associated: " + str(count)
	print "Datasets Associated: " + str(len(set(datasets)))

	
def ReconcileGroups():

#	page = lib.urlopen_with_retry('http://www.eionet.europa.eu/gemet/fetchThemes?language=en')
#	page_dict = json.loads(page.read())	
	global_groups = GlobalGroup.objects.all()

	for gg in global_groups:
#		ass = False
#		for theme in page_dict:
#			if (gg.name in theme['preferredLabel']['string']) or (theme['preferredLabel']['string'] in gg.name):
#				print gg.name + "==" + theme['preferredLabel']['string']
#				gg.uri = theme['uri']
#				ass = True
#		if ass == False:
			print gg.name 
			page = lib.urlopen_with_retry('http://www.eionet.europa.eu/gemet/getConceptsMatchingKeyword?keyword=' + urllib.quote(gg.name.encode('utf-8').lower()) + '&search_mode=0&thesaurus_uri=http://www.eionet.europa.eu/gemet/concept/&language=en')
			page_dict2 = json.loads(page.read())	
			for p in page_dict2:
#				print ">> " + p['preferredLabel']['string']
				gg.uri = page_dict2[0]['uri']
			gg.save()

def AssocGlobalTagsToGroups():

	theme = "http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#theme"

	globaltags = GlobalTag.objects.all()
	for gt in globaltags:
		print gt.name
		page = lib.urlopen_with_retry("http://www.eionet.europa.eu/gemet/getRelatedConcepts?concept_uri=" + gt.uri + "&relation_uri=" + urllib.quote(theme) )
		page_dict = json.loads(page.read())	
#		if len(page_dict) == 0:
#			print "top: " + gt.name
		for t in page_dict:
#			print t['uri']
			gg = GlobalGroup.objects.filter(uri = t['uri'])
			if  len(gg) > 0:
				for g in gg:
#					print "found " + gt.name
					gt.global_groups.add(g)
					gt.save()
			else:
				g = GlobalGroup(name = t['preferredLabel']['string'], uri = t['uri'])
				g.save()
				gt.global_groups.add(g)
				gt.save()
#				print "not found " + gt.name
	
def GlobalGroupsURI():

	globalgroups = GlobalGroup.objects.all()
	g = Graph()
	name = URIRef('http://www.w3.org/2004/02/skos/core#prefLabel')

	for gg in globalgroups:
		print gg.uri
#		print gg.name
#		if gg.uri:
#			g.parse(gg.uri)
#			for s,p,o in g.triples((None,name,None)):
#				if o.language == 'en': print ">> " + o.value + ' - ' + gg.uri; break

def MergeGroups(g1,g2,action='show'):
	
	if action == 'show':
		print "G1: " + g1.name + " - " + g1.uri
		for g in g1.groups.all():
			print " >> " + g.display_name
		for g in g1.globaltag_set.all():
			print " >>>> " + g.name

	
		print "--------------------"
		print "G2: " + g2.name + " - " + g2.uri
		for g in g2.groups.all():
			print " >> " + g.display_name
		for g in g2.globaltag_set.all():
			print " >>>> " + g.name


	elif action == 'merge':
		for g in g2.groups.all():
			g1.groups.add(g)
			g1.save()
		g2.delete()

def HarvestDatasetDescriptions():

	rounds = LoadRound.objects.filter(success=1, roundn =1, id = 85)

	print "getting dataset descriptions"


	for r in rounds:
		## get datasets
		LIMIT = 50
		START = 0
		

		keeploading = True
		url = r.open_data_portal.url

		print url + '/api/3/action/package_search?rows='+str(LIMIT)+'&start='+str(START)

		while keeploading:
			dataset_list_response = 0
			try:
				dataset_list_response = lib.urlopen_with_retry(url + '/api/3/action/package_search?rows='+str(LIMIT)+'&start='+str(START))

#				dataset_list_response = lib.urlopen_with_retry("https://data.qld.gov.au/api/3/action/package_search?fq=tags:injury")
			except:
				print "Website not available while getting datasets"
				break


			if dataset_list_response: 
				dataset_list = []	
				try: 
					dataset_list_dict = json.loads(dataset_list_response.read())
					dataset_list = dataset_list_dict['result']['results']
				except:
					1 == 1

				print url + '/api/3/action/package_search?rows='+str(LIMIT)+'&start='+str(START)

				print START
				print len(dataset_list)
				print dataset_list_dict['result']['count']
				print "----"

				if (len(dataset_list) == 0):
					keeploading = False
					break		
				else:
					START += LIMIT

				for dataset in dataset_list:
					dataset_response = 0

					d_id = dataset.get('id')
					notes = dataset.get('notes')
#					print d_id
#					print dataset.get('notes')
#					try: 
					dd = Dataset.objects.filter(ckan_id = d_id)
					for d in dd:
						if (notes != None) and (d.description == None):
							d.description = notes
							d.save()
#							print "-------"
#							print d.description
							
#					except:
#						print "dataset not found"
#			break


def HarvestDatasetDescriptions2(roundn):

	datasets = Dataset.objects.filter(load_round_id = roundn)

	for d in datasets:
		url = d.load_round.open_data_portal.url + '/api/3/action/package_search?fq=id:' + d.ckan_id
#		url = "http://open-data.europa.eu/data/api/3/action/package_search?fq=name:5t0thInXvB1fGFyAqYi9A"

#		print url
		description = 0
		try: 
			dataset_list_response = lib.urlopen_with_retry(url)
			dataset_list_dict = json.loads(dataset_list_response.read())
		except:
			print "error"

#TEST ID DESCRIPTION
		try:
			desc = dataset_list_dict['result']['results'][0]['description']
		except:	
			desc = None
		try:
			desc2 = dataset_list_dict['result']['results'][0]['notes']
		except:
			desc2 = None

		if desc != None:
			print "1"
			print desc
		if desc2 != None:
			d.description = desc2
			print desc2

#		break
		d.save()

def ReconcileOrphanTags():
	main_tags = Tag.objects.filter(main_tag=True)
	orphans = filter(lambda x: x.tagmeaning_set.count() > 0,main_tags)

	for orphan in orphans:
		print orphan.display_name
		sqs = SearchQuerySet().filter(text=orphan.get_translation())
		for res in sqs:
				if res.content_type == 'tag_analytics.globaltag':
					print orphan.display_name + " > " + res.object.name
					break
		break

def ManualReconcile():

	term = 'public procurement'
	term2 = 'procurement'	
	gemet_uri = 'http://www.eionet.europa.eu/gemet/concept/6810'
	# sqs = SearchQuerySet().filter(text=term).filter_or(text=term2)
	# for res in sqs:
	# 	t = res.object
	# 	if res.content_type() == 'tag_analytics.tag':
	# 		if t.main_tag == True:
	# 			try:
	# 				TagMeaning.objects.get(tag_id=t.id,meaning = gemet_uri)
	# 			except:
	# 				print str(t.id) + t.display_name
	# 				m = TagMeaning(tag=t, meaning = gemet_uri)
	# 				m.save()

	gt = GlobalTag.objects.get(id = 4321)
	tms = TagMeaning.objects.filter(meaning = gemet_uri)
	for tm in tms:
		t = Tag.objects.get(id = tm.tag_id)
		gt.tags.add(t)
	gt.save()
#TODO
#enhance tag - global tag matching.
#failing examples: health-care not assigned to health care
# PROCUREMENT not assigned to public procurement
#tags containing - in the begging also failing

def AssocTagGlobalTag(load_round_id):

	tags = Tag.objects.filter(load_round_id = load_round_id)
	for t in tags:
		for m in t.tagmeaning_set.all():
			gts = GlobalTag.objects.filter(uri = m.meaning)
			for gt in gts:
				print gt
				gt.tags.add(t)
				for st in t.similar_tags.all():
					gt.tags.add(st)
				gt.save()

def SetMeaningToSimilarTags():

	main_tags = Tag.objects.filter(main_tag = True)
	for t in main_tags:
		for gt in t.globaltag_set.all():
			for st in t.similar_tags.all():
				gt.tags.add(st)
				gt.save()
			

def RemoveTrailOpenDataPortalUrl():
	oo = OpenDataPortal.objects.all()

	for o in oo:
		o.url = o.url.strip('/')
		o.save()

