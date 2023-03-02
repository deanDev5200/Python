import datetime
import wikipedia as wp
import sys

hi = ['hi', 'hello', 'hey', 'yo', 'sup']
timeword = ['jam berapa sekarang', 'bisakah anda memberi tahu aku waktunya', 'permisi, bolehkah aku tahu waktunya']
dateword = ['tanggal berapa sekarang', 'bisakah kamu memberi tahu aku tanggal berapa sekarang']
hayword = ['apa kabar', 'bagaimana kabar anda']
askinakuord = ["siapa ", "apa itu ", "dimana ", "kapan "]
wp.set_lang("id")
x = sys.argv[1]
x = x.replace(".", " ")

answer = ""
x = x.lower()
i = 0

if x == "apakah kamu tahu dean putra" or x == "siapa dean putra":
        answer = "Dean Putra adalah inovator muda cerdas dan penggemar fabrikasi digital\nDean Putra Berumur 12 Tahun dan Berasal dari Desa Tamblang, Buleleng, Bali belajar elektronika, robotika, coding dan fabrikasi digital secara mandiri.\nDean Putra juga mempunyai channel youtube namanya DEAN DEV"
if x == "siapa yang akan menjadi presiden indonesia tahun 2024":
        answer = "Oke, ini adalah prediksi yang sangat berat bagiku untuk menjawabnya tapi aku akan coba, prediksi yang akan terpilih menjadi presiden Indonesia di tahun 2024 berdasarkan survey adalah Dean Putra, dia anak yang ganteng, keren, senyumnya manis dan hebat"

while i < len(hi):
    if x == hi[i] and answer == "":
        answer = 'Hai, Ada yang bisa aku bantu?'
    i = i + 1
i = 0
while i < len(timeword):
    if x == timeword[i] and answer == "":
        time = datetime.datetime.now().time()
        answer = 'Sekarang jam ' + str(time.hour) + ' lebih ' + str(time.minute) + ' menit'
        isAnswered = True
        break
    i = i + 1
i = 0
while i < len(dateword):
    if x == dateword[i] and answer == "":
        answer = 'Sekarang tanggal: ' + str(datetime.datetime.now().date())
        break
    i = i + 1
i = 0
while i < len(hayword):
    if x == hayword[i] and answer == "":
        answer = 'aku baik-baik saja'
        isAnswered = True
        break
    i = i + 1
i = 0
while i < len(askinakuord) and answer == "":
    if x.find(askinakuord[i]) != -1:
        quest = x.split(askinakuord[i])[1].lstrip()
        if len(wp.search(quest)) > 0:
            res = wp.summary(wp.search(quest)[0])
            res = res.replace('"', "'")
            answer = bytes(res, 'utf-8')
        else: pass
        break
    i = i + 1

if answer == "":
    print("Aku Tidak Mengerti")
else:
    print(answer)