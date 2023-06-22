import cv2
import xlsxwriter
import datetime
import json
import PySimpleGUI as sg
import subprocess
import os
from simple_facerec import SimpleFacerec

layout = [
    [
        [sg.Button("Mulai"), sg.Text("*Mulai Program Absen")],
        [sg.Button("Berhenti"), sg.Text('*Hentikan Program Absen')],
        [sg.Button("Keluar"), sg.Text('*Keluar Dari Program Absen')]
    ]]

isScanned = []
studentNames = []
isStart = False
isValid = False
notValid = 'Tidak Ada Gambar Dari: | '
h = subprocess.check_output('dir /B', shell=True, universal_newlines=True)

a = subprocess.check_output('dir /B /A:D', shell=True, universal_newlines=True)

f =  a.find("output")

if f == -1:
    os.mkdir('output/')
elif a[f-1] != "\n":
    if a[f+6] != "\n":
        os.mkdir('output/')

if h.find('data.json') != -1:
    studentNames.clear()
    dataFile = open('data.json', 'rt')
    dataObj = json.load(dataFile)
    x = 0
    while x < len(dataObj['names']):
        studentNames.append(dataObj['names'][x])
        x += 1
    f = subprocess.check_output('cd "Tes Gambar/" & dir /B', shell=True, universal_newlines=True)
    y = 0
    x = 0
    while x < len(studentNames):
        if f.find(studentNames[x] + '.jpg') != -1:
            y += 1
            print("Jumlah Data Valid: " + str(y) + '/' + str(len(studentNames)) + ' : ' + studentNames[x])
        else:
            notValid += studentNames[x] + ' | '
        x += 1
    if y == len(studentNames):
        isScanned.clear()
        x = 0
        while x < len(studentNames):
            isScanned.append(False)
            x += 1
        isValid = True
    elif y == 0:
        notValid = "Tidak Ada Gambar Dari: | SEMUANYA | "
    x = 0
else:
    notValid = "Tidak Ada data.json"

window = sg.Window("Absensi Face Recognition", layout)
if isValid:
    sfr = SimpleFacerec()
    sfr.load_encoding_images("faces/")
    dow = 'Minimal'
    curr_date = datetime.date.today()
    if curr_date.weekday() == 0:
        dow = 'Senin'
    elif curr_date.weekday() == 1:
        dow = 'Selasa'
    elif curr_date.weekday() == 2:
        dow = 'Rabu'
    elif curr_date.weekday() == 3:
        dow = 'Kamis'
    elif curr_date.weekday() == 4:
        dow = 'Jumat'
    elif curr_date.weekday() == 5:
        dow = 'Sabtu'

    workbook = xlsxwriter.Workbook('output/Absen ' + str(datetime.datetime.now()).split(' ')[0] + ' ' + dow + '.xlsx')
    lastDate = str(datetime.datetime.now()).split(' ')[0]
    cap = cv2.VideoCapture(0)

    worksheet = workbook.add_worksheet('Main')
    worksheet.add_table(0, 0, len(studentNames), 1, {'style': 'Table Style Light 13', 'autofilter': 0, 'banded_rows': 0, 'banded_columns': 1,  'first_column': 1, 'columns': [{'header': 'Nama'},
                                            {'header': 'Waktu'},
                                            ]})

    y = 0

    while y < len(studentNames):
        worksheet.write('A' + str(y + 2), studentNames[y])
        y += 1

    while True:
        event, values = window.read(0.5) # type: ignore
        if event == 'Mulai':
            isStart = True
        elif event == 'Berhenti':
            isStart = False
        elif event == 'Keluar':
            break 
        elif event == sg.WIN_CLOSED:
            break

        if isStart == True:
            rawdatetime = str(datetime.datetime.now())

            date = rawdatetime.split(' ')[0]
            if date != lastDate:
                x = 0
                while x < len(isScanned):
                    isScanned[x] = False
                    x += 1
                workbook.close()

                curr_date = datetime.date.today()
                if curr_date.weekday() == 0:
                    dow = 'Senin'
                elif curr_date.weekday() == 1:
                    dow = 'Selasa'
                elif curr_date.weekday() == 2:
                    dow = 'Rabu'
                elif curr_date.weekday() == 3:
                    dow = 'Kamis'
                elif curr_date.weekday() == 4:
                    dow = 'Jumat'
                elif curr_date.weekday() == 5:
                    dow = 'Sabtu'

                workbook = xlsxwriter.Workbook('output/Absen ' + str(datetime.datetime.now()).split(' ')[0] + ' ' + dow + '.xlsx')

                worksheet = workbook.add_worksheet('Main')
                worksheet.add_table(0, 0, len(studentNames), 1, {'style': 'Table Style Light 13', 'banded_rows': 0, 'banded_columns': 1, 'autofilter': 0, 'first_column': 1, 'columns': [{'header': 'Nama'},
                                                {'header': 'Waktu'},
                                                ]})

                y = 0

                while y < len(studentNames):
                    worksheet.write('A' + str(y + 2), studentNames[y])
                    y += 1
                lastDate = date


            ret, frame = cap.read()
            face_locations, face_names = sfr.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                if name != 'Unknown':
                    x = 0
                    while x < len(studentNames):
                        if name[0] == studentNames[x] and isScanned[x] == False:
                            curr_date = datetime.date.today()
                            rawtime = rawdatetime.split(' ')[1]
                            time = rawtime.split('.')[0]

                            print(x)
                            worksheet.write('B' + str(x + 2), time)
                            isScanned[x] = True
                        x += 1
                    cv2.putText(frame, name[0],(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
                cv2.rectangle(frame, (x1, y1, x2, y2), (0, 0, 200), 4)

            cv2.imshow("Frame", frame)
        else:
            cv2.destroyAllWindows()

    workbook.close()
    window.close()
    cap.release()
    cv2.destroyAllWindows()
else:
    print("Data Tidak Valid: " + notValid)