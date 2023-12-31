# credits:
#     freq2sound: https://stackoverflow.com/a/27978895
#     stream_sound: https://stackoverflow.com/a/27978895
#     bytearray: https://stackoverflow.com/a/28130794

import io, pyaudio, numpy, wave

sampling_rate: int = 44100

def freq2sound(freq: float, duration: float = 0.5, volume: float = 0.5, sampling_rate: int = sampling_rate) -> bytes:
	samples = (numpy.sin(2 * numpy.pi * numpy.arange(sampling_rate * duration) * freq / sampling_rate)).astype(numpy.float32)
	return (volume * samples).tobytes()

def stream_sound(audio: bytes, output_format = pyaudio.paFloat32, channels = 1, sampling_rate: int = sampling_rate, output: bool = True) -> None:
	p = pyaudio.PyAudio()
	stream = p.open(format = output_format, channels = channels, rate = sampling_rate, output = output)
	stream.write(audio)
	stream.stop_stream()
	stream.close()
	p.terminate()

_ch: list[str] = [chr(i) for i in range(128)]
_freq = range(200,455,2)
ch_freq_map: dict[str,int] = dict(zip(_ch, _freq))
ch_sound_map: dict[str, bytes] = {ch:freq2sound(freq) for (ch, freq) in ch_freq_map.items()}

text: str = input('Enter string:\n > ')

sounds = bytearray()
for ch in text:
	sounds.extend(bytearray(ch_sound_map[ch]))

stream_sound(bytes(sounds))
