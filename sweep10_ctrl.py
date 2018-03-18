#!/usr/bin/python
import threading

from sweep10 import *

tb = sweep10()

f = -6e6
fc = f + 925.7e6
def foo():
   global f,fc
   print(fc,tb.analog_probe_avg_mag_sqrd_x_0.level())
   fc = f + 925.7e6
   tb.analog_sig_source_x_0.set_frequency(f+1e3)
   tb.osmosdr_source_0.set_center_freq(fc, 0)
   tb.wxgui_fftsink2_0.set_baseband_freq(fc)
   f += 1e3
   if (f > 6e6):
     f = -6e6
   threading.Timer(1,foo).start()

tb.Start(True)
foo()
tb.Wait()

