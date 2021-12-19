import PySimpleGUIQt as psg
from ip_reveal.config import PARSED_ARGS, CONFIG
from pathlib import Path

from ip_reveal.assets.ui_elements.backgrounds import NEON_DARK_FP


class PreferencesWindow(object):
    
    def __init__(self):
        self.running = False
        
        form = CONFIG.pref_window_specs
        
        self.layout = []
        self.divergant = False
        
        if 'USER' in CONFIG.parser.sections():
            section = 'USER'
        else:
            section = 'DEFAULTS'
        
        for opt in CONFIG.parser.options(section):
            opt_label = opt.replace('_', ' ').capitalize()
            if CONFIG.parser.get(section, opt) in ['True', 'False']:
                self.layout += [
                        [psg.Checkbox(
                                opt_label,
                                key=f'PREF_INPUT_{opt.upper()}',
                                enable_events=True)]]
            elif CONFIG.parser.get(section, opt).isnumeric():
                self.layout += [
                        [
                                psg.Text(opt_label),
                                psg.InputText(
                                        CONFIG.parser.get(section, opt),
                                        key=f'PREF_INPUT_{opt.upper()}',
                                        enable_events=True)
                                ]
                        ]
            elif CONFIG.parser.get(section, opt).isalnum():
                self.layout += [
                        [
                                psg.Text(opt_label),
                                psg.InputText(CONFIG.parser.get(section, opt),
                                              key=f'PREF_INPUT_{opt.upper()}',
                                              enable_events=True
                                              )]
                        ]
            elif '/' in CONFIG.parser.get(section,opt):
                key = f'PREF_INPUT_{opt.upper()}'
                self.layout += [
                        [
                                psg.Text('Config Filepath:'),
                                psg.InputText(CONFIG.parser.get(section, opt), key=f'PREF_INPUT_{opt.upper()}'),
                                psg.FileBrowse(target=key,
                                               initial_folder=str(Path(CONFIG.parser.get(section, opt)).parent),
                                               enable_events=True,
                                               key=key.replace('INPUT', 'BUTTON'))
                
                                ]
                        ]
        buttons = ['Save', 'Reset', 'Cancel']
        
        btn_layout = []
        
        for button in buttons:
            if button == 'Save' or button == 'Reset':
                vis = False
            else:
                vis = True
            _btn = [psg.Button(
                        button,
                        visible=vis,
                        disabled=not vis,
                        key=f"PREF_BUTTON_{button.upper()}")]
            btn_layout.append(_btn)
            
        self.layout += btn_layout
            
        self.window=psg.Window('Preferences', layout=self.layout,
                               background_image=NEON_DARK_FP,)
        
    
    def check_changes(self):
        if self.divergant:
        
            self.window['PREF_BUTTON_RESET'].update(visible=True, disabled=False)
            self.window['PREF_BUTTON_SAVE'].update(visible=True, disabled=False)
        
        else:
    
            self.window['PREF_BUTTON_RESET'].update(visible=False, disabled=True)
            self.window['PREF_BUTTON_SAVE'].update(visible=False, disabled=True)
    
       
       
    def run(self):
        self.running = True
        vals_last_save = None
        while self.running:
            event, values = self.window.read(timeout=100)
            
            if vals_last_save is None:
                vals_last_save = values
                
            vals_differ = (vals_last_save != values)
            
            if vals_differ:
                save_button_color = 'green'
            else:
                save_button_color = 'red'
            
            self.window['PREF_BUTTON_SAVE'].update(disabled=not vals_differ, button_color=('black', save_button_color))
            
            if event is None:
                self.running = False
                self.window.hide()
                
            elif event == 'PREF_BUTTON_CANCEL':
                self.running = False
                self.window.hide()
                
            elif event == 'PREF_BUTTON_SAVE':
                vals_last_save = values
                if 'USER' not in CONFIG.parser.sections():
                    CONFIG.parser.add_section('USER')
                CONFIG.parser.set('USER', 'refresh_interval', str(values['PREF_INPUT_REFRESH_INTERVAL']))
                for val in values:
                    _val = val.split('_INPUT_')[-1].lower()
                    
                    CONFIG.parser.set('USER', _val, str(values[val]))
                    CONFIG.save()
                self.window.hide()
                self.window['PREF_INPUT_REFRESH_INTERVAL'](CONFIG.parser.getint('USER', 'refresh_interval'))
                self.running = False
            elif 'PREF_INPUT' in event:
                self.divergant = True
                if 'PREF_INPUT_CONFIG_FILEPATH' in event:
                    self.window['PREF_INPUT_CONFIG_FILEPATH'].update(str(values['PREF_INPUT_CONFIG_FILEPATH']))
            elif 'PREF_BUTTON' in event:
                if event == 'PREF_BUTTON_CONFIG_FILEPATH':
                    self.divergant = True
                
                if event == 'PREF_BUTTON_RESET':
    
                    self.window['PREF_BUTTON_RESET'].update(visible=False)
                    self.window['PREF_BUTTON_SAVE'].update(visible=False)
                
                    for val in vals_last_save:
                        self.window[val].update(vals_last_save[val])
            
            self.check_changes()
                
