import operator
import sys
import tkinter
import random
from tkinter import messagebox
import shici

LEVEL = 8
RECT_ROWS = 8
RECT_COLS = 8
SIZE = 50
LEFT = 400
RIGHT = 150

w_width = RECT_ROWS * SIZE
w_height = RECT_COLS * SIZE
spc = 10

def _leftbutton(ntag: str, canvas: tkinter.Canvas):
    global bw
    # print(ntag)
    # for i in bw: print(i)
    for i, j in (get_around(int(ntag[-2]), int(ntag[-1]))):
        bw[i][j] = not bw[i][j]
        canvas.itemconfig("Rec" + str(i) + str(j), fill=("white" if bw[i][j] else "black"))

    if operator.eq(bw, question):
        if messagebox.askyesno("提示", tips[random.randint(0, len(tips) - 1)]+"\r恭喜你，成功了。是否继续挑战？"):
            _question()
        else:
            sys.exit()

def get_around(x, y):  # 点击块上下左右的方块的列表位置
    return [(i, j) for i in range(max(0, x - 1), min(RECT_ROWS - 1, x + 1) + 1)
            for j in range(max(0, y - 1), min(RECT_COLS - 1, y + 1) + 1) if i == x or j == y]

def _levelget(e):
    global LEVEL
    LEVEL = levelScale.get()

def _question():
    global canvas1, LEVEL, posTuple, bw, question
    bw = [[True] * RECT_COLS for i in range(RECT_ROWS)]
    _rightupdata()
    question = [[True] * RECT_COLS for i in range(RECT_ROWS)]
    leftdis.itemconfig('Lec', fill="white")
    count = 0
    posTuple = set()
    if levelScale.get() == 100:
        if messagebox.askokcancel("提示", "解这个谜题很考验你的耐心，继续请确认，不继续请取消。"):
            LEVEL = 500
        else:
            levelScale.set(8)
    else:
        LEVEL = levelScale.get()

    while count < LEVEL:
        posTuple.add((random.randint(0, RECT_ROWS - 1), random.randint(0, RECT_COLS - 1)))
        if LEVEL <= 8:
            count = len(posTuple)
        else:
            count += 1
    for pos in posTuple:
        for i, j in get_around(pos[0], pos[1]):
            # print(i, j)
            question[i][j] = not question[i][j]
            leftdis.itemconfig("Lec" + str(i) + str(j), fill=("white" if question[i][j] else "black"))

def _emptyright():
    global bw
    bw = [[True] * RECT_COLS for i in range(RECT_ROWS)]
    _rightupdata()


def _rightupdata():
    global bw
    for i in range(len(bw)):
        for j in range(len(bw[i])):
            rightdis.itemconfig("Rec" + str(i) + str(j), fill=("white" if bw[i][j] else "black"))


def _answer():
    if levelScale.get() == 100:
        messagebox.showinfo("不抛弃，不放弃", tips[random.randint(0, len(tips) - 1)])
    else:
        print(f"点击的{len(posTuple)}个块如下：")
        poslist = list(posTuple)
        poslist.sort()
        count = 0
        for i in poslist:
            print(i, end='')
            count += 1
            if not count % 10:
                print()
        print()
        messagebox.showinfo("答案", posTuple)

tip = shici.b.decode()
tips = tip.split()

# 创建窗体
root = tkinter.Tk()
root.title('黑白方块')
root.geometry(f'{w_width * 2 + spc}x{w_height + 80}+{LEFT}+{RIGHT}')
root.resizable(False, False)

# 创建两个画布，左边的为题目画布，右边为解题画布
leftdis = tkinter.Canvas(root, width=w_width, height=w_height)
rightdis = tkinter.Canvas(root, width=w_width, height=w_height)
# 按Grid放置控件
leftdis.grid(row=0, column=0, columnspan=2)
rightdis.grid(row=0, column=2, columnspan=2)

# 创建出题命令按钮
questionButton = tkinter.Button(root, width=20, text='重新出题', command=_question)
questionButton.grid(row=1, column=1)

# 创建解题复位按钮
emptyButton = tkinter.Button(root, width=20, text="清除重来", command=_emptyright)
emptyButton.grid(row=1, column=3)

# 创建查看答案按钮
answerButton = tkinter.Button(root, width=20, text="偷看小抄", command=_answer)
answerButton.grid(row=1, column=2)

# 创建难度调节
levelScale = tkinter.Scale(root, orient=tkinter.HORIZONTAL, length=200,
                           from_=1, to=100, resolution=1, command=_levelget)
levelScale.set(LEVEL)
levelScale.grid(row=1, column=0)

# 生成解题数组，默认True为白色
bw = [[True] * RECT_COLS for i in range(RECT_ROWS)]
question = []
for i in range(RECT_ROWS):
    leftdis.create_line((i * SIZE, 0), (i * SIZE, w_height))
    leftdis.create_line((0, i * SIZE), (w_height, i * SIZE))
    rightdis.create_line((i * SIZE, 0), (i * SIZE, w_height))
    rightdis.create_line((0, i * SIZE), (w_height, i * SIZE))

    for j in range(RECT_COLS):
        leftdis.create_rectangle((i * SIZE, j * SIZE), (i * SIZE + SIZE, j * SIZE + SIZE),
                                 fill="white", tags=('Lec' + str(j) + str(i), "Lec"))
        rightdis.create_rectangle((i * SIZE, j * SIZE), (i * SIZE + SIZE, j * SIZE + SIZE),
                                  fill="white", activefill='red', tags=('Rec' + str(j) + str(i), "Rec"))


        def r_leftclick(event, ntag='Rec' + str(j) + str(i)):
            _leftbutton(ntag, rightdis)


        rightdis.tag_bind('Rec' + str(j) + str(i), '<Button-1>', r_leftclick)

leftdis.create_line((0, 2), (w_width, 2), width=2)
leftdis.create_line((3, 0), (3, w_height), width=2)
leftdis.create_line((w_width - 1, 2), (w_width - 1, w_height), width=2)
leftdis.create_line((3, w_height), (w_width - 1, w_height), width=2)

rightdis.create_line((0, 2), (w_width, 2), width=2)
rightdis.create_line((3, 0), (3, w_height), width=2)
rightdis.create_line((w_width - 1, 2), (w_width - 1, w_height), width=2)
rightdis.create_line((3, w_height), (w_width - 1, w_height), width=2)

canvas1 = leftdis
# questionButton.bind("<Button-1>", test)
_question()

if __name__ == '__main__':
    root.mainloop()
