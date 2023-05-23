import pymysql
import getweather
import datetime

now = datetime.datetime.now().date()
forecast = getweather.main_data

db = pymysql.connect(host="localhost",
user="root", password="gaga0223",
charset="utf8", database="opensw")

cursor = db.cursor()

'''
def mail_info():
    text = input()
    sql = "INSERT INTO mail_table(created_at,content,weather) VALUES(%s,%s,%s)"
    val = (now, text, forecast)
    cursor.execute(sql, val)
    db.commit()


def user_info():
    sql = "INSERT INTO user_table(email,pwd,name,birthday,period) VALUES(%s,%s,%s,%s,%s)"
    email = input()
    pwd = input()
    name = input()
    birthday = input()
    period = input()
    val = (email, pwd, name, birthday, period)
    cursor.execute(sql, val)
    db.commit()


print("이메일,비번,이름,생일,기간 입력")
user_info()

print("본문 내용 입력")
mail_info()

'''


sql2 = "SELECT period FROM user_table"
cursor.execute(sql2)
period_result = cursor.fetchall()

periods = []
for row in period_result:
    period = int(row[0])
    periods.append(period)


sql = "SELECT created_at FROM mail_table"
cursor.execute(sql)
created_at_result = cursor.fetchall()
new_dates = []

for i, row in enumerate(created_at_result):
    created_at = datetime.datetime.strptime(row[0], '%Y-%m-%d')
    period = periods[i % len(periods)]  # periods 배열에서 해당 인덱스에 대응하는 값을 가져오기
    new_date = created_at + datetime.timedelta(days=7 * period)
    new_dates.append(new_date)


# for date in new_dates:
#    print(date)







