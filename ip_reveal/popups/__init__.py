import PySimpleGUI as GUI
from assets.ui_elements.icons.alerts import icons_alert_shield
import simpleaudio as sa
from threading import Thread
import os

pwd = os.getcwd()
audio_asset_lib_path = pwd + "/assets/sounds/alerts"


class AlertSounds(object):
    def __init__(self):
        self.asset_pathlib = audio_asset_lib_path
        self.o_pulse_alert = sa.WaveObject.from_wave_file(self.asset_pathlib + "/o-pulse-alert.wav")

    def high(self):
        self.o_pulse_alert.play()

    def moderate(self):
        pass

    def minor(self):
        pass


def ip_change_notify(old, new):
    bell = AlertSounds()
    bell.high()
    GUI.popup_notify(f'Your external IP address has changed from {old} to {new}', display_duration_in_ms=7000, alpha=.8,
                     location=(750, 450), icon=icons_alert_shield)
