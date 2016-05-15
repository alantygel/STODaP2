from evaluation.models import DatasetAnswer
from evaluation.models import Answer

def adjust():

	das = DatasetAnswer.objects.all()
	for da in das:
		urls = da.urls.split("#")
		for url in urls:
			a = Answer(url=url, dataset_answer = da)
			a.save()

