import pygame
import threading
import sys
import math
import time
import sys
import os
from pathlib import Path

PI = 3.1415926535

def LoadConf(ConfName):
    file = open(ConfName, 'r')
    N = 9
    colors = []
    for i in range(N):
        inp = file.readline().split()
        colors.append([int(x) for x in (inp[-3:-1] + [inp[-1]])])
    return colors

CamPos = [0, 0, 0]
CamRot = [0, PI / 2, -PI / 2]
SDist = 400
INF = 10 ** 9
SPD = 3000
Mult = 500
RSPD = 1
DetStep = 5
DetStep = math.radians(DetStep)
MouseSensDiv = 100
ScalingSPD = 10
G0Color, G1Color, G2Color, G3Color, FrameColor, SelectionColor, SelectionTextColor, BGColor, StepSelectionColor = LoadConf('GKIT.conf')
#PPos = [0, 0, 0]

def ToCoordSpace(vect, space):
    vct = list(vect)
    for i in range(len(vect)):
        vct[i] = vct[i] + space[i]
    return vct

def MultVect(vect, n):
    Answer = []
    for i in range(len(vect)):
        Answer.append(vect[i] * n)
    return Answer

def Dist(v1, v2):
    return ((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2) ** 0.5

def Dist3(v1, v2):
    return ((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2 + (v1[2] - v2[2]) ** 2) ** 0.5

def ToNormal(angle):
    return angle % math.radians(360)

def DeltaAngleRadCW(A1, A2):
    A1 = ToNormal(A1)
    A2 = ToNormal(A2)
    if A1 != A2:
        if A1 > A2:
            return A1 - A2
        else:
            return A1 + math.radians(360) - A2
    else:
        return math.radians(360)

def DeltaAngleRadCCW(A2, A1):
    A1 = ToNormal(A1)
    A2 = ToNormal(A2)
    if A1 != A2:
        if A1 > A2:
            return A1 - A2
        else:
            return A1 + math.radians(360) - A2
    else:
        return math.radians(360)

def ToSeconds(minutes):
    return str(int(minutes)) + ' minutes ' + str(int((minutes - int(minutes)) * 6000) / 100) + ' seconds'

def read(FileNames):
    lines = []
    colors = []
    thimbs = []
    periods = []
    BCounts = []
    GoOnTimes = []
    ProcessTimes = []
    Coms = []
    LGoOnTimes = []
    LProcessTimes = []
    BlockCount = 0
    GlobalText = []
    time = 0
    GLine = -1
    if hasattr(sys, '_MEIPASS'):
        #print('Record')
        font = os.path.join('arial.otf')
        font = pygame.font.Font(font, 12)
        IsEXE = True
    else:
        font = pygame.font.Font(None, 24)
    scr = pygame.display.set_mode([450, 150])
    GlobalLength = 0
    for FileName in FileNames:
        try:
            fl = open(FileName, 'r')
            GlobalLength += len(fl.read().split('\n'))
        except:
            print("No file", FileName)
            input('Press [Enter] to exit.')
            exit()
    for period, FileName in enumerate(FileNames):
        curr_path = Path('.')
        print(f"Current path: {curr_path.absolute()}")
        print(f"Filename: {FileName}")
        try:
            file = open(FileName, 'r')
        except:
            print("No file", FileName)
            input('Press [Enter] to exit.')
            exit()
        x, y, z = (0, 0, 20)
        tx, ty, tz = (0, 0, 20)
        inp = file.readline()
        GLine += 1
        line = 0
        LenMemor = len(lines)
        CSpace = [0, 0, 0]
        while not (inp == 'M30' or inp == 'M30\n'):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            percent = max(GLine / GlobalLength, 0)
            scr.fill((0, 0, 255))
            pygame.draw.rect(scr, (255, 255, 255), [10, 50, 430, 50])
            pygame.draw.rect(scr, (50, 50, 50), [12, 52, 426, 46])
            pygame.draw.rect(scr, (0, 255, 0), [14, 54, 422 * percent, 42])
            scr.blit(font.render(str(int(percent * 100)) + '%', 0, (255, 255, 255)), [10, 12])
            scr.blit(font.render('Loading file ' + FileName, 0, (255, 255, 255)), [10, 112])
            scr.blit(font.render(inp[:-1], 0, (255, 255, 255)), [10, 130])
            pygame.display.update()
            GlobalText.append(inp)
            #print(line)
            tx, ty, tz = x, y, z
            line += 1
            GLine += 1
            Comands = inp.split()
            if len(Comands) != 0:
                if Comands[0] == 'G0' or Comands[0] == 'G00':
                    SecondStr = ''
                    Key = ''
                    for simbol in list(Comands[1]):
                        if simbol == 'X':
                            if Key != '':
                                if Key == 'X':
                                    print('ERROR! Line -', line, '\n    X coordinate was set twice...')
                                    tx = float(SecondStr)
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'X'
                        elif simbol == 'Y':
                            if Key != '':
                                if Key == 'Y':
                                    print('ERROR! Line -', line, '\n    Y coordinate was set twice...')
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'Y'
                        elif simbol == 'Z':
                            if Key != '':
                                if Key == 'Z':
                                    print('ERROR! Line -', line, '\n    Z coordinate was set twice...')
                                    tz = float(SecondStr)
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                SecondStr = ''
                            Key = 'Z'
                        else:
                            SecondStr = SecondStr + simbol
                    if Key == 'X':
                        tx = float(SecondStr)
                    if Key == 'Y':
                        ty = float(SecondStr)
                    if Key == 'Z':
                        tz = float(SecondStr)
                    FSpeed = 4100
                    lines.append([[x * Mult, y * Mult, z * Mult], ToCoordSpace([tx * Mult, ty * Mult, tz * Mult], CSpace)])
                    colors.append(G0Color)
                    thimbs.append(1)
                    periods.append(period)
                    BCounts.append(BlockCount)
                    Coms.append(GLine)
                    GoOnTimes.append(time)
                    LGoOnTimes.append(time)
                    time += Dist3([x, y, z], [tx, ty, tz]) / FSpeed
                    ProcessTimes.append(Dist3([x, y, z], [tx, ty, tz]) / FSpeed)
                    LProcessTimes.append(Dist3([x, y, z], [tx, ty, tz]) / FSpeed)
                    BlockCount += 1
                elif Comands[0] == 'G1' or Comands[0] == 'G01':
                    SecondStr = ''
                    Key = ''
                    for simbol in list(Comands[1]):
                        if simbol == 'X':
                            if Key != '':
                                if Key == 'X':
                                    print('ERROR! Line -', line, '\n    X coordinate was set twice...')
                                    tx = float(SecondStr)
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'X'
                        elif simbol == 'Y':
                            if Key != '':
                                if Key == 'Y':
                                    print('ERROR! Line -', line, '\n    Y coordinate was set twice...')
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'Y'
                        elif simbol == 'Z':
                            if Key != '':
                                if Key == 'Z':
                                    print('ERROR! Line -', line, '\n    Z coordinate was set twice...')
                                    tz = float(SecondStr)
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                SecondStr = ''
                            Key = 'Z'
                        elif simbol == 'F':
                            if Key == 'X':
                                tx = float(SecondStr)
                            if Key == 'Y':
                                ty = float(SecondStr)
                            if Key == 'Z':
                                tz = float(SecondStr)
                            SecondStr = ''
                        else:
                            SecondStr = SecondStr + simbol
                    FSpeed = float(SecondStr)
                    SecondStr = ''
                    lines.append([[x * Mult, y * Mult, z * Mult], ToCoordSpace([tx * Mult, ty * Mult, tz * Mult], CSpace)])
                    colors.append(G1Color)
                    thimbs.append(2)
                    periods.append(period)
                    BCounts.append(BlockCount)
                    Coms.append(GLine)
                    GoOnTimes.append(time)
                    LGoOnTimes.append(time)
                    time += Dist3([x, y, z], [tx, ty, tz]) / FSpeed
                    ProcessTimes.append(Dist3([x, y, z], [tx, ty, tz]) / FSpeed)
                    LProcessTimes.append(Dist3([x, y, z], [tx, ty, tz]) / FSpeed)
                    BlockCount += 1
                elif Comands[0] == 'G2' or Comands[0] == 'G02':
                    SecondStr = ''
                    Key = ''
                    Cx = x
                    Cy = y
                    RadMet = False
                    for index, simbol in enumerate(list(Comands[1])):
                        if simbol == 'X':
                            if Key != '':
                                if Key == 'X':
                                    print('ERROR! Line -', line, '\n    X coordinate was set twice...')
                                    tx = float(SecondStr)
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'X'
                        elif simbol == 'Y':
                            if Key != '':
                                if Key == 'Y':
                                    print('ERROR! Line -', line, '\n    Y coordinate was set twice...')
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'Y'
                        elif simbol == 'Z':
                            if Key != '':
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Z':
                                    print('ERROR! Line -', line, '\n    Z coordinate was set twice...')
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'Z'
                        elif simbol == 'I':
                            if Key != '':
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'I'
                        elif simbol == 'J':
                            Cx = x + float(SecondStr)
                            SecondStr = ''
                        elif simbol == 'R':
                            if Key != '':
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                            RadMet = True
                            SecondStr = ''
                        elif simbol == 'F':
                            FSpeed = float(Comands[1][index + 1:])
                            break
                        else:
                            SecondStr = SecondStr + simbol
                    tx, ty, tz = ToCoordSpace([tx, ty, tz], CSpace)
                    if not RadMet:
                        Cy = y + float(SecondStr)
                        SecondStr = ''
                    else:
                        Radius = float(SecondStr)
                        StVector = [tx - x, ty - y]
                        CP = [x + StVector[0] / 2, y + StVector[1] / 2]
                        PerpVector = [-StVector[1], StVector[0]]
                        Cxt, Cyt = MultVect(PerpVector, ((Radius ** 2 - (Dist((0, 0), StVector) / 2) ** 2) ** 0.5) / Dist((0, 0), PerpVector))
                        Cxt += CP[0]
                        Cyt += CP[1]
                        Cx = Cxt
                        Cy = Cyt
                        Angle1 = ToAngle(*(x - Cx, y - Cy))
                        Angle2 = ToAngle(*(tx - Cx, ty - Cy))
                        Step = (DeltaAngleRadCW(Angle1, Angle2))
                        #print(math.degrees(Step))
                        if (Step > math.radians(180) and Radius > 0) or (Step < math.radians(180) and Radius < 0):
                            Cxt, Cyt = MultVect(MultVect(PerpVector, -1), ((Radius ** 2 - (Dist((0, 0), StVector) / 2) ** 2) ** 0.5) / Dist((0, 0), PerpVector))
                            Cxt += CP[0]
                            Cyt += CP[1]
                        Cx = Cxt
                        Cy = Cyt
                        SecondStr = ''
                        R1 = abs(Radius)
                        R2 = abs(Radius)
                        StepR = 0
                        #print(Radius)
                    Angle1 = ToAngle(*(x - Cx, y - Cy))
                    Angle2 = ToAngle(*(tx - Cx, ty - Cy))
                    DetDep = int(DeltaAngleRadCW(Angle1, Angle2) / DetStep)
                    Step = (DeltaAngleRadCW(Angle1, Angle2)) / DetDep
                    #print(math.degrees(Step * DetDep))
                    R1 = Dist((x, y), (Cx, Cy))
                    R2 = Dist((tx, ty), (Cx, Cy))
                    StepR = (R2 - R1) / DetDep
                    Pos = [x, y, z]
                    DeltaTimeSum = 0
                    ZStep = (tz - z) / DetDep
                    for i in range(DetDep):
                        Angle = -Step * i + Angle1
                        Radius = StepR * i + R1
                        NextPos = [math.cos(Angle) * Radius + Cx, math.sin(Angle) * Radius + Cy, z + ZStep * i]
                        lines.append([MultVect(Pos, Mult), MultVect(NextPos, Mult)])
                        colors.append(G2Color)
                        thimbs.append(2)
                        periods.append(period)
                        BCounts.append(BlockCount)
                        Coms.append(GLine)
                        GoOnTimes.append(time)
                        LGoOnTimes.append(time)
                        time += Dist3(Pos, NextPos) / FSpeed
                        LProcessTimes.append(Dist3(Pos, NextPos) / FSpeed)
                        DeltaTimeSum += Dist3(Pos, NextPos) / FSpeed
                        Pos = NextPos
                    lines.append([MultVect(Pos, Mult), MultVect([tx, ty, tz], Mult)])
                    colors.append(G2Color)
                    thimbs.append(2)
                    periods.append(period)
                    BCounts.append(BlockCount)
                    Coms.append(GLine)
                    GoOnTimes.append(time)
                    LGoOnTimes.append(time)
                    time += Dist3(Pos, [tx, ty, tz]) / FSpeed
                    DeltaTimeSum += Dist3(Pos, [tx, ty, tz]) / FSpeed
                    LProcessTimes.append(Dist3(Pos, [tx, ty, tz]) / FSpeed)
                    for i in range(DetDep + 1):
                        ProcessTimes.append(DeltaTimeSum)
                    BlockCount += 1
    ##                lines.append([MultVect([x, y, z], Mult), MultVect([tx, ty, tz], Mult)])
    ##                colors.append((255, 255, 0))
    ##                thimbs.append(10)
    ##                lines.append([MultVect([x, y, z], Mult), MultVect([Cx, Cy, tz], Mult)])
    ##                colors.append((0, 255, 255))
    ##                thimbs.append(10)
                elif Comands[0] == 'G3' or Comands[0] == 'G03':
                    SecondStr = ''
                    Key = ''
                    Cx = x
                    Cy = y
                    RadMet = False
                    for index, simbol in enumerate(list(Comands[1])):
                        if simbol == 'X':
                            if Key != '':
                                if Key == 'X':
                                    print('ERROR! Line -', line, '\n    X coordinate was set twice...')
                                    tx = float(SecondStr)
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'X'
                        elif simbol == 'Y':
                            if Key != '':
                                if Key == 'Y':
                                    print('ERROR! Line -', line, '\n    Y coordinate was set twice...')
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'Y'
                        elif simbol == 'Z':
                            if Key != '':
                                if Key == 'Z':
                                    print('ERROR! Line -', line, '\n    Z coordinate was set twice...')
                                    tz = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                SecondStr = ''
                            Key = 'Z'
                        elif simbol == 'I':
                            if Key != '':
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'I'
                        elif simbol == 'J':
                            Cx = x + float(SecondStr)
                            SecondStr = ''
                        elif simbol == 'R':
                            if Key != '':
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                            RadMet = True
                            SecondStr = ''
                        elif simbol == 'F':
                            FSpeed = float(Comands[1][index + 1:])
                            break
                        else:
                            SecondStr = SecondStr + simbol
                    tx, ty, tz = ToCoordSpace([tx, ty, tz], CSpace)
                    if not RadMet:
                        Cy = y + float(SecondStr)
                        SecondStr = ''
                    else:
                        Radius = float(SecondStr)
                        StVector = [tx - x, ty - y]
                        CP = [x + StVector[0] / 2, y + StVector[1] / 2]
                        PerpVector = [-StVector[1], StVector[0]]
                        Cxt, Cyt = MultVect(PerpVector, ((Radius ** 2 - (Dist((0, 0), StVector) / 2) ** 2) ** 0.5) / Dist((0, 0), PerpVector))
                        Cxt += CP[0]
                        Cyt += CP[1]
                        Cx = Cxt
                        Cy = Cyt
                        Angle1 = ToAngle(*(x - Cx, y - Cy))
                        Angle2 = ToAngle(*(tx - Cx, ty - Cy))
                        Step = (DeltaAngleRadCCW(Angle1, Angle2))
                        if (Step > math.radians(180) and Radius > 0) or (Step < math.radians(180) and Radius < 0):
                            Cxt, Cyt = MultVect(MultVect(PerpVector, -1), ((Radius ** 2 - (Dist((0, 0), StVector) / 2) ** 2) ** 0.5) / Dist((0, 0), PerpVector))
                            Cxt += CP[0]
                            Cyt += CP[1]
                        Cx = Cxt
                        Cy = Cyt
                        SecondStr = ''
                        R1 = abs(Radius)
                        R2 = abs(Radius)
                        StepR = 0
                        #print(Radius)
                    Angle1 = ToAngle(*(x - Cx, y - Cy))
                    Angle2 = ToAngle(*(tx - Cx, ty - Cy))
                    DetDep = int(DeltaAngleRadCCW(Angle1, Angle2) / DetStep)
                    Step = (DeltaAngleRadCCW(Angle1, Angle2)) / DetDep
                    R1 = Dist((x, y), (Cx, Cy))
                    R2 = Dist((tx, ty), (Cx, Cy))
                    StepR = (R2 - R1) / DetDep
                    Pos = [x, y, z]
                    DeltaTimeSum = 0
                    ZStep = (tz - z) / DetDep
                    #print(tz)
                    for i in range(DetDep):
                        Angle = Step * i + Angle1
                        Radius = StepR * i + R1
                        NextPos = [math.cos(Angle) * Radius + Cx, math.sin(Angle) * Radius + Cy, z + ZStep * i]
                        lines.append([MultVect(Pos, Mult), MultVect(NextPos, Mult)])
                        colors.append(G3Color)
                        thimbs.append(2)
                        periods.append(period)
                        BCounts.append(BlockCount)
                        Coms.append(GLine)
                        GoOnTimes.append(time)
                        LGoOnTimes.append(time)
                        time += Dist3(Pos, NextPos) / FSpeed
                        LProcessTimes.append(Dist3(Pos, NextPos) / FSpeed)
                        DeltaTimeSum += Dist3(Pos, NextPos) / FSpeed
                        Pos = NextPos
                    lines.append([MultVect(Pos, Mult), MultVect([tx, ty, tz], Mult)])
                    colors.append(G3Color)
                    thimbs.append(2)
                    periods.append(period)
                    BCounts.append(BlockCount)
                    Coms.append(GLine)
                    GoOnTimes.append(time)
                    LGoOnTimes.append(time)
                    time += Dist3(Pos, [tx, ty, tz]) / FSpeed
                    DeltaTimeSum += Dist3(Pos, [tx, ty, tz]) / FSpeed
                    LProcessTimes.append(Dist3(Pos, [tx, ty, tz]) / FSpeed)
                    for i in range(DetDep + 1):
                        ProcessTimes.append(DeltaTimeSum)
                    BlockCount += 1
    ##                lines.append([MultVect([x, y, z], Mult), MultVect([tx, ty, tz], Mult)])
    ##                colors.append((255, 255, 0))
    ##                thimbs.append(10)
    ##                lines.append([MultVect([x, y, z], Mult), MultVect([Cx, Cy, tz], Mult)])
    ##                colors.append((0, 255, 255))
    ##                thimbs.append(10)
                if Comands[0] == 'G10':
                    SecondStr = ''
                    Key = ''
                    for simbol in list(Comands[1]):
                        if simbol == 'X':
                            if Key != '':
                                if Key == 'X':
                                    print('ERROR! Line -', line, '\n    X coordinate was set twice...')
                                    tx = float(SecondStr)
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'X'
                        elif simbol == 'Y':
                            if Key != '':
                                if Key == 'Y':
                                    print('ERROR! Line -', line, '\n    Y coordinate was set twice...')
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                if Key == 'Z':
                                    tz = float(SecondStr)
                                SecondStr = ''
                            Key = 'Y'
                        elif simbol == 'Z':
                            if Key != '':
                                if Key == 'Z':
                                    print('ERROR! Line -', line, '\n    Z coordinate was set twice...')
                                    tz = float(SecondStr)
                                if Key == 'Y':
                                    ty = float(SecondStr)
                                if Key == 'X':
                                    tx = float(SecondStr)
                                SecondStr = ''
                            Key = 'Z'
                        else:
                            SecondStr = SecondStr + simbol
                    if Key == 'X':
                        tx = float(SecondStr)
                    if Key == 'Y':
                        ty = float(SecondStr)
                    if Key == 'Z':
                        tz = float(SecondStr)
                    CSpace = [tx, ty, tx]
            x, y, z = ToCoordSpace([tx, ty, tz], CSpace)
            inp = file.readline()
        GlobalText.append(inp)
    pygame.display.quit()
    return (lines, colors, thimbs, periods, BCounts, Coms, GlobalText, GoOnTimes, ProcessTimes, LGoOnTimes, LProcessTimes, BlockCount, time)

def Summ(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]

def ToAngle(x, y):
    return math.atan2(y, x)

def Rotate(x, y, deg):
    ln = Dist([0, 0], [x, y])
    A = ToAngle(x, y)
    X = math.sin(A + deg) * ln
    Y = math.cos(A + deg) * ln
    return [X, Y]

def ToLocal(CPos, CRot, lns):
    lines = list(lns)
    Answer = []
    for line in lines:
        default = [Summ(CPos, line[0]), Summ(CPos, line[1])]
        for point in default:
            #point[1], point[2] = Rotate(point[1], point[2], CRot[0])
            point[0], point[1] = Rotate(point[0], point[1], CRot[2])
            point[2], point[0] = Rotate(point[2], point[0], CRot[1])
        Answer.append(default)
    return Answer

def ScreenCoords(lines, ScrDist):
    global INF
    Answer = []
    for i, line in enumerate(lines):
        if not(line[0][0] < ScrDist and line[1][0] < ScrDist):
            if line[0][0] > ScrDist and line[1][0] > ScrDist:
                if line[0][0] != 0:
                    KY1 = line[0][1] / line[0][0]
                    KZ1 = line[0][2] / line[0][0]
                else:
                    KY1 = line[0][1] / 0.01
                    KZ1 = line[0][2] / 0.01
                if line[1][0] != 0:
                    KY2 = line[1][1] / line[1][0]
                    KZ2 = line[1][2] / line[1][0]
                else:
                    KY2 = line[1][1] / 0.01
                    KZ2 = line[1][2] / 0.01
                Answer.append([[KY1 * ScrDist, KZ1 * ScrDist], [KY2 * ScrDist, KZ2 * ScrDist]])
            else:
                #print('Apcho!')
                if line[0][0] < ScrDist:
                    Point = line[1]
                else:
                    Point = line[0]
                if Point[0] != 0:
                    KY1 = Point[1] / Point[0]
                    KZ1 = Point[2] / Point[0]
                else:
                    KY1 = Point[1] / 0.01
                    KZ1 = Point[2] / 0.01
                kY = (line[0][1] - line[1][1]) / (line[0][0] - line[1][0] if line[0][0] - line[1][0] != 0 else 0.01)
                bY = line[1][1] - line[1][0] * kY
                YY = kY * ScrDist + bY
                kZ = (line[0][2] - line[1][2]) / (line[0][0] - line[1][0] if line[0][0] - line[1][0] != 0 else 0.01)
                bZ = line[1][2] - line[1][0] * kZ
                ZZ = kZ * ScrDist + bZ
                Answer.append([[KY1 * ScrDist, KZ1 * ScrDist], [YY, ZZ]])
        else:
            Answer.append([[-INF, -INF], [-INF, -INF]])
    return Answer

def Centrix(coord, SCRX, SCRY):
    return [-coord[0] + SCRX / 2, -coord[1] + SCRY / 2]

def RotateSpeed(spd, rot):
    Answer = list(spd)
    Answer[1] = -spd[0] * math.cos(rot) + spd[1] * math.sin(rot)
    Answer[0] = -spd[1] * math.cos(rot) + -spd[0] * math.sin(rot)
    return Answer

def GetPhresePosition(time, lines, STimes, PTimes):
    Index = 0
    for i in range(len(STimes)):
        if STimes[i] <= time < STimes[i] + PTimes[i]:
            Index = i
    Shift = MultVect([lines[Index][1][0] - lines[Index][0][0], lines[Index][1][1] - lines[Index][0][1], lines[Index][1][2] - lines[Index][0][2]], (time - STimes[Index]) / PTimes[Index])
##    if (time - STimes[Index]) / PTimes[i] > 1:
##        print((time - STimes[Index]) / PTimes[i])
    Pos = [lines[Index][0][0] + Shift[0], lines[Index][0][1] + Shift[1], lines[Index][0][2] + Shift[2]]
    return Pos

def PhreseMesh(pos):
    x, y, z = pos
    return [[[x, y, z], [x + 300, y + 300, z + 2000]], [[x, y, z], [x + 300, y - 300, z + 2000]], [[x, y, z], [x - 300, y - 300, z + 2000]], [[x, y, z], [x - 300, y + 300, z + 2000]], [[x + 300, y + 300, z + 2000], [x + 300, y - 300, z + 2000]], [[x + 300, y - 300, z + 2000], [x - 300, y - 300, z + 2000]], [[x - 300, y - 300, z + 2000], [x - 300, y + 300, z + 2000]], [[x - 300, y + 300, z + 2000], [x + 300, y + 300, z + 2000]]]

pygame.init()
KeepGoing = True
print('\n' * 3 + '-' * 70)
print('G-code KIT, G-code viewer by Kudryashov Ilya')
print('Default settings:')
print('Movement speed -', SPD)
print('Keyboard rotation speed -', RSPD)
print('Mouse sensitive -', 1 / MouseSensDiv)
print('Curve detalisation step angle -', DetStep)
print('\n' * 5)
print('Enter names of files to open with format (.gcode, .txt and other) splited by [Space]')
lines, colors, thimbs, periods, BCs, Coms, ProgText, GoOnTimes, PTimes, LGoOnTimes, LPTimes, N, Time = read(input().split())
pygame.init()
MaxLen = 0
for string in ProgText:
    if len(string) > MaxLen:
        MaxLen = len(string)
#print(LGoOnTimes)
#print(LPTimes)
SCRX = 1000
SCRY = 700
try:
    screen = pygame.display.set_mode([SCRX, SCRY])
except:
    print('Screen ERROR --------------------------------------------------------------')
Speed = [0, 0, 0]
RSpeed = [0, 0, 0]
ShowI = 0
clock = pygame.time.Clock()
tm = time.monotonic()
#font = pygame.font.render('arial', 24)
SwipeR = False
ColorMode = False
AnimationS = 0
AnimTimer = 0
Inform = False
font = None
if hasattr(sys, '_MEIPASS'):
    #print('Record')
    font = os.path.join('arial.otf')
    font = pygame.font.Font(font, 12)
    IsEXE = True
else:
    font = pygame.font.Font(None, 24)
    IsEXE = False
Controlls = True
PAnimS = 0
PAnimT = 0
ShowPhrese = False
while KeepGoing:
    TimeMonot = time.monotonic()
    DeltaTime = TimeMonot - tm
    tm = TimeMonot
    screen.fill(BGColor)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            KeepGoing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                Speed[0] -= SPD
            if event.key == pygame.K_s:
                Speed[0] += SPD
            if event.key == pygame.K_a:
                Speed[1] += SPD
            if event.key == pygame.K_d:
                Speed[1] -= SPD
            if event.key == pygame.K_LCTRL:
                Speed[2] += SPD
            if event.key == pygame.K_SPACE:
                Speed[2] -= SPD
            if event.key == pygame.K_UP:
                RSpeed[1] -= RSPD
            if event.key == pygame.K_DOWN:
                RSpeed[1] += RSPD
            if event.key == pygame.K_LEFT:
                RSpeed[2] -= RSPD
            if event.key == pygame.K_RIGHT:
                RSpeed[2] += RSPD
            if event.key == pygame.K_q:
                AnimationS -= 1
            if event.key == pygame.K_e:
                AnimationS += 1
            if event.key == 61:
                SPD += 500
                RSPD += 1 / 6
            if event.key == 45:
                SPD -= 500
                RSPD -= 1 / 6
            if event.key == pygame.K_2:
                PAnimS += 1
                ShowPhrese = True
            if event.key == pygame.K_1:
                PAnimS -= 1
                ShowPhrese = True
            if event.key == pygame.K_LSHIFT:
                ColorMode = not ColorMode
            if event.key == pygame.K_ESCAPE:
                KeepGoing = False
            if event.key == pygame.K_F2:
                Inform = not Inform
            if event.key == pygame.K_F1:
                Controlls = not Controlls
            if event.key == pygame.K_COMMA:
                MouseSensDiv += 10
            if event.key == pygame.K_PERIOD and MouseSensDiv > 10:
                MouseSensDiv -= 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                Speed[0] -= -SPD
            if event.key == pygame.K_s:
                Speed[0] += -SPD
            if event.key == pygame.K_a:
                Speed[1] += -SPD
            if event.key == pygame.K_d:
                Speed[1] -= -SPD
            if event.key == pygame.K_LCTRL:
                Speed[2] += -SPD
            if event.key == pygame.K_SPACE:
                Speed[2] -= -SPD
            if event.key == pygame.K_UP:
                RSpeed[1] -= -RSPD
            if event.key == pygame.K_DOWN:
                RSpeed[1] += -RSPD
            if event.key == pygame.K_LEFT:
                RSpeed[2] -= -RSPD
            if event.key == pygame.K_RIGHT:
                RSpeed[2] += -RSPD
            if event.key == pygame.K_q:
                AnimationS += 1
            if event.key == pygame.K_e:
                AnimationS -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                SDist += ScalingSPD
            if event.button == 5 and SDist > ScalingSPD * 2:
                SDist -= ScalingSPD
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            SwipeR = True
            pygame.mouse.get_rel()
            pygame.mouse.set_visible(False)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            SwipeR = False
            pygame.mouse.set_visible(True)
    CamPos = Summ(CamPos, MultVect(RotateSpeed(Speed, CamRot[2]), DeltaTime))
    CamRot = Summ(CamRot, MultVect(RSpeed, DeltaTime))
    if SwipeR:
        MRel = pygame.mouse.get_rel()
        CamRot = Summ(CamRot, [0, MRel[1] / MouseSensDiv, MRel[0] / MouseSensDiv])
        #pygame.mouse.set_pos([SCRX / 2, SCRY / 2])
        #pygame.mouse.get_rel()
    AnimTimer += DeltaTime * AnimationS
    ShowI = int(AnimTimer * 10) % N
    period = periods[BCs.index(ShowI)]
    #if 0 <= PAnimT + PAnimS * DeltaTime < Time:
    PAnimT = (PAnimT + (PAnimS * DeltaTime) / 60) % Time
    for i, ln in enumerate(ScreenCoords(ToLocal(CamPos, CamRot, lines), SDist)):
        if (BCs + [-1])[i] != ShowI:
            pygame.draw.line(screen, (colors[i] if period == periods[i] or ColorMode else (50, 50, 50)), Centrix(ln[0], SCRX, SCRY), Centrix(ln[1], SCRX, SCRY), thimbs[i])
        else:
            pygame.draw.line(screen, StepSelectionColor, Centrix(ln[0], SCRX, SCRY), Centrix(ln[1], SCRX, SCRY), 5)
    PhreseLines = PhreseMesh(GetPhresePosition(PAnimT, lines, LGoOnTimes, LPTimes))
    #print(PhreseLines)
    if ShowPhrese:
        for ln in ScreenCoords(ToLocal(CamPos, CamRot, PhreseLines), SDist):
            pygame.draw.line(screen, (255, 255, 0), Centrix(ln[0], SCRX, SCRY), Centrix(ln[1], SCRX, SCRY), 2)
    if Inform:
        #screen.fill((0, 0, 255))
        screen.blit(font.render('Distance to screen surface: ' + str(SDist), 0, (255, 255, 255)), [0, 0])
        screen.blit(font.render('Movement speed: ' + str(SPD), 0, (255, 255, 255)), [0, 30])
        screen.blit(font.render('Arrow rotation speed: ' + str(math.degrees(RSPD)) + '                   Mouse senitive: ' + str(1 / MouseSensDiv), 0, (255, 255, 255)), [0, 60])
        screen.blit(font.render('World camera position: ' + 'X ' + str(-CamPos[0] / Mult) + '   Y ' + str(-CamPos[1] / Mult) + '   Z ' + str(-CamPos[2] / Mult), 0, (255, 255, 255)), [0, 90])
        screen.blit(font.render('World camera rotation: ' + 'X ' + str(CamRot[0] / Mult) + '   Y ' + str(CamRot[1] / Mult) + '   Z ' + str(CamRot[2] / Mult), 0, (255, 255, 255)), [0, 120])
        screen.blit(font.render('Global step: ' + str(ShowI + 1), 0, (255, 255, 255)), [0, 150])
        screen.blit(font.render('Time: ' + ToSeconds(Time), 0, (255, 255, 255)), [0, 180])
        screen.blit(font.render('Step start time: ' + ToSeconds(GoOnTimes[BCs.index(ShowI)]), 0, (255, 255, 255)), [0, 210])
        screen.blit(font.render('Step action time: ' + ToSeconds(PTimes[BCs.index(ShowI)]), 0, (255, 255, 255)), [0, 240])
        screen.blit(font.render('Phrese animation time speed: ' + str(PAnimS), 0, (255, 255, 255)), [0, 270])
        screen.blit(font.render('Global phrese animation time: ' + ToSeconds(PAnimT), 0, (255, 255, 255)), [0, 300])
        LN = Coms[BCs.index(ShowI)]
        SimbMult = 9.5
        if IsEXE:
            SimbMult = 7
        pygame.draw.rect(screen, FrameColor, [0, SCRY - 280, (MaxLen + 4) * SimbMult, 280])
        pygame.draw.rect(screen, SelectionColor, [0, SCRY - 181, (MaxLen + 4) * SimbMult, 16])
        for i in range(-4, 5):
            if 0 <= LN + i < len(ProgText):
                if i != -1:
                    screen.blit(font.render((ProgText[LN + i][:-1] if ProgText[LN + i][-1] == '\n' else ProgText[LN + i]), 0, (255, 255, 255)), [0, SCRY - (5 - i) * 30])
                else:
                    screen.blit(font.render('>>' + ProgText[LN + i][:-1] + '<<', 0, SelectionTextColor), [0, SCRY - (5 - i) * 30])
##        screen.blit(font.render((ProgText[LN - 3][:-1] if LN - 3 >= 0 else ''), 0, (255, 255, 255)), [0, SCRY - 240])
##        screen.blit(font.render((ProgText[LN - 2][:-1] if LN - 2 >= 0 else ''), 0, (255, 255, 255)), [0, SCRY - 210])
##        screen.blit(font.render('>>' + (ProgText[LN - 1][:-1] if LN - 1 >= 0 else '') + '<<', 0, (255, 255, 255)), [0, SCRY - 180])
##        screen.blit(font.render((ProgText[LN][:-1] if LN < len(ProgText) else ''), 0, (255, 255, 255)), [0, SCRY - 150])
##        screen.blit(font.render((ProgText[LN + 1][:-1] if LN < len(ProgText) else ''), 0, (255, 255, 255)), [0, SCRY - 120])
##        screen.blit(font.render((ProgText[LN + 2][:-1] if LN < len(ProgText) else ''), 0, (255, 255, 255)), [0, SCRY - 90])
##        screen.blit(font.render((ProgText[LN + 3][:-1] if LN < len(ProgText) else ''), 0, (255, 255, 255)), [0, SCRY - 60])
##        screen.blit(font.render((ProgText[LN + 4][:-1] if LN < len(ProgText) else ''), 0, (255, 255, 255)), [0, SCRY - 30])
    if Controlls:
        screen.fill((0, 0, 255))
        screen.blit(font.render('Moving - WASD, [LCtrl], [Space]                Zoom - [Mouse wheel Up/Down]', 0, (255, 255, 255)), [0, 0])
        screen.blit(font.render('Rotation - [Arrows] or [Mouse]                 Mous sensitive change - [,], [.]', 0, (255, 255, 255)), [0, 30])
        screen.blit(font.render('Speed change - [+], [-]                        Phrese animation speed change - [1], [2]', 0, (255, 255, 255)), [0, 60])
        screen.blit(font.render('Step change - [Q], [E]', 0, (255, 255, 255)), [0, 90])
        screen.blit(font.render('Show all models in color mode (On/Off) - [LShift]', 0, (255, 255, 255)), [0, 120])
        screen.blit(font.render('World information - [F2]', 0, (255, 255, 255)), [0, 150])
        screen.blit(font.render('Help bar Open/Close - [F1]', 0, (255, 255, 255)), [0, 180])
    pygame.display.update()
    clock.tick(60)
pygame.quit()
