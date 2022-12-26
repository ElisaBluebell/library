import csv
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainProgram(QWidget):

    def __init__(self):
        super().__init__()
        self.initui()

    # ui 설정
    def initui(self):
        # 필요 변수 선언
        self.data_list = []
        self.result_list = []
        self.selected_row = []

        # 페이지 세팅
        self.set_labels()
        self.set_buttons()
        self.set_lines()

        # 기능 실행
        self.open_data()
        self.set_table()
        self.search_data()

        # 프로그램 기본사항
        self.setWindowTitle("카센터 정보관리")
        self.setGeometry(0, 0, 800, 600)
        self.show()

    # 라벨 세팅
    def set_labels(self):
        # 이름 라벨
        self.name_label = QLabel('이름', self)
        # 라벨의 위치와 크기 설정
        self.name_label.setGeometry(120, 100, 50, 20)

        # 지역 라벨
        self.location_label = QLabel('지역', self)
        self.location_label.setGeometry(370, 100, 50, 20)

    # 버튼 세팅
    def set_buttons(self):
        # 종료 버튼
        self.quit_btn = QPushButton('종료', self)
        self.quit_btn.setGeometry(720, 560, 50, 20)
        # 시그널을 통한 연결 설정
        self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

        # 조회 버튼
        self.search_btn = QPushButton('조회', self)
        self.search_btn.setGeometry(640, 100, 50, 20)
        self.search_btn.clicked.connect(self.search_data)

        # 저장 버튼
        self.save_btn = QPushButton('저장', self)
        self.save_btn.setGeometry(710, 100, 50, 20)
        self.save_btn.clicked.connect(self.save_data)

    # 라인에딧 설정
    def set_lines(self):
        # 업체명 입력칸
        self.search_name = QLineEdit(self)
        self.search_name.move(160, 100)
        # 엔터 키를 통한 작동 추가
        self.search_name.returnPressed.connect(self.search_data)
        
        # 지역 입력칸
        self.search_location = QLineEdit(self)
        self.search_location.move(410, 100)
        self.search_location.returnPressed.connect(self.search_data)

    # 데이터 삽입
    def open_data(self):
        # csv 파일 오픈
        f = open('carcenter_data.csv', 'r', encoding='UTF-8')
        reader = csv.reader(f)
        for line in reader:
            # self.data_list에 저장함
            self.data_list.append(line)
        f.close()

    # 검색 기능(for문 안에 큰 if문들을 넣으니 오류 발생)
    def search_process(self):
        # 결과값 초기화
        self.result_list = []
        # 경우별 결과값 삽입, 둘 다 비어있는 경우
        if not self.search_location.text() and not self.search_name.text():
            for i in range(len(self.data_list)):
                if i != 0:
                    # data_list에 연번의 역할을 할 숫자를 추가
                    self.data_list[i].append(i)
                    # 결과값은 기본 데이터와 동일함
                    self.result_list.append(self.data_list[i])
        # 로케이션 라인에딧이 비어있는 경우
        elif not self.search_location.text():
            # 이름 라인을 csv를 통해 받아온 데이터와 대조하여
            for i in range(len(self.data_list)):
                if self.search_name.text() in self.data_list[i][0]:
                    # 결과값에 추가함
                    print(self.data_list[i])
                    self.result_list.append(self.data_list[i])
        # 이름 라인이 비어있는 경우
        elif not self.search_name.text():
            for i in range(len(self.data_list)):
                if self.search_location.text() in self.data_list[i][2]:
                    self.result_list.append(self.data_list[i])
        # 둘 다 차있는 경우
        else:
            # 두가지 모두를 기본 데이터와 비교 후
            for i in range(len(self.data_list)):
                    if self.search_location.text() in self.data_list[i][2] and \
                            self.search_name.text() in self.data_list[i][0]:
                        # 대입함
                        self.result_list.append(self.data_list[i])
        # 명칭 재설정
        for i in range(len(self.result_list)):
            # 급수 통일, 01, 1 등으로 통일되지 않았으며 이용자가 알아보기 힘들기 때문에 각 급에 해당하는 정식 명칭 입력
            if self.result_list[i][1] == '01' or self.result_list[i][1] == '1':
                self.result_list[i][1] = '자동차종합정비업'
            if self.result_list[i][1] == '02' or self.result_list[i][1] == '2':
                self.result_list[i][1] = '소형자동차정비업'
            if self.result_list[i][1] == '03' or self.result_list[i][1] == '3':
                self.result_list[i][1] = '자동차전문정비업'
            if self.result_list[i][1] == '04' or self.result_list[i][1] == '4':
                self.result_list[i][1] = '원동기전문정비업'
            if self.result_list[i][1] == '99':
                self.result_list[i][1] = '기타'

    # 표 생성
    def set_table(self):
        self.data_table = QTableWidget(self)
        # 표의 크기는 csv 파일 헤드라벨의 갯수를 제해야 하므로 data_list의 길이 - 1
        self.data_table.setRowCount(len(self.result_list) - 1)
        # 표를 통해서는 6가지의 값을 출력할 것임
        self.data_table.setColumnCount(6)
        self.data_table.setGeometry(40, 150, 720, 400)
        # 표의 헤드라벨 설정
        self.data_table.setHorizontalHeaderLabels(['업체명', '업체종류', '주소', '전화번호', '영업시작시간',
                                                   '영업종료시간'])
        # 표의 각 항의 너비 설정, 각각의 데이터와 라벨을 적정히 표시하는 크기로 설정하고 나머지는 주소에 몰아줌
        self.data_table.setColumnWidth(0, 100)
        self.data_table.setColumnWidth(1, 110)
        self.data_table.setColumnWidth(2, 198)
        self.data_table.setColumnWidth(3, 90)
        self.data_table.setColumnWidth(4, 80)
        self.data_table.setColumnWidth(5, 80)
        self.data_table.pressed.connect(self.new_data)
        # 표의 각 칸에 해당하는 데이터 입력
        for i in range(len(self.result_list) - 1):
            # 인덱스 값을 버티컬 헤더로 설정
            self.data_table.setVerticalHeaderItem(i, QTableWidgetItem(str(self.result_list[i + 1][20])))
            self.data_table.setItem(i, 0, QTableWidgetItem(self.result_list[i + 1][0]))
            self.data_table.setItem(i, 1, QTableWidgetItem(self.result_list[i + 1][1]))
            self.data_table.setItem(i, 2, QTableWidgetItem(self.result_list[i + 1][2]))
            # 전화번호, 표의 구성 상 영업시간 앞에 오는 것이 좋아보여 앞으로 뺌
            self.data_table.setItem(i, 3, QTableWidgetItem(self.result_list[i + 1][14]))
            self.data_table.setItem(i, 4, QTableWidgetItem(self.result_list[i + 1][12]))
            self.data_table.setItem(i, 5, QTableWidgetItem(self.result_list[i + 1][13]))

    # 데이터 검색 기능
    def search_data(self):
        # 데이터 검색의 프로세스
        self.search_process()
        # 테이블 값 수정 프로세스 2가지 기능을 하나로 엮음
        self.modify_table_data()

    # 테이블 수정 프로세스
    def modify_table_data(self):
        # search_data로 갱신한 result_list에 대응하게끔 표의 길이를 수정한 뒤
        self.data_table.setRowCount(len(self.result_list) - 1)
        # 새로 생성된 데이터를 재삽입함
        # self.data_table.setVerticalHeaderLabels
        for i in range(len(self.result_list)):
            # 인덱스 값을 버티컬 헤더로 설정
            self.data_table.setVerticalHeaderItem(i, QTableWidgetItem(str(self.result_list[i][20])))
            self.data_table.setItem(i, 0, QTableWidgetItem(self.result_list[i][0]))
            self.data_table.setItem(i, 1, QTableWidgetItem(self.result_list[i][1]))
            # 주소의 경우 도로명과 지번 두 가지가 있기 때문에
            self.data_table.setItem(i, 2, QTableWidgetItem(self.result_list[i][2]))
            # 도로명 주소가 공란일 경우
            if not self.result_list[i][2]:
                # 지번 주소를 입력함
                self.data_table.setItem(i, 2, QTableWidgetItem(self.result_list[i][3]))
            self.data_table.setItem(i, 3, QTableWidgetItem(self.result_list[i][14]))
            self.data_table.setItem(i, 4, QTableWidgetItem(self.result_list[i][12]))
            self.data_table.setItem(i, 5, QTableWidgetItem(self.result_list[i][13]))

    # 데이터 저장
    def save_data(self):
        # self.selected_row에 내용이 있는 경우 반복함
        reply = QMessageBox.question(self, '저장', '저장하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        # 예 누를 시 데이터 저장
        if reply == QMessageBox.Yes:
            while self.selected_row:
                # 데이터 리스트에 변경된 값 적용
                self.data_list[int(self.data_table.verticalHeaderItem(self.selected_row[0]).text())][0] = self.data_table.item(self.selected_row[0], 0).text()
                self.data_list[int(self.data_table.verticalHeaderItem(self.selected_row[0]).text())][1] = self.data_table.item(self.selected_row[0], 1).text()
                self.data_list[int(self.data_table.verticalHeaderItem(self.selected_row[0]).text())][2] = self.data_table.item(self.selected_row[0], 2).text()
                self.data_list[int(self.data_table.verticalHeaderItem(self.selected_row[0]).text())][14] = self.data_table.item(self.selected_row[0], 3).text()
                self.data_list[int(self.data_table.verticalHeaderItem(self.selected_row[0]).text())][12] = self.data_table.item(self.selected_row[0], 4).text()
                self.data_list[int(self.data_table.verticalHeaderItem(self.selected_row[0]).text())][13] = self.data_table.item(self.selected_row[0], 5).text()
                # 적용된 업체를 리스트에서 제거
                self.selected_row.remove(self.selected_row[0])

            # csv 파일에 적용
            f = open('carcenter_data.csv', 'w', newline='', encoding='UTF-8')
            write = csv.writer(f)
            for i in range(len(self.data_list)):
                write.writerow(self.data_list[i])

        # 아닐 시 패스
        else:
            pass

    # 선택한 행 저장용
    def new_data(self):
        # 작업량을 줄이기 위해 이전에 선택한 적 없는 행일 경우에만 추가함
        if self.data_table.currentRow() not in self.selected_row:
            self.selected_row.append(self.data_table.currentRow())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainProgram()
    sys.exit(app.exec_())
