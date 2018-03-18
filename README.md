# limesdr_sweep

sweep10.pyc - gnuradio companion graph<br/>
sweep10.py  - gnuradio companion output of generate the flow graph<br/>
sweep10_ctrl.py  -  first control script, only one xmit band, imports the grc graph, instantiates the class and sweeps a freq from -6e6 to 6e6 over the 15MHz wide band, displaying the fft.  Run with a 10db attenuation from output on TX1_1 (BAND1) to LNAW <br/>
sweep10_ctrl_2.py - 2nd control script for wide band, adjusts the transmit freq up as it goes.<br/>

