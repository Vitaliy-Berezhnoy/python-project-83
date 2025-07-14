from urllib.parse import urlparse

import validators


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def is_valid_url(url):
    return validators.url(url) and len(url) <= 255

