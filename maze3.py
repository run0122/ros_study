from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import sys

class MainWindow(QWidget):
         
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QVBoxLayout(self)

        for i in range(0, 9):
            exec(f"self.line{i} = QLabel(self)") 
            exec(f'self.line{i}.setAlignment(Qt.AlignCenter)')
            exec(f'layout.addWidget(self.line{i})')
        
        self.lineLocation = QLabel(self)
        self.lineError = QLabel(self)

        layout.addWidget(self.lineLocation)
        layout.addWidget(self.lineError)

        self.resize(200, 200)
        self.drawMap()
    
    # 맵 및 현재 위치 출력 함수
    def drawMap(self):
        for row in range(9):
            Text = ""
            for col in range(9):
                Text += str(gameMap[row][col]) + " "
            exec(f'self.line{row}.setText(Text)')
        self.lineLocation.setText(f'현재 위치 : ({currentRow},{currentCol})')  

    def keyPressEvent(self, e): #키가 눌러졌을 때 실행됨
        if e.key() == 16777235:     # 위쪽 방향키
            print("Up")
            self.check(-1, 0)
        elif e.key() == 16777237:   # 위쪽 방향키
            print("Down")
            self.check(1, 0)
        elif e.key() == 16777234:   # 왼쪽 방향키
            print("Left")
            self.check(0, -1)
        elif e.key() == 16777236:   # 오른쪽 방향키
            print("Right")
            self.check(0, 1)
        else:
            print("방향키를 입력하세요.")

    def keyReleaseEvent(self, e): #키를 누른상태에서 뗏을 때 실행됨
        pass
    
    # 에러 검사 및 맵 출력
    def errorCheck(self):
        global error
        self.drawMap()
        if gameFinished == True:
            self.lineError.setText("게임 종료 됐습니다")
            return
        elif error == False:
            self.lineError.setText("Good")
        elif error == True:
            self.lineError.setText("Not Good")
            error = False
    
    # 상하좌우 판단
    def check(self, changeRow, changeCol):
        global currentRow, currentCol, gameFinished, error
        # 맵 밖으로 나가려 할 때
        if currentRow + changeRow < 0 or currentRow + changeRow > 8 or currentCol + changeCol < 0 or currentCol + changeCol > 8 :
            error = True
        # 길이 있을 때
        elif gameMap[currentRow+changeRow][currentCol+changeCol] == 'o':
            gameMap[currentRow+changeRow][currentCol+changeCol] = 'P'
            gameMap[currentRow][currentCol] = 'o'
            currentRow += changeRow
            currentCol += changeCol
        # 종료될 때
        elif gameMap[currentRow+changeRow][currentCol+changeCol] == 'F':
            gameMap[currentRow+changeRow][currentCol+changeCol] = 'F'
            gameMap[currentRow][currentCol] = 'o'
            gameFinished = True
        # X에 부딛혔을 때
        else:
            error = True
        self.errorCheck()
    
gameMap = []

gameFinished = False
error = False

currentRow, currentCol = 8,0

if __name__ == "__main__":

    f = open('./level1.map')
    for i in range(9):
        line = f.readline()
        splitedLine = line.split()
        gameMap.append(splitedLine)

    f.close()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()