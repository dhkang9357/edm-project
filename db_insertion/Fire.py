import openpyxl
import DBManager

def parse(xml):
    pass

def main():
    file_path = 'C:\\Users\\Kang\\Desktop\\git\\edm-project\\db_insertion\\Firedata.xlsx'
    df = openpyxl.load_workbook(file_path)

    sheets_city = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종'] 
    sheets_island = ['경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주도']
    locations = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시', '세종특별자치시']

    table = 'Fire'
    columns = ['index', 'location', 'date', 'firecount', 'humidity']

    db = DBManager.DBManager()
    index = 5326

    for i, sheet in enumerate(sheets_island):
        data = df[sheet]
        location = sheet

        if sheet == '제주도':
            location = '제주특별자치도'

        field_data = zip(data['A'], data['B'], data['C'])

        for j, [date, firecount, humidity] in enumerate(field_data):
            if j < 2:
                continue

            if date.value == None:
                continue

            d = date.value.strftime("%Y-%m-%d")
            values = [index, location, d, firecount.value, humidity.value]

            db.insert_row(table, columns, values)

            index += 1

    # for i, sheet in enumerate(sheets_city):
    #     data = df[sheet]
    #     location = locations[i]

    #     field_data = zip(data['C'], data['D'], data['E'])

    #     for j, [date, firecount, humidity] in enumerate(field_data):
    #         if j == 0:
    #             continue

    #         if date.value == None:
    #             continue

    #         d = date.value.strftime("%Y-%m-%d")
    #         values = [index, location, d, firecount.value, humidity.value]

    #         db.insert_row(table, columns, values)

    #         index += 1

    db.close()

if __name__ == '__main__':
    main()
