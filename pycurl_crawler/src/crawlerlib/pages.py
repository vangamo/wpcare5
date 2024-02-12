from wpcare.pages import Pages as WPCarePages



class Pages(WPCarePages):
  PAGES = []

  KEYNAMES = ['id', 'uuid', 'url']
  FIELDNAMES = ['id', 'uuid', 'url', 'created_at', 'site', 'types', 'visited_at', 'links']


Pages.init()
