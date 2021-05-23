import re
import json
import folium
import MySQLdb

from django.shortcuts import render
from django.http import HttpResponse

class Database():
    def __init__(self):
        self.connection = None
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'autoset'
        self.dbname = 'dhkang1'

    def connect(self):
        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.dbname)

    def run_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

def index(request):
    return render(request, 'app/index.html')

def load_map(request):
    location = [37.283103, 127.044878]

    db = Database()
    db.connect()

    # t = db.run_query('SELECT * FROM dhkang1.test_table where name = "아주대학교";')
    # print(type(t))
    
    map = folium.Map(location=location, zoom_start=16)
    popup = folium.Popup('경기도 수원시 영통구 월드컵로 206', min_width=200, max_width=400)
    folium.Marker(location=location, popup=popup).add_to(map)

    return HttpResponse(map._repr_html_(), content_type='text/html')