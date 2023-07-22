import warnings
warnings.filterwarnings("ignore")
import sounddevice as sound_device  
import soundfile as sound_file

while True:
    p = input("Enter: ")
    if p != '' and int(p) <= 10 and int(p) > 0:
        data_set, fsample = sound_file.read ( f'Audio/{p}.wav' )
        sound_device.play ( data_set, fsample )
