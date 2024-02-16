import uuid
from datetime import datetime

from wpcare.jsonNamedCrud import JsonNamedCrud



class ModelBase():
  ADAPTER = None

  FIELDNAMES = ['id', 'created_at']
  KEYS = ['id']



  def __init__(self, identifier_or_data=None):
    self.initialize()

    if identifier_or_data is None:
      self.id = None

    elif isinstance(identifier_or_data, int) or (isinstance(identifier_or_data, int) and identifier_or_data.isdecimal()):
      self.id = int(identifier_or_data)
      self.load()

    elif isinstance(identifier_or_data, dict):
      self.objetivize(identifier_or_data)

    else:
      raise BaseException("TODO: Not implemented!")



  '''
    Set default values to object attributes
  '''
  def initialize(self):
    for field in self.FIELDNAMES:
      setattr(self, field, None)

    now = int(datetime.utcnow().timestamp())

    self.created_at = now



  def serialize(self):  # TODO: Add field types
    data_object = {}

    for field in self.FIELDNAMES:
      data_object[field] = getattr(self, field)

    return data_object



  def objetivize(self, data):  # TODO: Add field types
    for field in self.FIELDNAMES:
      setattr(self, field, data[field] if field in data else None)
    


  def save(self):
    if self.ADAPTER is None:
      raise BaseException("CONFIG ERROR: No adapter configured")

    self.ADAPTER.create(self)



  def load(self):
    if self.ADAPTER is None:
      raise BaseException("CONFIG ERROR: No adapter configured")

    item_data = None

    if self.id is not None:
      item_data = self.ADAPTER._get_data_raw(id=self.id)

    if item_data is None:
      self.initialize()
    else:
      self.objetivize(item_data)





class AdapterBase():
  MODEL_CLASS = ModelBase
  NAME = None

  @classmethod
  def init(cls):
    cls.MODEL_CLASS.ADAPTER = cls

    if cls.NAME is not None:
      cls.STORAGE = JsonNamedCrud(cls.NAME, cls.MODEL_CLASS, auto_commit=True, key_attr='id')



  @classmethod
  def get(cls, **kwargs):
    cls._check_params_are_fields(kwargs)

    identifier, identifier_value = next(cls._get_key_fields_from_params(kwargs))

    item = cls.STORAGE.get({identifier: identifier_value})
    return item



  @classmethod
  def list(cls, **kwargs):
    cls._check_params_are_fields(kwargs)

    item_list = cls.STORAGE.select( kwargs )

    return item_list



  @classmethod
  def create(cls, item):
    if item is None:
      raise BaseException("DATA ERROR: Item is None")
    
    if not isinstance(item, cls.MODEL_CLASS):
      raise BaseException("DATA ERROR: Item is not a "+str(cls.MODEL_CLASS))

    try:
      for identifier, identifier_value in cls._get_key_fields_from_params(item.serialize()):
        print('ID',identifier, identifier_value)
        item_found = cls.STORAGE.get({identifier: identifier_value})
        if item_found is not None:
          break

    except:
      if 'uuid' in item.FIELDNAMES:
        item.uuid = str(uuid.uuid4())
      cls.STORAGE.insert(item)
      return

    cls.STORAGE.update({identifier: identifier_value}, item)



  @classmethod
  def change(cls, item):
    cls.create(item)  # TODO: ?

  @classmethod
  def remove(cls, item):
    if item is None:
      raise BaseException("DATA ERROR: Item is None")
    
    if not isinstance(item, cls.MODEL_CLASS):  # TODO: Work with dict?
      raise BaseException("DATA ERROR: Item is not a "+str(cls.MODEL_CLASS))
    
    try:
      for identifier, identifier_value in cls._get_key_fields_from_params(item.serialize()):
        item_found = cls.STORAGE.get({identifier: identifier_value})
        if item_found is not None:
          break

    except:
      raise BaseException("DATA ERROR: Item not found for remove ("+str(vars(item))+")")

    cls.STORAGE.delete({identifier: identifier_value})



  @classmethod
  def _get_data_raw(cls, **kwargs):
    for key in cls.MODEL_CLASS.KEYS:
      if key in kwargs:
        identifier = key
        break

    else:
      raise BaseException("DATA ERROR: No key provided ("+str(kwargs.keys())+")")
    
    item = cls.STORAGE.getRaw({identifier:kwargs[identifier]})
    return item



  @classmethod
  def _check_params_are_fields(cls, kwargs):
    field_set = set(cls.MODEL_CLASS.FIELDNAMES)
    args_set = set(kwargs.keys())

    unknown_fields = args_set-field_set

    if len(unknown_fields) == 1:
      raise BaseException("DATA ERROR: Field unexpected ("+str(unknown_fields)+")")
    elif len(unknown_fields) > 1:
      raise BaseException("DATA ERROR: Fields unexpected ("+str(unknown_fields)+")")



  @classmethod
  def _get_key_fields_from_params(cls, kwargs):
    for key in cls.MODEL_CLASS.KEYS:
      if key in kwargs and kwargs[key] is not None:
        yield (key, kwargs[key])

    else:
      raise BaseException("DATA ERROR: No key provided ("+str(kwargs.keys())+")")


AdapterBase.init()