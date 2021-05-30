import re
import json
import folium
import MySQLdb
import statistics
from .database import Database

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'app/index.html')

def load_location(request):
    db = Database.instance()

    query = 'SELECT distinct(SearchedCity) FROM ProtectedForest.SearchedLocation2;'
    location = db.run_query(query)
    print(location)
    return HttpResponse(json.dumps(location), content_type='text/json')

def load_city(request):
    location = request.POST.get('location')
    print(location)
    db = Database.instance()

    query = 'SELECT distinct(firelocation) FROM ProtectedForest.SearchedLocation2 where SearchedCity = "{}" and firelocation != "";'.format(location)
    location = db.run_query(query)
    print(location)
    return HttpResponse(json.dumps(location), content_type='text/json')

def load_map(request):
    location = request.POST.get('location')
    city = request.POST.get('city')

    db = Database.instance()

    query = 'SELECT ForestLatitude, ForestLongitude FROM ProtectedForest.SearchedLocation2 where searchedCity = "{}" and Firelocation = "{}";'.format(location, city)
    positions = db.run_query(query, True)

    print(positions)

    position_y = [y for y, _ in positions]
    position_x = [x for y, x in positions]

    mean_y = min(position_y) + ((max(position_y) - min(position_y)) / 2)
    mean_x = min(position_x) + ((max(position_x) - min(position_x)) / 2)

    map = folium.Map(location=[mean_y, mean_x], zoom_start=11, width='100%', height='94.7%')

    for y, x in positions:
        popup = folium.Popup('y: {}, x: {}'.format(y, x), min_width=200, max_width=400)
        folium.Marker(location=[y, x], popup=popup).add_to(map)

    return HttpResponse(map._repr_html_(), content_type='text/html')