import sys
import sounddevice as sound_device  
import soundfile as sound_file  

p = sys.argv[1]

data_set1, fsample1 = sound_file.read ( 'Audio/0001.wav' )
data_set2, fsample2 = sound_file.read ( 'Audio/0002.wav' )
data_set3, fsample3 = sound_file.read ( 'Audio/0003.wav' )
data_set4, fsample4 = sound_file.read ( 'Audio/0004.wav' )
data_set5, fsample5 = sound_file.read ( 'Audio/0005.wav' )
data_set6, fsample6 = sound_file.read ( 'Audio/0006.wav' )
data_set7, fsample7 = sound_file.read ( 'Audio/0007.wav' )
data_set8, fsample8 = sound_file.read ( 'Audio/0008.wav' )
data_set9, fsample9 = sound_file.read ( 'Audio/0009.wav' )
data_set10, fsample10 = sound_file.read ( 'Audio/0010.wav' )

if p == '1':
    sound_device.play ( data_set1, fsample1 )
elif p == '2':
    sound_device.play ( data_set2, fsample2 )
elif p == '3':
    sound_device.play ( data_set3, fsample3 )
elif p == '4':
    sound_device.play ( data_set4, fsample4 )
elif p == '5':
    sound_device.play ( data_set5, fsample5 )
elif p == '6':
    sound_device.play ( data_set6, fsample6 )
elif p == '7':
    sound_device.play ( data_set7, fsample7 )
elif p == '8':
    sound_device.play ( data_set8, fsample8 )
elif p == '9':
    sound_device.play ( data_set9, fsample9 )
elif p == '10':
    sound_device.play ( data_set10, fsample10 )
