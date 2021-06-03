import MySQLdb

class Singleton:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance

class Database(Singleton):
    def __init__(self):
        self.host = '18.223.6.165'
        self.user = 'root'
        self.passwd = ''
        self.dbname = 'ProtectedForest'

        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.dbname, charset='utf8')

    def run_query(self, query, origin = False):
        cursor = self.connection.cursor()
        cursor.execute(query)
        ret = list(cursor.fetchall())
        ret = ret[0] if len(ret) == 1 else [r for r in ret]
        return ret