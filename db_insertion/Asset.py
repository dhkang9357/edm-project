import MySQLdb
import openpyxl
import DBManager

import requests
import xml.etree.ElementTree as ET

def check_validation(values):
    if '' in values:
        return False

    try:
        y = float(values[4])
        x = float(values[5])

        if y == 0 or x == 0:
            return False

    except:
        return False

    return True

def get_asset_info(id):
    if len(id) != 12:
        return None

    asset_type = id[:2]
    asset_id = id[2:10]
    asset_city = id[-2:]

    url = 'http://www.cha.go.kr/cha/SearchKindOpenapiDt.do?ccbaKdcd={}&ccbaAsno={}&ccbaCtcd={}'.format(asset_type, asset_id, asset_city)

    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.content

def parse(xml):
    tree = ET.fromstring(xml)

    location = tree.find('./item/ccbaCtcdNm').text.strip()
    name = tree.find('./item/ccbaMnm1').text.strip()
    x = tree.find('longitude').text.strip()
    y = tree.find('latitude').text.strip()
    address = tree.find('./item/ccbaLcad').text.strip()
    id = '{}-제{}호'.format(tree.find('ccbaKdcd').text.strip(), tree.find('./item/crltsnoNm').text.strip())

    return location, id, name, y, x, address

def main():
    file_path = 'C:\\Users\\Kang\\Desktop\\git\\edm-project\\db_insertion\\Assets.xlsx'
    df = openpyxl.load_workbook(file_path)

    data = df['문화재 정보']

    # 문화재코드
    field_data = data['A']
    index = 1

    table = 'Asset'
    columns = ['index', 'location', 'id', 'name', 'y', 'x', 'address']

    db = DBManager.DBManager()

    for i, code in enumerate(field_data):
        if i == 0:
            continue

        xml = get_asset_info(code.value)

        if xml is None:
            continue

        try:
            location, id, name, y, x, address = parse(xml)
        except:
            print('error')
            continue

        values = [index, location, id, name, y, x, address]

        if check_validation(values) is False:
            continue

        db.insert_row(table, columns, values)
        index += 1

        # if index == 5:
        #     break

    db.close()

if __name__ == '__main__':
    main()
