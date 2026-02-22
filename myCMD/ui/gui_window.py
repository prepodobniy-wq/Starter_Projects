# -*- coding: utf-8 -*-
"""
GUI Terminal Window - macOS Console.app style
Clean black background with gray Helvetica text
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
from pathlib import Path
from datetime import datetime


class GUITerminalWindow:   
    """Simple terminal window - macOS Console.app style"""
    
    def __init__(self, shell=None, i18n=None):
        self.shell = shell
        self.i18n = i18n or self._default_i18n()
        self.running = True
        self.font_size = 12
        self.is_fullscreen = False
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Terminal")
        self.root.geometry("1000x700")
        self.root.configure(bg='#000000')
        
        # Bind keyboard shortcuts
        self. root.bind('<F11>', lambda e: self._toggle_fullscreen())
        self.root.bind('<F2>', lambda e: self._show_help())
        self.root.bind('<Control-equal>', lambda e: self._increase_font())
        self.root.bind('<Control-plus>', lambda e: self._increase_font())
        self.root.bind('<Control-minus>', lambda e: self._decrease_font())
        self.root.bind('<Control-0>', lambda e: self._reset_font())
        
        # Setup UI
        self._setup_ui()
        self._print_banner()
        self. input_field. focus()
        
    def _default_i18n(self):
        """Fallback i18n"""
        from core.i18n import I18n
        return I18n('en')
    
    def _setup_ui(self):
        """Setup simple black terminal UI"""
        
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Output text area - pure black background
        self.output_text = tk.Text(
            main_frame,
            bg='#000000',
            fg='#808080',
            font=('Helvetica', self.font_size),
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=15,
            highlightthickness=0,
            insertbackground='#808080'
        )
        self.output_text.pack(fill=tk. BOTH, expand=True, padx=0, pady=0)
        
        # Configure text tags
        self.output_text. tag_config('error', foreground='#FF6B6B')
        self.output_text. tag_config('success', foreground='#808080')
        self.output_text.tag_config('warning', foreground='#FFD93D')
        self.output_text.tag_config('info', foreground='#6DD5FF')
        self.output_text.tag_config('input', foreground='#808080')
        self.output_text.tag_config('prompt', foreground='#808080')
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='#000000')
        input_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Prompt
        prompt_label = tk.Label(
            input_frame,
            text="→ ",
            bg='#000000',
            fg='#808080',
            font=('Helvetica', self.font_size)
        )
        prompt_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Input field
        self.input_field = tk.Entry(
            input_frame,
            bg='#000000',
            fg='#808080',
            font=('Helvetica', self.font_size),
            relief=tk.FLAT,
            bd=0,
            insertbackground='#808080',
            highlightthickness=0
        )
        self.input_field. pack(side=tk.LEFT, fill=tk. BOTH, expand=True)
        self.input_field.bind('<Return>', self._on_input)
        self.input_field.bind('<Up>', self._on_history_up)
        self.input_field.bind('<Down>', self._on_history_down)
        
        # History index
        self.history_index = -1
    
    def _update_prompt(self):
        """Update window title"""
        if self.shell:
            cwd = str(self.shell.cwd).replace(os.path.expanduser('~'), '~')
            user = self.shell.env.get('USER', 'user')
            self.root.title(f"{user} — Terminal — {cwd}")
    
    def _print_banner(self):
        """Print welcome banner"""
        now = datetime.now()
        time_str = now.strftime("%a %b %d %H:%M:%S")
        user = self.shell.env.get('USER', 'user') if self.shell else 'user'
        
        banner = f"Last login: {time_str} on ttys000\n"
        self._write_output(banner, 'info')
        self._update_prompt()
    
    def _write_output(self, text:  str, tag: str = 'input'):
        """Write to output text area"""
        self. output_text.config(state=tk.NORMAL)
        self.output_text. insert(tk.END, text, tag)
        if not text.endswith('\n'):
            self.output_text.insert(tk.END, '\n')
        self.output_text. see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def _on_input(self, event=None):
        """Handle input"""
        cmd_input = self.input_field.get().strip()
        self. input_field.delete(0, tk.END)
        
        if not cmd_input:  
            return
        
        self._write_output(f"→ {cmd_input}", 'input')
        
        try:
            code, output = self.shell.execute(cmd_input)
            
            if output:
                if code == 0:
                    self._write_output(output, 'success')
                else:   
                    self._write_output(output, 'error')
            
            if self.shell.system_map_enabled and self.shell.pipe_chain:    
                self._write_output(self.shell._visualize_pipe_chain(), 'info')
            
            self._update_prompt()
            
        except Exception as e:
            self._write_output(f"Error: {e}", 'error')
    
    def _on_history_up(self, event=None):
        """Navigate history up"""
        if not self.shell. history:   
            return 'break'
        
        if self.history_index == -1:
            self.history_index = len(self.shell.history) - 1
        else:
            self. history_index = max(0, self.history_index - 1)
        
        self. input_field.delete(0, tk.END)
        self.input_field.insert(0, self.shell.history[self. history_index])
        return 'break'
    
    def _on_history_down(self, event=None):
        """Navigate history down"""
        if not self.shell.history:
            return 'break'
        
        if self.history_index < len(self.shell.history) - 1:
            self.history_index += 1
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, self.shell.history[self.history_index])
        else:
            self.history_index = -1
            self.input_field.delete(0, tk.END)
        
        return 'break'
    
    def _show_help(self, event=None):
        """Show help dialog (F2)"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("800x600")
        help_window.configure(bg='#000000')
        
        help_text = tk.Text(
            help_window,
            bg='#000000',
            fg='#808080',
            font=('Helvetica', 11),
            wrap=tk. WORD,
            relief=tk. FLAT,
            bd=0,
            padx=15,
            pady=15,
            highlightthickness=0
        )
        help_text.pack(fill=tk. BOTH, expand=True)
        
        help_content = """KEYBOARD SHORTCUTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
F11             Toggle fullscreen
F2              Show this help
Ctrl + =        Increase font size
Ctrl + -        Decrease font size
Ctrl + 0        Reset font size
↑ / ↓           Navigate history
Enter           Execute command

FILE OPERATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ls [path]       List directory
cd [path]       Change directory
pwd             Show current path
cat <file>      View file
open <file>     Open file
create <file>   Create file
mkdir <dir>     Create directory
rm <file>       Remove file

AI COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ai help <cmd>   Explain command
ai fix          Fix last error
ai bash <text>  Convert to bash

LANGUAGE & THEMES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
lang list       Show languages
lang set <code> Change language
theme list      Show themes
theme set <name> Change theme

EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ ls
→ cd projects
→ cat file.txt
→ ai help grep
→ lang set ru
→ theme set dos

Type 'help' in terminal for full command list. 
"""
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen (F11)"""
        self.is_fullscreen = not self. is_fullscreen
        self. root.state('zoomed' if self.is_fullscreen else 'normal')
        return 'break'
    
    def _increase_font(self):
        """Increase font size"""
        if self.font_size < 18:
            self.font_size += 1
            self._update_font_size()
        return 'break'
    
    def _decrease_font(self):
        """Decrease font size"""
        if self.font_size > 10:
            self. font_size -= 1
            self._update_font_size()
        return 'break'
    
    def _reset_font(self):
        """Reset font size"""
        self.font_size = 12
        self._update_font_size()
        return 'break'
    
    def _update_font_size(self):
        """Update all fonts"""
        self.output_text.config(font=('Helvetica', self.font_size))
        self.input_field. config(font=('Helvetica', self.font_size))
    
    def _on_exit(self):
        """Exit application"""
        if messagebox.askyesno("Quit", "Save session before exit?"):
            self.shell.save_session()
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()