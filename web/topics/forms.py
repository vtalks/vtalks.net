from dal import autocomplete

from topics.models import Topic


class TopicForm(autocomplete.FutureModelForm):

    class Meta:
        model = Topic
        fields = ('__all__')
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple('tags:tag-autocomplete')
        }