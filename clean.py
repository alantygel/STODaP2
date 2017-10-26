import django
django.setup()

from tag_analytics.functions_rdf import cleanStr
from tag_analytics.views_rdf import PrintDatasetRdfListView

print "cleaning"
cleanStr()
print "gen rdf"
PrintDatasetRdfListView(None)
