from wpcare.jsonCrud import JsonCrud, _check_parameters, _search_condition

'''
Methods:
  - JsonNamedCrud( entity, entity_class, auto_commit?, key_attr )
  - open()
  - close()
  - get(search)
  - count(search)
  - select(search)
  - insert(data)
  - update(search, data)
  - delete(search)
  - getRaw(search)
'''

class JsonNamedCrud(JsonCrud):
  def __init__(self, entity, entity_class, auto_commit=False, key_attr='id'):
    super().__init__(entity, auto_commit, key_attr)

    self.entity_class = entity_class



  def get(self, *args, **kwargs):
    data = super().get(*args, **kwargs)

    return self.entity_class(data) if data is not None else None
  


  def getRaw(self, *args, **kwargs):
    data = super().get(*args, **kwargs)

    return data



  def select(self, *args, **kwargs):
    data = _check_parameters(args, kwargs)

    item_generator = (self.entity_class(item) for item in self.cache if _search_condition(data, item))

    return item_generator
  


  def insert(self, *args, **kwargs):
    data = _check_parameters(args, kwargs)

    if isinstance(data, self.entity_class):
      raw_data = data.serialize()

      if self.config['key'] in raw_data and raw_data[self.config['key']] is None:
        del raw_data[self.config['key']]

      key_id = super().insert(raw_data)

      if hasattr(data, self.config['key']):
        setattr(data, self.config['key'], key_id)

      return key_id
    
    elif isinstance(data, dict):
      key_id = super().insert(data)

      return key_id



  def update(self, data_search_or_object, data_update):

    if isinstance(data_search_or_object, self.entity_class):
      raw_data = data_search_or_object.serialize()

      if self.config['key'] in raw_data and raw_data[self.config['key']] is not None:
        super().update({self.config['key']: raw_data[self.config['key']]}, raw_data)

        return data_search_or_object
      else:
        # Upsert?
        pass

    elif isinstance(data_search_or_object, dict):

      if isinstance(data_update, self.entity_class):
        raw_data = data_update.serialize()

        if self.config['key'] in raw_data:
          del raw_data[self.config['key']]

        updated_items = super().update(data_search_or_object, raw_data)

        return (self.entity_class(item) for item in updated_items)

      elif isinstance(data_update, dict):
        updated_items = super().insert(data_search_or_object, data_update)

        return updated_items # TODO: Cast dict into object?



  def delete(self, *args, **kwargs):
    data = _check_parameters(args, kwargs)

    if isinstance(data, self.entity_class):
      raw_data = data.serialize()

      if self.config['key'] in raw_data:
        removed_items = super().delete({self.config['key']: raw_data[self.config['key']]})

      else:
        removed_items = super().delete(raw_data)

      return (self.entity_class(item) for item in removed_items)

    else:
      removed_items = super().delete(*args, **kwargs)

      return (self.entity_class(item) for item in removed_items) # TODO: Cast dict into object?
