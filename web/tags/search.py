from django.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def search_talks_by_tag(tag, page=None, sort=None):
    """ Get Talks by Tag from ElasticSearch
    """
    client = Elasticsearch([{
        'host': settings.ELASTICSEARCH['default']['HOSTNAME'],
        'port': settings.ELASTICSEARCH['default']['PORT'],
    }])

    s = Search(using=client, index="vtalks")

    # Build query
    s = s.filter('term', tags=tag.name)

    # Pagination
    if page:
        start = 0
        end = 10
        if page > 1:
            start = settings.PAGE_SIZE * (page - 1)
            end = settings.PAGE_SIZE * page
        s = s[start:end]

    # Sorting
    if sort:
        if sort == 'date':
            sort = 'created'
        elif sort == 'popularity':
            sort = 'wilsonscore_rank'
        else:
            sort = '_score'
        s = s.sort({sort: {"order": "desc"}})

    # Fields selection
    s = s.source(['id'])

    response = s.execute()

    results_total = response.hits.total
    results_ids = [hit.id for hit in response.hits]

    return results_total, results_ids