import os
import sys
import pymysql
from datetime import datetime
import smtplib
import weather
from email.mime.text import MIMEText
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QDate, Qt

db=pymysql.connect(host="localhost", user="root", password="0311",charset="utf8", database="opensource")
cursor=db.cursor()      #db 연결 객체
user_id = None
today_weather = weather.main_data
now = datetime.now().date()
pwd = 'lpyweewytdihlbpk'       # 메일을 전송해주는 중앙 서버 역할을 하는 이메일의 비번

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('start.ui')
form_class = uic.loadUiType(form)[0]
form_signup = resource_path('signup.ui')
form_signupclass = uic.loadUiType(form_signup)[0]
form_login = resource_path('login.ui')
form_loginclass = uic.loadUiType(form_login)[0]
form_main = resource_path('main.ui')
form_mainclass = uic.loadUiType(form_main)[0]
form_write = resource_path('write.ui')
form_writeclass = uic.loadUiType(form_write)[0]
form_mailbox = resource_path('mailbox.ui')
form_mailboxclass = uic.loadUiType(form_mailbox)[0]
form_my = resource_path('mypage.ui')
form_myclass = uic.loadUiType(form_my)[0]

def kor_weather(today_weather):
    if today_weather==0:
        return "뇌우"
    elif today_weather==1:
        return "비"
    elif today_weather==2:
        return "비"
    elif today_weather==3:
        return "눈"
    elif today_weather==4:
        return "안개"
    elif today_weather==5:
        return "안개"
    elif today_weather==6:
        return "황사"
    elif today_weather==7:
        return "안개"
    elif today_weather==8:
        return "맑음"
    elif today_weather==9:
        return "흐림"

class StartWidget(QDialog, QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.start_signupbutton.clicked.connect(self.signupclick)
        self.start_loginbutton.clicked.connect(self.loginclick)

    def signupclick(self):
        self.close()
        self.signup = SignupWidget()

    def loginclick(self):
        self.close()
        self.login = LoginWidget()


class SignupWidget(QDialog, QWidget, form_signupclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.signup_birth = self.findChild(QDateEdit, "signup_birth")
        self.signup_back.clicked.connect(self.signup_startclick2)
        self.signup_ok.clicked.connect(self.signup_startclick)

    def signup_startclick(self):
        sname = self.signup_name.text()
        smonth = self.signup_month.currentText()
        sday = self.signup_day.currentText()
        semail = self.signup_email.text()
        spwd = self.signup_pwd.text()
        speriod = self.signup_period.currentText()

        if speriod == '2주 뒤':
            speriod = 2
        elif speriod == '4주 뒤':
            speriod = 4
        elif speriod == '6주 뒤':
            speriod = 6
        elif speriod == '8주 뒤':
            speriod = 8
        elif speriod == '12주 뒤':
            speriod = 12

        if not sname or not semail or not spwd:
            popup = QMessageBox()
            popup.setWindowTitle("Error")
            popup.setText("빈칸을 채워주세요.")
            popup.setIcon(QMessageBox.Warning)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
        elif len(spwd) < 8:  # 비밀번호 길이가 8자 미만인지 확인
            popup = QMessageBox()
            popup.setWindowTitle("Error")
            popup.setText("비밀번호는 최소 8자 이상이어야 합니다.")
            popup.setIcon(QMessageBox.Warning)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
        else:
            if self.signup_db(sname, semail, spwd, smonth, sday, speriod):
                self.close()
                self.startback = StartWidget()

    def signup_startclick2(self):
        self.close()
        self.startback = StartWidget()

    def signup_db(self, sname, semail, spwd, smonth, sday, speriod):
        check_sql = "SELECT user_id FROM user_table where email = %s"
        #cursor.execute(check_sql, semail)
        cursor.execute(check_sql, (semail,))
        result = cursor.fetchone()
        if result is not None:      #같은 이메일로 등록된 정보가 있을 때
            popup = QMessageBox()
            popup.setWindowTitle("error")
            popup.setText("이미 등록된 이메일입니다.")
            popup.setIcon(QMessageBox.Warning)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
            return 0
        else:       #같은 이메일로 등록된 정보가 없을 때
            sql = "INSERT INTO user_table(email, pwd, name, birth, period) VALUES(%s, %s, %s, %s, %s)"
            val = (semail, spwd, sname, smonth + sday, speriod)
            cursor.execute(sql, val)
            db.commit()
            return 1


class LoginWidget(QDialog, QWidget, form_loginclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.login_back.clicked.connect(self.login_startclick)
        self.login_ok.clicked.connect(self.mainclick)

    def login_startclick(self):
        self.close()
        self.startback = StartWidget()

    def mainclick(self):
        login_email = self.login_email.text()
        login_pwd = self.login_pwd.text()
        if login_email:
            if login_pwd:
                global user_id
                user_id= self.login(login_email, login_pwd)
                if user_id is not None:
                    self.close()
                    self.main = MainWidget()
                else:
                    popup = QMessageBox()
                    popup.setWindowTitle("error")
                    popup.setText("아이디 또는 비밀번호를 잘못 입력했습니다.")
                    popup.setIcon(QMessageBox.Warning)
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.exec_()
            else:
                popup = QMessageBox()
                popup.setWindowTitle("error")
                popup.setText("비밀번호를 입력해주세요")
                popup.setIcon(QMessageBox.Warning)
                popup.setStandardButtons(QMessageBox.Ok)
                popup.exec_()
        else:
            popup = QMessageBox()
            popup.setWindowTitle("error")
            popup.setText("이메일을 입력해주세요")
            popup.setIcon(QMessageBox.Warning)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()

    def login(self, email, pwd):
        sql = "SELECT user_id FROM user_table WHERE email = %s AND pwd = %s"
        cursor.execute(sql, (email, pwd))
        result = cursor.fetchone()          #user_id 반환
        if result is not None:
            return result[0]
        else:
            return None


class MainWidget(QDialog, QWidget, form_mainclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.main_write.clicked.connect(self.mailclick)
        self.main_logout.clicked.connect(self.logoutclick)
        self.main_archive.clicked.connect(self.archiveclick)
        self.main_setup.clicked.connect(self.mypageclick)

    def mailclick(self):
        self.close()
        self.write = WriteWidget()

    def logoutclick(self):
        self.close()
        self.startback = StartWidget()

    def archiveclick(self):
        self.close()
        self.mailbox = MailboxWidget()

    def mypageclick(self):
        self.close()
        self.mypage = MypageWidget()

class WriteWidget(QDialog, QWidget, form_writeclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.write_ok.clicked.connect(self.sendclick)
        self.write_back.clicked.connect(self.sendback)
        self.dateEdit.setDate(QDate.currentDate())
        #self.weather12.setText(str(today_weather))
        if today_weather == 0:
            self.weather12.setStyleSheet("background-image : url(\'Thunderstorm.jpg\');")
        elif today_weather == 1 or today_weather == 2:
            self.weather12.setStyleSheet("background-image : url(\'Rain.jpg\');")
        elif today_weather == 3:
            self.weather12.setStyleSheet("background-image : url(\'Snow.jpg\');")
        elif today_weather == 4 or today_weather == 5 or today_weather == 7:
            self.weather12.setStyleSheet("background-image : url(\'Fog.jpg\');")
        elif today_weather == 6:
            self.weather12.setStyleSheet("background-image : url(\'Dust.jpg\');")
        elif today_weather == 8:
            self.weather12.setStyleSheet("background-image : url(\'Clear.jpg\');")
        else:
            self.weather12.setStyleSheet("background-image : url(\'Clouds.jpg\');")

    def sendclick(self):
        title = self.title_content.toPlainText()
        content = self.write_content.toPlainText()
        if not content:
            popup = QMessageBox()
            popup.setWindowTitle("error")
            popup.setText("메일 내용을 작성해주세요.")
            popup.setIcon(QMessageBox.Warning)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
        else:
            popup = QMessageBox()
            # mail_table에 데이터 삽입
            query = "INSERT INTO mail_table(created_at,title,content,weather,user_id) VALUES(%s,%s,%s,%s,%s)"
            val = (now, title, content, today_weather, user_id)
            cursor.execute(query, val)
            db.commit()
            self.check_and_send_mail(today_weather)
            popup.setWindowTitle("전송 완료")
            popup.setText("메일이 전송되었습니다.")
            popup.setIcon(QMessageBox.Information)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
            self.close()
            self.mainback = MainWidget()

    def timeover(self):
         query = "SELECT created_at FROM mail_table WHERE weather=%s AND user_id=%s AND send=False"
         cursor.execute(query, (today_weather, user_id))
         created_at = cursor.fetchone()[0]
         created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
         over = (now - created_at).days
         return over

    def send_mail(self, text, title,created_at,weather_2):
        query = "SELECT email FROM user_table WHERE user_id=%s"
        cursor.execute(query, (user_id,))
        email = cursor.fetchone()[0]
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login('yeoonjinParkofficial@gmail.com', pwd)
        msg = MIMEText(created_at+'\n'+weather_2+'\n\n'+text)
        msg['Subject'] = title
        smtp.sendmail('yeoonjinParkofficial@gmail.com', email, msg.as_string())
        smtp.quit()

    def check_and_send_mail(self,weather_2):
        korea_weather=kor_weather(weather_2)
        try:
            time_result = self.timeover()
            query = "SELECT period FROM user_table WHERE user_id=%s"
            cursor.execute(query, (user_id,))
            period = int(cursor.fetchone()[0])
            if time_result >= period * 7:
                query = "SELECT content FROM mail_table WHERE weather=%s AND user_id=%s AND send=False"
                cursor.execute(query, (today_weather, user_id))
                result = cursor.fetchone()
                query4 = "SELECT title,created_at FROM mail_table WHERE weather=%s AND user_id=%s AND send=False"
                cursor.execute(query4, (today_weather, user_id))
                ret4=cursor.fetchone()
                title=ret4[0]
                created_at=ret4[1]
                text = result[0] if result else None
                if text:
                    self.send_mail(text, title,created_at,korea_weather)
                else:
                    print("데이터를 사용할 수 없습니다.")

                query2 = "SELECT mail_id FROM mail_table WHERE weather=%s AND user_id=%s AND send=False"
                cursor.execute(query2, (today_weather, user_id))
                select_mail_id = cursor.fetchone()
                selected = select_mail_id[0]

                query3 = "UPDATE mail_table SET send=True WHERE mail_id=%s"
                cursor.execute(query3, (selected,))
                db.commit()
        except:
            return 0
    def sendback(self):
        self.close()
        self.mainback = MainWidget()

class MailboxWidget(QDialog, QWidget, form_mailboxclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        # 행 간격 조정
        self.tableWidget.setStyleSheet("QTableView::item { margin: 10px; }")

        # 메일 목록 로드
        self.load_mails()

    def load_mails(self):
        # 메일 목록을 로드하는 로직 구현
        # 예시로 메일 목록을 추가하는 코드를 작성합니다.
        mails = [("2023-05-01", "Sunny", "Title 1", "Sent"),
                 ("2023-05-02", "Rainy", "Title 2", "Sent"),
                 ("2023-05-03", "Cloudy", "Title 3", "Not Sent")]

        # 테이블 위젯에 메일 목록 표시
        self.tableWidget.setRowCount(len(mails))
        for i, (date, weather, title, status) in enumerate(mails):
            item_date = QTableWidgetItem(date)
            item_weather = QTableWidgetItem(weather)
            item_title = QTableWidgetItem(title)
            item_status = QTableWidgetItem(status)
            self.tableWidget.setItem(i, 0, item_date)
            self.tableWidget.setItem(i, 1, item_weather)
            self.tableWidget.setItem(i, 2, item_title)
            self.tableWidget.setItem(i, 3, item_status)

class MypageWidget(QDialog, QWidget, form_myclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = StartWidget()
    myWindow.show()
    app.exec_()
