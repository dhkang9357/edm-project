import MySQLdb

class DBManager():
    def __init__(self):
        self.host = '18.223.6.165'
        self.user = 'root'
        self.passwd = ''
        self.dbname = 'EDMProject'

        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.dbname, charset='utf8')

    def insert_row(self, table, columns, values):
        cursor = self.connection.cursor()

        column = ', '.join(['`{}`'.format(c) for c in columns])
        value = ', '.join(["'{}'".format(v) for v in values])
        query = "INSERT INTO EDMProject.{} ({}) VALUES ({});".format(table, column, value)

        print(query)
        cursor.execute(query)

    def run_query(self, query, origin = False):
        cursor = self.connection.cursor()
        cursor.execute(query)
        ret = list(cursor.fetchall())
        return ret if origin else [r[0] for r in ret]

    def close(self):
        self.connection.commit()
        self.connection.close()