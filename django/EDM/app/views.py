import re
import json
import folium
import MySQLdb
import statistics
from .database import Database

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # return render(request, 'app/index.html')
    return render(request, 'app/index_staff.html')

def load_location(request):
    db = Database.instance()

    query = 'SELECT location FROM EDMProject.LocationInfo;'
    location = db.run_query(query)
    print(location)
    return HttpResponse(json.dumps(location), content_type='text/json')

def load_city(request):
    pass
#     location = request.POST.get('location')
#     print(location)
#     db = Database.instance()

#     query = 'SELECT distinct(firelocation) FROM ProtectedForest.SearchedLocation2 where SearchedCity = "{}" and firelocation != "";'.format(location)
#     location = db.run_query(query)
#     print(location)
#     return HttpResponse(json.dumps(location), content_type='text/json')

def assign_tree_data(map, info):
    for index, location, id, type, y, x, address in info:
        if y == 0 or x == 0:
            continue

        desc = '보호수 종류: {}<br>보호수 지정번호: {}<br>주소: {}'.format(type, id, address)
        popup = folium.Popup(desc, min_width=200, max_width=400)
        folium.Marker(location=[y, x], popup=popup, icon=folium.Icon(color="green", icon="info-sign")).add_to(map)

    return

def assign_asset_data(map, info):
    category_type = {
        11 : '국보',
        12 : '보물',
        13 : '사적',
        14 : '사적및명승',
        15 : '명승',
        16 : '천연기념물',
        17 : '국가무형문화재',
        18 : '국가민속문화재',
        21 : '시도유형문화재',
        22 : '시도무형문화재',
        23 : '시도기념물',
        24 : '시도민속문화재',
        31 : '문화재자료',
        79 : '등록문화재',
        80 : '이북5도 무형문화재'
    }

    for index, location, id, name, y, x, address in info:
        category, number = int(id.split('-')[0]), id.split('-')[1:]
        id = '{}-{}'.format(category_type[category], ''.join(number))

        desc = '문화재명: {}<br>문화재 지정번호: {}<br>주소: {}'.format(name, id, address)
        popup = folium.Popup(desc, min_width=200, max_width=600)
        folium.Marker(location=[y, x], popup=popup, icon=folium.Icon(color="red", icon="info-sign")).add_to(map)

    return

def assign_fire_data(map, info):
    pass

def get_default_position(location):
    db = Database.instance()

    query = 'SELECT y, x FROM EDMProject.LocationInfo where location = "{}";'.format(location)
    position = db.run_query(query, True)

    return position

def load_map(request):
    types = request.POST.getlist('type[]')
    location = request.POST.get('location')

    db = Database.instance()

    print(types, location)

    function_map = {
        'Tree': assign_tree_data,
        'Asset': assign_asset_data,
        'Fire': assign_fire_data
    }

    default_position = get_default_position(location)

    map = folium.Map(location=default_position, zoom_start=11, width='100%', height='94.7%')

    for table in types:
        query = 'SELECT * FROM EDMProject.{} where location = "{}";'.format(table, location)
        print(query)
        info = db.run_query(query, True)

        assign = function_map[table]
        assign(map, info)

    # db = Database.instance()

    # query = 'SELECT ForestLatitude, ForestLongitude FROM ProtectedForest.SearchedLocation2 where searchedCity = "{}" and Firelocation = "{}";'.format(location, city)
    # positions = db.run_query(query, True)

    # print(positions)

    # position_y = [y for y, _ in positions]
    # position_x = [x for y, x in positions]

    # mean_y = min(position_y) + ((max(position_y) - min(position_y)) / 2)
    # mean_x = min(position_x) + ((max(position_x) - min(position_x)) / 2)

    # for y, x in positions:
    #     popup = folium.Popup('y: {}, x: {}'.format(y, x), min_width=200, max_width=400)
    #     folium.Marker(location=[y, x], popup=popup).add_to(map)

    return HttpResponse(map._repr_html_(), content_type='text/html')