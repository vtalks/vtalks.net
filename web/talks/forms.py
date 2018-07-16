from dal import autocomplete

from talks.models import Talk


class TalkForm(autocomplete.FutureModelForm):

    class Meta:
        model = Talk
        fields = ('__all__')
        widgets = {
            'tags': autocomplete.TaggitSelect2('tags:tag-autocomplete')
        }