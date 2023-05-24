import pymysql
import datetime
import weather
email = "jung@gmail.com" ##################로그인할 아이디
pwd = "1234" #############로그인할 비번

now=datetime.datetime.now()
forecast=weather.main_data
db=pymysql.connect(host="",
user="root", password="",
charset="utf8", database="opsw")
cursor=db.cursor()



def mail_info(user_id):
    print("본문 내용 입력")
    text = input()
    sql="INSERT INTO mail_table(created_at,content,weather,user_id) VALUES(%s,%s,%s,%s)"
    val=(now,text,forecast,user_id)
    cursor.execute(sql, val)
    db.commit()


def sign_up():
    sql="INSERT INTO user_table(email,pwd,name,birthday,period) VALUES(%s,%s,%s,%s,%s)"
    print("이메일,비번,이름,생일,기간 입력")
    email=input()
    pwd=input()
    name=input()
    birthday=input()
    period=input()
    val=(email,pwd,name,birthday,period)
    cursor.execute(sql,val)
    db.commit()


def login(email, pwd):
    try:
        sql = "SELECT user_id FROM user_table WHERE email = %s AND pwd = %s"
        cursor.execute(sql, (email, pwd))
        result = cursor.fetchone()
        user_id=result[0]
        return user_id
    except:
        return False

#sign_up() #######################회원가입 

user_id=login(email,pwd)

#mail_info(user_id) ###################메일 작성

