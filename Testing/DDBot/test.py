import sounddevice as sd
from pydub import AudioSegment
import soundfile as sf
sd.default.device = 2
sd.default.samplerate = 48000

s = AudioSegment.from_file('ttstmp.mp3')
f = s.set_frame_rate(48000)
f.export('ttstmp2.mp3', format="mp3", bitrate="48000")
data, fs = sf.read('ttstmp2.mp3')
sd.play(data)
sd.wait()
