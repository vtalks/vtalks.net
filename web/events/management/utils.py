import re


def get_twitter_handle(data):
    """ Extract twitter handle
    """
    twitter_handle = ""

    if not data:
        return twitter_handle

    # Match patterns like 'https://twitter.com/handle
    regexp = "https:\/\/twitter.com\/(?P<handle>.*)"
    m = re.findall(regexp, data)
    if len(m) > 0:
        twitter_handle = m[0]

    return twitter_handle
