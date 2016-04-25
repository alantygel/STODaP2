from .models import Tag
from .models import OpenDataPortal
from .models import LoadRound

from unidecode import unidecode

def SummaryTable():

	number_of_portals = OpenDataPortal.objects.count()
	rounds = LoadRound.objects.filter(roundn=1,success=1)
	all_tags = 0
	for r in rounds: all_tags += r.tag_set.count()

	all_groups = 0
	for r in rounds: all_groups += r.group_set.count()

	all_datasets = 0
	notag_datasets = 0
	nogroup_datasets = 0
	min_datasets = 1000; max_datasets = 0; min_tags = 1000 ; max_tags = 0
	for r in rounds:
		if r.tag_set.count() > max_tags: max_tags = r.tag_set.count()
		if r.tag_set.count() < min_tags: min_tags = r.tag_set.count()
		if r.dataset_set.count() < min_datasets: min_datasets = r.dataset_set.count()
		if r.dataset_set.count() > max_datasets: max_datasets = r.dataset_set.count()
		for d in r.dataset_set.all():
			all_datasets += 1
			if d.tag_set.count() == 0: notag_datasets += 1			
			if d.groups.count() == 0: nogroup_datasets += 1


	print "number_of_portals: " + str(number_of_portals)
	print "number_success_portals: " + str(len(rounds))
	print "number of tags: " + str(all_tags)
	print "number of groups: " + str(all_groups)
	print "number of datasets: " + str(all_datasets)
	print "number of datasets without group: " + str(nogroup_datasets)
	print "number of datasets without tag: " + str(notag_datasets)
	print "min_datasets: " + str(min_datasets) 
	print "max_datasets: " + str(max_datasets)	
	print "min_tags: " + str(min_tags)
	print "max_tags: " + str(max_tags)


def TagsOverN(N):

	mfile = open('percentage_over_' + str(N) + '.m', 'w')
	mfile.write ('tags_over_n = ['  + '\n')

	rounds = LoadRound.objects.filter(roundn=1,success=1)
	tags_over_n_perc = []
	for r in rounds:
		tags_over_n = 0
		for t in r.tag_set.all():
			if t.datasets.count() > N:
				tags_over_n += 1
		if r.tag_set.count() != 0:
			res = float(tags_over_n)/float(r.tag_set.count())
		else:		
			res = 0

		av_reuse = sum(map(lambda z: z.datasets.count(), r.tag_set.all()))/float(r.tag_set.count())

		tags_over_n_perc.append(res)
		mfile.write (str(tags_over_n) + ' ' + str(res) + " " + str(av_reuse) +'\n')

#		# merge similar tags
#		alltags = []
#		odp = ODP[o]	
#		for t in odp.tags:
#			alltags.append(model.AllTags(t.name,odp.url,t.count,odp.lang))
#		alltags = sorted(alltags,key=lambda x: x.name)

#		k = 0
#		print odp.url
#		while k < len(alltags)-1:
#			if (unidecode(alltags[k].name.lower()) == unidecode(alltags[k+1].name.lower())):
#				alltags[k].count += alltags[k+1].count
#				alltags.remove(alltags[k+1])
#				k -= 1		
#			k += 1
#			#print str(k) + " " + str(len(list))

#		tags_over_n = 0
#		for t in alltags:
#			if int(t.count) > N:
#				tags_over_n += 1
#		if len(alltags) != 0:
#			res2 = float(tags_over_n)/float(len(alltags))
#		else:		
#			res2 = 0

#		av_reuse_m = sum(map(lambda z: z.count, alltags))/float(len(alltags))
#		print av_reuse_m

#		mfile_m.write (str(tags_over_n) + ' ' + str(res2) +  " " + str(av_reuse_m) + '\n')

	mfile.write ('];')
	mfile.close()

#	mfile_m.write ('];')
#	mfile_m.close()

	tags_over_n_perc = sorted (tags_over_n_perc)
	return tags_over_n_perc	

def TagsDistribution():

	mfile = open('tags_distibution.m', 'w')
	rounds = LoadRound.objects.filter(roundn=1,success=1)

	k = 0;
	for r in rounds:
		if r.tag_set.count() > 0:
			k += 1
			mfile.write('tags_distibution{' + str(k) +  '} = [\n')
			for t in r.tag_set.all():
				mfile.write(str(t.datasets.count()) + '\n')
			mfile.write('];\n')

	mfile.close()

def TagsPerDataset():

	mfile = open('tags_perdataset.m', 'w')
	rounds = LoadRound.objects.filter(roundn=1,success=1)
	k = 0;
	for r in rounds:
		if r.dataset_set.count() > 0:
			k += 1
			mfile.write('tags_per_dataset{' + str(k) +  '} = [\n')
			for d in r.dataset_set.all():
				mfile.write(str(d.tag_set.count()) + '\n')
			mfile.write('];\n')

	mfile.close()

def Similarity():

	rounds = LoadRound.objects.filter(roundn=1,success=1)
	mfile = open('similarity.m', 'w')

	mfile.write('similarity = [ \n')	
	for k,r in enumerate(rounds):
		T = r.tag_set.count()
		tags = r.tag_set.all()
		tags = map(lambda x: unidecode(x.display_name.lower()), tags)
		tags = sorted(tags)
		s = 0
		for i in range(T-1):
			j = i
			while (tags[j] == tags[j+1]):
				s += 1
				if (j+1) < T-1:
					j += 1
				else:
					break
		mfile.write(str(float(s)/len(tags)) + '\n')	
	mfile.write(']; \n')	

