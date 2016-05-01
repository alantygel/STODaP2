from django import forms
from django.utils.text import capfirst
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

from haystack.forms import ModelSearchForm
from haystack.forms import FacetedSearchForm
from haystack.constants import DEFAULT_ALIAS
from haystack import connections
from haystack.utils import get_model_ct

from haystack.utils.app_loading import haystack_get_model

from .models import Dataset

def model_choices(using=DEFAULT_ALIAS):
    choices = [(get_model_ct(m), capfirst(smart_text(m._meta.verbose_name_plural)))
               for m in connections[using].get_unified_index().get_indexed_models()]
    return sorted(choices, key=lambda x: x[1])

class MySearchForm(ModelSearchForm):

    q = forms.CharField(required=False, label='',
                        widget=forms.TextInput(attrs={'type': 'search' , 
                                                      }))

    def __init__(self, *args, **kwargs):
        super(ModelSearchForm, self).__init__(*args, **kwargs)
        self.fields['models'] = forms.MultipleChoiceField(choices=model_choices(), required=False, label=_('Search Only In'), widget=forms.CheckboxSelectMultiple)

    def get_models(self):
        """Return a list of the selected models."""
        search_models = []

        if self.is_valid():
            for model in self.cleaned_data['models']:
                search_models.append(haystack_get_model(*model.split('.')))

        return search_models

    def search(self):
        sqs = super(ModelSearchForm, self).search()
        return sqs.models(*self.get_models())

class MyFacetedSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        self.selected_facets = kwargs.pop("selected_facets", [])
        super(FacetedSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(FacetedSearchForm, self).search()

        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))

        return sqs.models(Dataset)