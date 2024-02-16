def get_site_from_url(url):
  url_parts=url.split('/')

  if url.startswith('http'):
    return url_parts[2]
  else:
    return url_parts[0]



def normalize_slash_url(url):
  # TODO: Add domain and https:
  # TODO: Identify files (like .js, .css, name.html, .pdf or images)

  if not url.endswith('/'):
    return url+'/'

  return url



def normalize_link(url, page_url):
  (protocol, void, domain, *path_parts) = page_url.split('/')
  normalized_url = url

  if normalized_url.startswith('//'):
    normalized_url = protocol+normalized_url

  if normalized_url.startswith('/'):
    normalized_url = protocol+'//'+domain+normalized_url

  if normalized_url.startswith('#'):
    normalized_url = page_url+normalized_url

  return normalized_url