import psycopg2
from psycopg2.extras import DictCursor
import os

print(os.environ)

class DatabaseConnException(Exception):
  pass

class DatabaseDataException(Exception):
  pass

class DB:
  __conn__ = None

  @classmethod
  def get_connection(cls):
    if cls.__conn__ is None:
      try:
        cls.__conn__ = get_connection()
      except Exception as ex:
        print( ex )
        cls.__conn__ = None

    return cls.__conn__

def get_connection():
  return psycopg2.connect(
    database=os.environ.get('PGSQL_WPCARE_DB','wpcare'),
    user=os.environ.get('PGSQL_WPCARE_USER','wpcare_user'),
    password=os.environ.get('PGSQL_WPCARE_PASSWORD',''),
    host=os.environ.get('PGSQL_WPCARE_HOST','localhost'),
    port=os.environ.get('PGSQL_WPCARE_PORT','5432'),
    cursor_factory=psycopg2.extras.DictCursor
  )

def check_database():
  try:
    get_connection()
  except Exception as ex:
    return 'Error DB: '+str(ex), 503
  else:
    return 'Success', 200