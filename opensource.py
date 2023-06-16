import os
import sys
import pymysql
from datetime import datetime
import smtplib
import weather
import random
from email.mime.text import MIMEText
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon

db=pymysql.connect(host="localhost", user="root", password="0509",charset="utf8", database="opensource")
cursor=db.cursor()                      #db 연결 객체
user_id = None
today_weather = weather.main_data
now = datetime.now().date()
pwd = 'lpyweewytdihlbpk'                # 메일을 전송해주는 중앙 서버 역할을 하는 이메일의 비번

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

def kor_weather(weather):
    if weather==0:
        return "뇌우"
    elif weather==1:
        return "비"
    elif weather==2:
        return "비"
    elif weather==3:
        return "눈"
    elif weather==4:
        return "안개"
    elif weather==5:
        return "안개"
    elif weather==6:
        return "황사"
    elif weather==7:
        return "안개"
    elif weather==8:
        return "맑음"
    elif weather==9:
        return "흐림"



class StartWidget(QDialog, QWidget, form_class):                    #시작 화면
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨우체통")
        self.setWindowIcon(QIcon('postbox5.png'))
        self.show()

        self.start_signupbutton.clicked.connect(self.signupclick)   #회원가입 클릭
        self.start_loginbutton.clicked.connect(self.loginclick)     #로그인 클릭

    def signupclick(self):
        self.close()
        self.signup = SignupWidget()

    def loginclick(self):
        self.close()
        self.login = LoginWidget()



class SignupWidget(QDialog, QWidget, form_signupclass):             #회원가입 화면
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨우체통")
        self.setWindowIcon(QIcon('postbox5.png'))
        self.show()

        self.signup_birth = self.findChild(QDateEdit, "signup_birth")
        self.signup_ok.clicked.connect(self.signup_startclick)      #회원가입 클릭
        self.signup_back.clicked.connect(self.signup_startclick2)   #뒤로가기 클릭



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

        if not sname or not semail or not spwd:                 #하나라도 공백일 때
            popup = QMessageBox()
            popup.setWindowTitle("Error")
            popup.setText("빈칸을 채워주세요.")
            popup.setIcon(QMessageBox.Warning)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
        elif len(spwd) < 8:                                     #비밀번호 8자리 이하일 때
            popup = QMessageBox()
            popup.setWindowTitle("Error")
            popup.setText("비밀번호는 최소 8자 이상이어야 합니다.")
            popup.setIcon(QMessageBox.Warning)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
        else:
            if self.signup_db(sname, semail, spwd, smonth, sday, speriod):
                popup = QMessageBox()
                popup.setWindowTitle("환영합니다!")
                popup.setText("회원가입이 완료되었습니다.")
                popup.setIcon(QMessageBox.Information)
                popup.setStandardButtons(QMessageBox.Ok)
                popup.exec_()
                self.close()
                self.startback = StartWidget()

    def signup_startclick2(self):
        self.close()
        self.startback = StartWidget()

    def signup_db(self, sname, semail, spwd, smonth, sday, speriod):
        check_sql = "SELECT user_id FROM user_table where email = %s"
        cursor.execute(check_sql, (semail,))
        result = cursor.fetchone()
        if result is not None:                                  #같은 이메일로 등록된 정보가 있을 때
            popup = QMessageBox()
            popup.setWindowTitle("error")
            popup.setText("이미 등록된 이메일입니다.")
            popup.setIcon(QMessageBox.Warning)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
            return 0
        else:                                                   #같은 이메일로 등록된 정보가 없을 때
            sql = "INSERT INTO user_table(email, pwd, name, birth, period) VALUES(%s, %s, %s, %s, %s)"
            val = (semail, spwd, sname, smonth + sday, speriod)
            cursor.execute(sql, val)
            db.commit()
            return 1



class LoginWidget(QDialog, QWidget, form_loginclass):           #로그인 화면
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨우체통")
        self.setWindowIcon(QIcon('postbox5.png'))
        self.show()

        self.login_back.clicked.connect(self.login_startclick)
        self.login_ok.clicked.connect(self.mainclick)

    def login_startclick(self):
        self.close()
        self.startback = StartWidget()

    def mainclick(self):
        login_email = self.login_email.text()
        login_pwd = self.login_pwd.text()
        if login_email:                                         #로그인 입력
            if login_pwd:                                       #비밀번호 입력
                global user_id
                user_id= self.login(login_email, login_pwd)     #user id 받아옴
                if user_id is not None:                         #user id 있다면 -> 메인 화면으로
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
        result = cursor.fetchone()                          #user_id 반환
        if result is not None:
            return result[0]
        else:
            return None



class MainWidget(QDialog, QWidget, form_mainclass):         #메인화면
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨우체통")
        self.setWindowIcon(QIcon('postbox5.png'))
        self.show()

        self.main_write.clicked.connect(self.mailclick)
        self.main_logout.clicked.connect(self.logoutclick)
        self.main_archive.clicked.connect(self.mailboxclick)
        self.main_setup.clicked.connect(self.mypageclick)

    def mailclick(self):
        self.close()
        self.write = WriteWidget()

    def logoutclick(self):
        self.close()
        self.startback = StartWidget()

    def mailboxclick(self):
        self.close()
        self.mailbox = MailboxWidget()

    def mypageclick(self):
        self.close()
        self.mypage = MypageWidget()



class WriteWidget(QDialog, QWidget, form_writeclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨우체통")
        self.setWindowIcon(QIcon('postbox5.png'))
        self.show()
        self.write_ok.clicked.connect(self.sendclick)
        self.write_back.clicked.connect(self.sendback)
        today = datetime.now()
        todayshow1 = today.strftime("%Y년 %m월 %d일")
        self.todayshow.setText(str(todayshow1))
        # self.dateEdit.setDate(QDate.currentDate())
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

            import time

            # 전송 중임을 알리는 팝업 표시
            loading_popup = QMessageBox()
            loading_popup.setIcon(QMessageBox.Information)
            loading_popup.setWindowTitle("전송 중")
            loading_popup.setText("메일을 전송 중입니다.")
            loading_popup.setStandardButtons(QMessageBox.NoButton)  # 버튼을 보이지 않도록 설정
            loading_popup.show()
            QApplication.processEvents()  # 팝업 표시를 갱신하기 위해 이벤트 루프를 실행

            # birthday_mail() 메소드 실행
            self.birthday_mail()
            self.check_and_send_mail(today_weather)

            # 전송 완료 팝업 표시
            loading_popup.hide()  # 전송 중 팝업 숨기기

            # 전송 완료를 알리는 팝업 표시
            popup.setIcon(QMessageBox.Information)
            popup.setWindowTitle("전송 완료")
            popup.setText("메일이 전송되었습니다.")
            popup.setStandardButtons(QMessageBox.Ok)  # OK 버튼을 다시 보이도록 설정
            popup.exec_()

            self.close()
            self.mainback = MainWidget()


    def send_mail(self, title, text, created_at, weather_2):
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
            self.update_ok()
            query = "SELECT title FROM mail_table WHERE weather=%s AND user_id=%s AND send=False AND ok=True"
            cursor.execute(query, (weather_2, user_id))
            result = cursor.fetchall()
            title = random.choice(result)[0] if result else None
            query4 = "SELECT content, created_at FROM mail_table WHERE weather=%s AND user_id=%s AND title=%s AND send=False"
            cursor.execute(query4, (weather_2, user_id, title))
            result_4 = cursor.fetchone()
            text = result_4[0]
            created_at = result_4[1]
            self.send_mail(title, text, created_at, korea_weather)
            query3 = "UPDATE mail_table SET send=True WHERE content=%s AND title=%s AND weather=%s AND send=False"
            cursor.execute(query3, (text, title, weather_2))
            db.commit()

        except:
            return 0

    def update_ok(self):
        query = f"SELECT period FROM user_table WHERE user_id=%s"
        cursor.execute(query, (user_id,))
        period = int(cursor.fetchone()[0])
        period = period * 7
        query = "UPDATE mail_table SET ok = True WHERE user_id = %s AND DATEDIFF(%s, created_at) >= %s"
        cursor.execute(query, (user_id, now, period))
        db.commit()

    def birthday_mail(self):
        query="SELECT birth,name,email,surprise FROM user_table WHERE user_id=%s"
        cursor.execute(query, (user_id,))
        ret=cursor.fetchone()
        formatted_date = now.strftime("%m%d")
        birthday=ret[0]
        name=ret[1]
        email=ret[2]
        birthok=ret[3]
        print(birthday, name, email, birthok)
        if formatted_date==birthday:
            if birthok == 0:
                query = "UPDATE user_table SET surprise=True WHERE user_id=%s"
                cursor.execute(query, (user_id,))
                smtp = smtplib.SMTP('smtp.gmail.com', 587)
                smtp.starttls()
                smtp.login('yeoonjinParkofficial@gmail.com', pwd)
                text=f'생일축하해 {name}~\n생일선물은 나야.\n알아들었으면 끄덕여'
                msg = MIMEText(text)
                msg['Subject'] = f'생일축하합니다 {name}님 !!'
                smtp.sendmail('yeoonjinParkofficial@gmail.com', email, msg.as_string())
                smtp.quit()

    def sendback(self):
        self.close()
        self.mainback = MainWidget()



class MailboxWidget(QDialog, QWidget, form_mailboxclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨우체통")
        self.setWindowIcon(QIcon('postbox5.png'))
        self.show()

        self.tableWidget.setStyleSheet("QTableView::item { margin: 10px; }")
        self.load_mails()
        self.write_back.clicked.connect(self.writeback)

    def load_mails(self):
        # 테이블 위젯에 메일 목록 표시
        query = "SELECT created_at, weather, title, send FROM mail_table WHERE user_id=%s"
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        self.tableWidget.setColumnWidth(0, 145)
        self.tableWidget.setColumnWidth(1, 75)
        self.tableWidget.setColumnWidth(2, 360)
        self.tableWidget.setColumnWidth(3, 75)
        self.tableWidget.setRowCount(len(results))
        for i, result in enumerate(results):
            item_date = QTableWidgetItem(result[0])
            weather_text = kor_weather(result[1])
            item_weather = QTableWidgetItem(weather_text)
            item_title = QTableWidgetItem(result[2])
            bool_mapping = {
                True: " ♥",
                False: " ♡"
            }
            status = bool_mapping.get(result[3])
            item_status = QTableWidgetItem(status)

            self.tableWidget.setItem(i, 0, item_date)
            self.tableWidget.setItem(i, 1, item_weather)
            self.tableWidget.setItem(i, 2, item_title)
            self.tableWidget.setItem(i, 3, item_status)
        self.tableWidget.setStyleSheet("background-color: white;")

    def writeback(self):
        self.close()
        self.mainback2 = MainWidget()



class MypageWidget(QDialog, QWidget, form_myclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨우체통")
        self.setWindowIcon(QIcon('postbox5.png'))
        self.show()

        query = "SELECT name FROM user_table WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        name = cursor.fetchone()[0]  # 튜플에서 첫 번째 요소인 이름을 추출
        query1 = "SELECT email FROM user_table WHERE user_id = %s"
        cursor.execute(query1, (user_id,))
        email = cursor.fetchone()[0]  # 튜플에서 첫 번째 요소인 이메일을 추출
        self.name.setText(name)
        self.email.setText(email)
        self.mypage_back.clicked.connect(self.backclick)
        self.change.clicked.connect(self.update_user_info)
        self.leave.clicked.connect(self.delete_user)

    def backclick(self):
        self.close()
        self.main = MainWidget()

    def update_user_info(self):
        change_pwd = self.change_pwd.text()
        change_period = self.change_period.currentText()

        if change_period == '2주 뒤':
            change_period = 2
        elif change_period == '4주 뒤':
            change_period = 4
        elif change_period == '6주 뒤':
            change_period = 6
        elif change_period == '8주 뒤':
            change_period = 8
        elif change_period == '12주 뒤':
            change_period = 12

        if not change_pwd or not change_period:
            popup = QMessageBox()
            popup.setWindowTitle("Error")
            popup.setText("빈칸을 채워주세요.")
            popup.setIcon(QMessageBox.Warning)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
        elif len(change_pwd) < 8:
            popup = QMessageBox()
            popup.setWindowTitle("Error")
            popup.setText("비밀번호는 8자 이상 입력해주세요.")
            popup.setIcon(QMessageBox.Warning)
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
        else:
                self.set_pwd(change_pwd)  # 비밀번호 업데이트
                self.set_period(change_period)  # 기간 업데이트
                popup = QMessageBox()
                popup.setWindowTitle("변경 완료")
                popup.setText("정보가 성공적으로 업데이트되었습니다.")
                popup.setIcon(QMessageBox.Information)
                popup.setStandardButtons(QMessageBox.Ok)
                popup.exec_()

                self.close()
                self.change = MainWidget()

    def set_pwd(self, password):
        query = "UPDATE user_table SET pwd=%s WHERE user_id=%s"
        cursor.execute(query, (password, user_id))
        db.commit()

    def set_period(self, due_date):
        query = "UPDATE user_table SET period='%s' WHERE user_id=%s"
        cursor.execute(query, (due_date, user_id))
        period = due_date * 7
        query = "UPDATE mail_table SET ok = True WHERE user_id = %s AND DATEDIFF(%s, created_at) >= %s"
        cursor.execute(query, (user_id, now, period))
        query = "UPDATE mail_table SET ok = False WHERE user_id = %s AND DATEDIFF(%s, created_at) < %s"
        cursor.execute(query, (user_id, now, period))
        db.commit()

    def delete_user(self):
        query1 = "DELETE FROM user_table WHERE user_id=%s"
        cursor.execute(query1, (user_id,))
        query2 = "DELETE FROM mail_table WHERE user_id=%s"
        cursor.execute(query2, (user_id,))
        db.commit()
        popup = QMessageBox()
        popup.setWindowTitle("탈퇴 완료")
        popup.setText("회원 탈퇴가 완료되었습니다.")
        popup.setIcon(QMessageBox.Information)
        popup.setStandardButtons(QMessageBox.Ok)
        popup.exec_()
        self.close()
        self.change = StartWidget()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = StartWidget()
    myWindow.show()
    app.exec_()
