import PySimpleGUI as sg
import shutil
import subprocess
import os
layout = [
    [
        [sg.Text("Nama:"), sg.InputText()], 
        [sg.FileBrowse(button_text='Cari Gambar', file_types=(('JPG Image', '*.jpg; *.jpeg'),)), sg.Text('*Hanya File .jpg/.jpeg')], 
        [sg.Button("Tambah Nama")],
        [sg.Button('Hapus Nama')],
        [sg.Button("Buat File JSON"), sg.Text('*Jika File data.json Rusak atau Tidak Ada')]
    ]]

def updateJsonFile(deleteFirst):
    p = subprocess.check_output('cd faces/ & dir /B', shell=True, universal_newlines=True)
    if p.find('.jpg') != -1:
        d = None
        h = subprocess.check_output('dir /B', shell=True, universal_newlines=True)
        if h.find('data.json') == -1:
            d = open('data.json', 'xt')
            print('File data.json Dibuat')
        else:
            if deleteFirst:
                subprocess.check_output('erase data.json', shell=True, universal_newlines=True)
                d = open('data.json', 'xt')
                print('File data.json Dibuat Ulang')
            else:
                d = open('data.json', 'wt')
                print('File data.json Dibaca')
        k = '{\n        "names": ['

        
        o = p.replace('\n', ':')
        o = o.split(':')
        x = 0
        while x < len(o):
            if o[x].find('.jpg') != -1:
                k += ',"' + o[x].replace('.jpg', '') + '"'
            x += 1

        k += ']\n}'
        k = k.replace('[,', '[')
        d.write(k)
        d.close()
        print('Update data.json Berhasil')
    else:
        print('Tidak Ada Data Gambar Apapun')

def tambahNama(values):
        p = subprocess.check_output('dir /B /A:D', shell=True, universal_newlines=True)
        f =  p.find("faces")

        if p[f-1] != "\n":
            if p[f+5] != "\n":
                os.mkdir('faces/')

        shutil.copyfile(values['Cari Gambar'], './faces/' + values[0] + '.jpg')
        updateJsonFile(False)

def hapusNama(values):
        p = subprocess.check_output('dir /B /A:D', shell=True, universal_newlines=True)
        f =  p.find("faces")

        if p[f-1] == "\n":
            if p[f+5] == "\n":
                b = subprocess.check_output('cd faces/ & dir /B', shell=True, universal_newlines=True)

                if b.find(values[0] + '.jpg') != -1:
                    d = subprocess.check_output('cd faces/ & erase "' + values[0] + '.jpg"', shell=True, universal_newlines=True)
                    updateJsonFile(False)

                p = subprocess.check_output('cd faces/ & dir /B', shell=True, universal_newlines=True)
                print("Sebelum:\n" + b)
                print("Sesudah:\n" + p)

def printNama():
        p = subprocess.check_output('dir /B /A:D', shell=True, universal_newlines=True)
        f =  p.find("faces")

        if p[f-1] == "\n":
            if p[f+5] == "\n":
                p = subprocess.check_output('cd faces/ & dir /B', shell=True, universal_newlines=True)
                print(p)

window = sg.Window("Kelola Nama", layout)

while True:

    event, valuesraw = window.read() # type: ignore
    if event == "Tambah Nama" and (valuesraw[0] != "" and valuesraw['Cari Gambar'] != ""):
        tambahNama(values=valuesraw)

    elif event == "Hapus Nama" and valuesraw[0] != "":
        hapusNama(values=valuesraw)

    elif event == "Hapus Nama":
        printNama()

    elif event == "Buat File JSON":
        p = subprocess.check_output('dir /B /A:D', shell=True, universal_newlines=True)
        f =  p.find("faces")

        if p[f-1] == "\n":
            if p[f+5] == "\n":
                updateJsonFile(True)

            
    elif event == sg.WIN_CLOSED:
        break

window.close()