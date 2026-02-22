# -*- coding: utf-8 -*-
"""
🖥️ Terminal Window - Main UI
"""

import sys
import os
from typing import Optional
from pathlib import Path

class TerminalWindow:
    """Main terminal window"""
    
    def __init__(self, shell=None, i18n=None):
        self.shell = shell
        self. i18n = i18n or self._default_i18n()
        self.running = True
        self.input_buffer = ""
        self.history_position = -1
    
    def _default_i18n(self):
        """Fallback i18n"""
        from core.i18n import I18n
        return I18n('en')
    
    def run(self):
        """Main loop"""
        self._print_banner()
        print(f"\n{self.i18n.t('welcome')}\n")
        
        while self.running and self.shell. session_active:
            try: 
                prompt = self. shell.get_prompt()
                cmd_input = input(prompt).strip()
                
                if not cmd_input:
                    continue
                
                code, output = self.shell.execute(cmd_input)
                
                if output:
                    print(output)
                
                if self.shell.system_map_enabled:
                    print(self.shell._visualize_pipe_chain())
                
            except KeyboardInterrupt:
                print("\n^C")
            except EOFError:
                break
            except Exception as e: 
                print(f"❌ {e}")
    
    def _print_banner(self):
        """Print welcome banner"""
        from commands.ascii_commands import THEMES
        
        theme = self.shell.current_theme if self.shell else 'dos'
        if theme in THEMES:
            print(THEMES[theme]['banner'])
        else:
            print("\n🚀 nextgen-bash v2.0\n")
    
    def exit(self):
        """Exit terminal"""
        self.running = False
        self.shell.session_active = False