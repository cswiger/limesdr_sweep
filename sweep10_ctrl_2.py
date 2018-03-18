#!/usr/bin/python
import threading
from time import sleep
import sys

from sweep10 import *

f_start = 400e6
f_end = 500e6
# bw is 15MHz so sweep from -6 to +6MHz
fs_start = -6e6
fs_end = 6e6
# offset for the filter and probe
f_offset = 1e3
# frequency increment per step
f_inc = 100e3

# starting center freq is f_start + 1/2 BW, which fs_end is also
fc = f_start + fs_end

# instantiate the grc class
tb = sweep10()

# set initial xmit freq
tb.osmosdr_sink_0.set_center_freq(fc, 0)

# f sweeps from fs_start to fs_end then re-adjust the xmit freq until fs_end > f_end
f = fs_start
# set waveform to f plus the offset for the filter and probe
tb.analog_sig_source_x_0.set_frequency(f+f_offset)

def sweeper():
   global f,fc,fs_start,fs_end,f_end,f_inc
   # get the probe reading from the last setting
   print(fc+f,tb.analog_probe_avg_mag_sqrd_x_0.level())
   f += f_inc
   if (f > fs_end):
     # time to reset xmit freq up 12Mhz
     fc += 12e6
     # this could be more granular but for now... if the center freq is more than f_end stop, somehow
     if (fc > f_end):
        tb.stop
        # this will stop output but leaves the fft running, until is is closed
        sys.exit(0)
     # bump up the transmitter
     tb.osmosdr_sink_0.set_center_freq(fc, 0)
     f = fs_start
   # set the waveform frequency
   tb.analog_sig_source_x_0.set_frequency(f+1e3)
   # and the receiver
   tb.osmosdr_source_0.set_center_freq(fc+f, 0)
   tb.wxgui_fftsink2_0.set_baseband_freq(fc+f)
   # settle for a second and repeat
   threading.Timer(1,sweeper).start()

tb.Start(True)
sweeper()
tb.Wait()

