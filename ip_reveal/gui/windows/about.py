import PySimpleGUI as psg
from ip_reveal.config.version import VERSION


class AboutWindow(object):
    def __init__(self):
        self.layout = [
                [psg.Text('IP-Reveal')],
                [psg.Text(VERSION)],
                [psg.Text('https://github.com/Inspyre-Softworks/IP-Reveal')],
                [psg.Button('OK', key='OK_BUTTON')]
                ]
        
        self.running = False
        self.window = psg.Window('About IP-Reveal', layout=self.layout)

    def run(self):
        self.running = True
        while self.running:
            event, vals = self.window.read(timeout=100)
            
            if event is None:
                self.window.hide()
                self.running = False
            
            if event == 'OK_BUTTON':
                self.window.hide()
                self.running = False
            
        