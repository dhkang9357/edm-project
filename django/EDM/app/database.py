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
        self.dbname = 'EDMProject'

        # self.host = 'localhost'
        # self.user = 'root'
        # self.passwd = 'autoset'
        # self.dbname = 'edmproject'

        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.dbname, charset='utf8')

    def run_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        ret = cursor.fetchall()
        ret = ret[0] if len(ret) == 1 else [r for r in ret]

        if 'INSERT' in query:
          self.connection.commit()

        return ret