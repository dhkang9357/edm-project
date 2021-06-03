import MySQLdb
import openpyxl
import DBManager

def check_validation(values):
    if '' in values:
        return False

    try:
        float(values[4])
        float(values[5])
    except:
        return False

    return True

file_path = 'C:\\Users\\Kang\\Desktop\\git\\edm-project\\db_insertion\\Trees.xlsx'
df = openpyxl.load_workbook(file_path)

data = df['검색지역(시도명)']

# 시도명, 지정번호, 나무종류, 위도, 경도, 도로명주소, 지번주소
field_data = zip(data['B'], data['E'], data['K'], data['W'], data['X'], data['U'], data['V'])
index = 1

table = 'Tree'
columns = ['index', 'location', 'id', 'type', 'y', 'x', 'address']

db = DBManager.DBManager()

for i, [location, id, tree_type, y, x, new_addr, old_addr] in enumerate(field_data):
    if i == 0:
        continue

    if new_addr.value == '' and old_addr.value == '':
        continue

    addr = new_addr.value if new_addr.value != '' else old_addr.value

    values = [index, location.value, id.value, tree_type.value, y.value, x.value, addr]

    if check_validation(values) is False:
        continue

    db.insert_row(table, columns, values)
    index += 1

db.close()