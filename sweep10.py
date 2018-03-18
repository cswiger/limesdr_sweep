#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Sweep10
# Generated: Sun Mar 18 15:20:32 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class sweep10(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Sweep10")

        ##################################################
        # Variables
        ##################################################
        self.tx_samp_rate = tx_samp_rate = 15e6
        self.rx_sample_rate = rx_sample_rate = 50e3
        self.frequency = frequency = 925.7e6

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=-10,
        	ref_scale=2.0,
        	sample_rate=rx_sample_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(rx_sample_rate)
        self.osmosdr_source_0.set_center_freq(925.7e6, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(20, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('LNAW', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + 'driver=lime' )
        self.osmosdr_sink_0.set_sample_rate(tx_samp_rate)
        self.osmosdr_sink_0.set_center_freq(frequency, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(0, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('BAND1', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        self.band_pass_filter_0 = filter.fir_filter_ccc(1, firdes.complex_band_pass(
        	1, rx_sample_rate, 500, 1.5e3, 200, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0 = analog.sig_source_c(tx_samp_rate, analog.GR_COS_WAVE, 1e3, 1, 0)
        self.analog_probe_avg_mag_sqrd_x_0 = analog.probe_avg_mag_sqrd_c(0, 1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.analog_probe_avg_mag_sqrd_x_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.band_pass_filter_0, 0))

    def get_tx_samp_rate(self):
        return self.tx_samp_rate

    def set_tx_samp_rate(self, tx_samp_rate):
        self.tx_samp_rate = tx_samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.tx_samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.tx_samp_rate)

    def get_rx_sample_rate(self):
        return self.rx_sample_rate

    def set_rx_sample_rate(self, rx_sample_rate):
        self.rx_sample_rate = rx_sample_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.rx_sample_rate)
        self.osmosdr_source_0.set_sample_rate(self.rx_sample_rate)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.rx_sample_rate, 500, 1.5e3, 200, firdes.WIN_HAMMING, 6.76))

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.osmosdr_sink_0.set_center_freq(self.frequency, 0)


def main(top_block_cls=sweep10, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
