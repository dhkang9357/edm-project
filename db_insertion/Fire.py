import openpyxl
import DBManager

def parse(xml):
    pass

def main():
    file_path = 'C:\\Users\\Kang\\Desktop\\git\\edm-project\\db_insertion\\Fire2019.xlsx'
    df = openpyxl.load_workbook(file_path)

    sheets = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주도']

    table = 'LocationInfo'
    columns = ['index', 'location', 'y', 'x', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    db = DBManager.DBManager()

    index = 1
    for sheet in sheets:
        data = df[sheet]

        month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i, a in enumerate(data['A']):
            if i == 0:
                continue

            month[a.value.month] += 1

        location = data['B'][1].value
        print(location, month)

        values = [index, location, 0, 0] + month[1:]

        db.insert_row(table, columns, values)
        index += 1

    db.close()

if __name__ == '__main__':
    main()
