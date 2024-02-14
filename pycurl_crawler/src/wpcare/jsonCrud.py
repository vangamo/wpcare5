import json
import os

ROOT_DIR = os.path.abspath(os.curdir)
DATA_DIR = os.path.join(ROOT_DIR, "data")

class JsonCrud:
  def __init__(self, entity, auto_commit=False, key_attr='id'):
    self.entity = entity
    self.last_inserted_id = 0
    self.config = {
      "auto_commit": auto_commit,
      'key': key_attr
    }
    self.cache = []

    FILENAME = self.entity+".json"
    self.ENTITY_FILENAME = os.path.join(DATA_DIR, FILENAME)
    
    self.open()

  def open(self):
    try:
      with open(self.ENTITY_FILENAME, 'r') as f:
        self.cache = json.load(f)

        if len(self.cache) > 0:
          all_id = [item[self.config['key']] for item in self.cache]
          self.last_inserted_id = max(all_id)

    except Exception as e:
      print('ERROR reading '+self.ENTITY_FILENAME)
      print(e)

      self.commit()

  def close(self):
    self.commit()



  def get(self, *args, **kwargs):
    data = _check_parameters(args, kwargs)

    if len(data) == 0:
      raise BaseException("No data provided")

    idx = self._get_idx(data)

    return self.cache[idx] if idx is not None else None



  def count(self, *args, **kwargs):
    data = _check_parameters(args, kwargs)

    item_list = list(item for item in self.cache if _search_condition(data, item))

    return len(item_list)



  def select(self, *args, **kwargs):
    data = _check_parameters(args, kwargs)

    item_generator = (item for item in self.cache if _search_condition(data, item))

    return item_generator
  


  def insert(self, *args, **kwargs):
    data = _check_parameters(args, kwargs)

    if self.config['key'] not in data:
      self.last_inserted_id += 1
      data[ self.config['key'] ] = self.last_inserted_id
    else:
      self.last_inserted_id = max( self.last_inserted_id, data[ self.config['key'] ])

    self.cache.append(data)

    if self.config['auto_commit']:
      self.commit()

    return self.last_inserted_id



  def update(self, data_search, data_update):
    indexes = list(index for index, item in enumerate(self.cache) if _search_condition(data_search, item))[::-1]
    updated_items = []

    for idx in indexes:
      new_item = dict(self.cache[idx], **data_update)
      self.cache[idx] = new_item
      updated_items.append(new_item)
      print( 'UPDATE', new_item )

    if self.config['auto_commit']:
      self.commit()

    return updated_items



  def delete(self, *args, **kwargs):
    data = _check_parameters(args, kwargs)

    if data is None:
      return []

    indexes = list(index for index, item in enumerate(self.cache) if _search_condition(data, item))[::-1]
    removed_items = []

    for idx in indexes:
      removed_items.append( self.cache.pop(idx) )

    if self.config['auto_commit']:
      self.commit()

    return removed_items[::-1]



  def commit(self):
    try:
      with open(self.ENTITY_FILENAME, 'w') as f:
        json.dump(self.cache, f, indent=2)
    
    except Exception as e:
      print('ERROR writting '+self.ENTITY_FILENAME)
      print(e)
  

  def _get_idx(self, data):
    index = next((index for index, item in enumerate(self.cache) if _search_condition(data, item)), None)
    return index
  

def _check_parameters(args, kwargs):
  data = {}

  if len(args) == 1 and (isinstance(args[0], dict) or isinstance(args[0], object)):
    data = args[0]
  else:
    data = kwargs
  
  return data


def _search_condition(data, item):
  for k,v in data.items():
    if item[k] != v:
      return False
  else:
    return True

if __name__ == "__main__":
  testCrud = JsonCrud('test', auto_commit=True)

  testCrud.insert({'id': 128, 'name': 'test 1', 'created_at': 1707908140, 'category': 'test'})
  testCrud.insert({'name': 'test 2', 'created_at': 1707908280, 'category': 'test'})

  print( testCrud.get({'id': 1, 'name': 'test 1'}) )
  print( testCrud.get(id=2) )

  print( list(testCrud.select(id=1) ) )
  print( list(testCrud.select(category="test") ) )
  print( list(testCrud.select({ "category": "test"} ) ) )

  print( testCrud.count(id=1) )
  print( testCrud.count(category="test") )
  print( testCrud.count({ "category": "test"} ) )


  testCrud.insert({'name': 'test to delete', 'created_at': 1707908512, 'category': 'test'})

  print( list(testCrud.select() ) )

  print( testCrud.delete(id=3) )

  print( list(testCrud.select() ) )


  testCrud.insert({'name': 'test to delete', 'created_at': 1707908512, 'category': 'test'})
  testCrud.insert({'name': 'test to delete', 'created_at': 1707908512, 'category': 'test'})
  testCrud.insert({'name': 'test to delete', 'created_at': 1707908512, 'category': 'test'})

  print( testCrud.update( {'name': 'test to delete'}, {'name': 'test to update'} ))

  print( list(testCrud.select() ) )