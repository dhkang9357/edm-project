import re
import json
import folium
import MySQLdb
import statistics
from .database import Database
from . import weather, regression

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    class Meta:
        model = User
        fields = ("username", "email")

def index(request):
    user_id = str(request.user)

    if user_id == 'AnonymousUser':
        return HttpResponseRedirect('/login')

    user_info = get_user_info(user_id)

    if user_info['grade'] == 0:
        return render(request, 'app/index.html', user_info)

    return render(request, 'app/index_staff.html', user_info)

def load_location(request):
    db = Database.instance()

    query = 'SELECT location FROM EDMProject.LocationInfo;'
    location = db.run_query(query)
    return HttpResponse(json.dumps(location), content_type='text/json')

def load_city(request):
    pass

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

def get_default_position(location):
    db = Database.instance()

    query = 'SELECT y, x FROM EDMProject.LocationInfo where location = "{}";'.format(location)
    position = db.run_query(query)

    return position

def get_data(request):
    types = request.POST.getlist('type[]')
    location = request.POST.get('location')

    data = dict()
    data['map'] = get_map_data(types, location)
    data['fire'] = get_fire_data(location)
    data['regression'] = get_regression_data(location)
    data['widget'] = weather.get_weather_widget(location)

    return HttpResponse(json.dumps(data), content_type='text/json')

def get_regression_data(location):
    db = Database.instance()
    query = 'select firecount, humidity from fire where location="{}";'.format(location)
    row_data = db.run_query(query)

    X, Y = list(), list() # X: 화재건수, Y: 습도

    for _x, _y in row_data:
        X.append(_x)
        Y.append(_y)

    return regression.calculate(X, Y)


def get_fire_data(location):
    db = Database.instance()

    query = 'select location, month(date), sum(firecount) from fire where location="{}"  group by location, month(date);'.format(location)
    row_data = db.run_query(query)
    fire_data = [int(row[2]) / 2 for row in row_data]

    return fire_data

def get_map_data(types, location):
    db = Database.instance()

    function_map = {
        'Tree': assign_tree_data,
        'Asset': assign_asset_data,
    }

    default_position = get_default_position(location)

    map = folium.Map(location=default_position, zoom_start=10, width='100%', height='94.7%')

    for table in types:
        query = 'SELECT * FROM EDMProject.{} where location = "{}";'.format(table, location)
        info = db.run_query(query)

        assign = function_map[table]
        assign(map, info)

    return map._repr_html_()

def get_fire_info():
    pass

def get_user_info(user_id):
    db = Database.instance()
    query = "SELECT id, location, grade FROM EDMProject.UserInfo where id = '{}'".format(user_id)
    info = db.run_query(query)

    user_info = {
        'id': info[0],
        'location': info[1],
        'grade': info[2]
    }

    return user_info

def add_new_user(id, location):
    db = Database.instance()
    grade = 0
    query = "INSERT INTO UserInfo (`id`, `location`, `grade`) VALUES ('{}', '{}', '{}');".format(id, location, grade)
    db.run_query(query)

def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            location = request.POST.get('location')
            add_new_user(username, location)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'app/signup.html', {'form': form})