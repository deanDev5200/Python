import cv2
import xlsxwriter
import datetime
from simple_facerec import SimpleFacerec
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
isScanned = [False, False]
studentNames = ['Dean', 'Aline']

worksheet = workbook.add_worksheet('Main')
worksheet.add_table(0, 0, len(studentNames), 1, {'style': 'Table Style Light 13', 'autofilter': 0, 'banded_rows': 0, 'banded_columns': 1,  'first_column': 1, 'columns': [{'header': 'Nama'},
                                           {'header': 'Waktu'},
                                           ]})

y = 0

while y < len(studentNames):
    worksheet.write('A' + str(y + 2), studentNames[y])
    y += 1

while True:
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
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
workbook.close()
cap.release()
cv2.destroyAllWindows()
