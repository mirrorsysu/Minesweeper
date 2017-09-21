import random, sys, random
from PyQt5.QtWidgets import *
from functools import partial

class Minesweeper(QMainWindow):
    height = 10
    def __init__(self):
        super(Minesweeper, self).__init__()
        self.height = 30
        self.width = 50

        self.sumOfBlock = self.height * self.width
        self.numOfMine = 200
        self.setGeometry(50, 50, 30 * (self.width + 1), 30 * (self.height + 2))
        self.numOfFlag = 0
        self.supportFlag = 0

        self.minecnt = [[0 for i in range(self.width + 2)] for i in range(self.height + 2)]
        self.mine = [[0 for i in range(self.width + 2)] for i in range(self.height + 2)]
        self.opened = [[0 for i in range(self.width + 2)] for i in range(self.height + 2)]

        self.showMineText = QLabel(self)
        self.showMineText.setText(str(self.numOfMine - self.numOfFlag))
        self.showMineText.move(10, 10 + 30*self.height)
        self.showMineText.setText("剩余雷数：")
        self.showMineNum = QLabel(self)
        self.showMineNum.setText(str(self.numOfMine - self.numOfFlag))
        self.showMineNum.move(10 + 60, 10 + 30 * self.height)
        self.btnR = QPushButton(self)
        self.btnR.move(30 * (self.width / 2 - 1), 10 + 30 * self.height)
        self.btnR.clicked.connect(self.reset)
        self.btnR.setText('Reset')
        self.btnS = QPushButton(self)
        self.btnS.move(30 * (self.width / 2 - 5), 10 + 30 * self.height)
        self.btnS.clicked.connect(self.supportSwitch)
        self.btnS.setText('Support')
        self.btnA = QPushButton(self)
        self.btnA.move(30 * (self.width / 2 + 3), 10 + 30 * self.height)
        self.btnA.clicked.connect(self.autoScan)
        self.btnA.setText('Auto Scan')

    class xyBtn(QPushButton):
        def __init__(self, par, x, y, superclass):
            super(QPushButton, self).__init__(par);
            self.x = x
            self.y = y
            self.superclass = superclass
            self.setStyleSheet('QWidget {background-color:%s}' % "white")
        def getxy(self):
            return (self.x, self.y)

        def hasOpened(self):
            if self.superclass.opened[self.x + 1][self.y + 1] == 1:
                return 1
            else :
                return 0
        def mousePressEvent(self, e):
            if e.button() == 1:
                self.superclass.onClicked(self)
            elif e.button() == 2:
                self.superclass.onRightClicked(self)
        def mouseDoubleClickEvent(self, e):
            self.superclass.scanMine(self)
        def enterEvent(self, e):
            self.superclass.supportEnter(self)
        def leaveEvent(self, e):
            self.superclass.supportLeave(self)

    def autoScan(self):
        hasClicked = 0
        openedBtn = []
        for i in self.btn:
            if i.hasOpened():
                openedBtn.append(i)
        for btn in openedBtn:
            mineNum = self.minecnt[btn.x + 1][btn.y + 1]
            scanList = self.get8btn(btn)
            noOpen = len(scanList)
            for i in scanList:
                # i.setStyleSheet('QWidget {background-color:%s}' % "yellow")
                if i.text() == "★":
                    mineNum -= 1
                    noOpen -= 1
                elif self.opened[i.x + 1][i.y + 1] == 1:
                    noOpen -= 1
            for i in scanList:
                if i.hasOpened() == 0:
                    if mineNum == 0 and i.text() == "":
                        self.onClicked(i)
                        hasClicked = 1
                    elif noOpen == mineNum and i.text() == "":
                        self.setFlag(i)
                        hasClicked = 1
        # if len(openedBtn) == 0 or hasClicked == 0:
        #     neverVisit = []
        #     for i in  self.btn:
        #         if i.hasOpened() == 0:
        #             neverVisit.append(i)
        #     index = random.randint(0, len(neverVisit) - 1)
        #     self.onClicked(neverVisit[index])
    def setFlag(self, btn):
        btn.setText("★")
        self.numOfFlag += 1
        self.showMineNum.setText(str(self.numOfMine - self.numOfFlag))

    def reset(self):
        for i in range(0, self.height + 1):
            for j in range(0, self.width + 1):
                self.minecnt[i][j] = 0
                self.mine[i][j] = 0
                self.opened[i][j] = 0
        for i in self.btn:
            i.setStyleSheet('QWidget {background-color:%s}' % "white")
            i.setText("")
            i.setEnabled(True)
        self.setMine()
        self.numOfFlag = 0
        self.showMineNum.setText(str(self.numOfMine - self.numOfFlag))

    def setBtn(self):
        self.btn = []
        for i in range(0, self.sumOfBlock):
            self.btn.append(self.xyBtn(self, int(i/self.width), i%self.width, self))
            self.btn[i].resize(30, 30)
            self.btn[i].move(10 + 30*self.btn[i].y, 10 + 30*self.btn[i].x)

    def supportEnter(self, b):
        if self.opened[b.x + 1][b.y + 1] == 0 or self.supportFlag == 0:
            return
        mineNum = self.minecnt[b.x + 1][b.y + 1]
        scanList = self.get8btn(b)
        noOpen = len(scanList)
        for i in scanList:
            # i.setStyleSheet('QWidget {background-color:%s}' % "yellow")
            if i.text() == "★":
                mineNum -= 1
                noOpen -= 1
            elif self.opened[i.x + 1][i.y + 1] == 1:
                noOpen -= 1
        for i in scanList:
            if self.opened[i.x + 1][i.y + 1] == 0:
                if mineNum == 0 and i.text() == "":
                    i.setStyleSheet('QWidget {background-color:%s}' % "blue")
                elif noOpen == mineNum and i.text() == "":
                    i.setStyleSheet('QWidget {background-color:%s}' % "red")

    def supportLeave(self, b):
        if self.opened[b.x + 1][b.y + 1] == 0:
            return
        scanList = self.get8btn(b)
        for i in scanList:
            if self.opened[i.x + 1][i.y + 1] == 0:
                i.setStyleSheet('QWidget {background-color:%s}' % "white")
    def supportSwitch(self):
        self.supportFlag = not self.supportFlag

    def get8btn(self, b):
        index = b.x * self.width + b.y
        scanList = []
        if b.y > 0:
            scanList.append(self.btn[index - 1])
            if b.x > 0:
                scanList.append(self.btn[index - self.width])
                scanList.append(self.btn[index - self.width - 1])
            if b.x < self.height - 1:
                scanList.append(self.btn[index + self.width])
                scanList.append(self.btn[index + self.width - 1])
        if b.y < self.width - 1:
            scanList.append(self.btn[index + 1])
            if b.x > 0:
                if b.y == 0:
                    scanList.append(self.btn[index - self.width])
                scanList.append(self.btn[index - self.width + 1])
            if b.x < self.height - 1:
                if b.y == 0:
                    scanList.append(self.btn[index + self.width])
                scanList.append(self.btn[index + self.width + 1])
        return scanList

    def scanMine(self, b):
        if b.text() == "" or b.text() == "★" or b.text() == "?": return
        mineNum = int(b.text())
        scanList = []
        if mineNum >= 1 and mineNum <= 8:
            scanList = self.get8btn(b)
        for i in scanList:
            # i.setStyleSheet('QWidget {background-color:%s}' % "yellow")
            if i.text() == "★":
                mineNum -= 1
        if mineNum == 0:
            for i in scanList:
                self.onClicked(i)
    def onRightClicked(self, b):
        if b.text() == "":
            b.setText("★")
            self.numOfFlag += 1
        elif b.text() == "★":
            self.numOfFlag -= 1
            b.setText("?")
        elif b.text() == "?":
            b.setText("")
        self.showMineNum.setText(str(self.numOfMine - self.numOfFlag))

    def onClicked(self, b):
        if self.opened[b.x + 1][b.y + 1] == 1: return
        self.opened[b.x + 1][b.y + 1] = 1;
        if b.text() != "" : return

        b.setText(str(self.minecnt[b.x + 1][b.y + 1]))
        b.setStyleSheet("")

        if self.minecnt[b.x + 1][b.y + 1] == -1:
            b.setText("×")
            QMessageBox.information(self, "你输了", "踩到地雷了")
            self.reset()
            return
        elif self.minecnt[b.x + 1][b.y + 1] == 0:
            b.setText("")
            scanList = self.get8btn(b)
            for i in scanList:
                self.onClicked(i)
        return

    def setMine(self):
        for i in range(self.numOfMine):
            while 1:
                x = random.randint(1, self.height)
                y = random.randint(1, self.width)
                if self.mine[x][y] == 0:
                    self.mine[x][y] = 1
                    break

        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                self.minecnt[i][j] = self.showGetSum(i, j)
                if self.mine[i][j] == 1:
                    self.minecnt[i][j] = -1


    def showGetSum(self, x, y):
        sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                sum += self.mine[x + i][y + j]
        return sum

    def p(self):
        for i in self.mine:
            print(i)
        print ('------------------------------')
        for i in self.minecnt:
            print(i)

app = QApplication(sys.argv);
f = Minesweeper()
f.setMine()
f.setBtn()
f.show()
sys.exit(app.exec_())

