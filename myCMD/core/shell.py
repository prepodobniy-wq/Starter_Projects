# -*- coding: utf-8 -*-
"""
🧠 Shell Core Engine
Parses and executes commands without UI dependency
"""

import os
import json
import re
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Callable
from datetime import datetime
from importlib import import_module


class ShellCore:
    """Core shell engine - parses and executes commands"""
    
    def __init__(self, commands_path: Path, plugins_path: Path, 
                 sandbox_enabled: bool = True, i18n=None):
        self.commands_path = commands_path
        self.plugins_path = plugins_path
        self.sandbox_enabled = sandbox_enabled
        
        if i18n is None:
            from . i18n import I18n
            i18n = I18n('en')
        self.i18n = i18n
        
        # State
        self.history: List[str] = []
        self.history_index = -1
        self.last_command = ""
        self.last_error:  Optional[str] = None
        self.last_output = ""
        self.env:  Dict[str, str] = dict(os.environ)
        self.cwd = Path.cwd()
        self.session_active = True
        self. dryrun_mode = False
        self.trace_mode = False
        self. current_theme = 'dos'
        
        # Visual system map
        self.system_map_enabled = False
        self.pipe_chain:  List[Dict[str, Any]] = []
        
        # Variables and functions
        self.variables: Dict[str, str] = {}
        
        # Performance tracking
        self.last_command_time = 0.0
        
        # Load commands
        self.commands:  Dict[str, Callable] = {}
        self. plugins: Dict[str, Any] = {}
        self.builtin_cmds = [
            'bash_commands',
            'ai_commands',
            'extend_commands',
            'sandbox_commands',
            'ascii_commands',
            'viz_commands',
            'session_commands',
            'language_commands'
        ]
        
        self.load_builtin_commands()
        self.load_custom_commands()
        self.load_plugins()
    
    def load_builtin_commands(self):
        """Load built-in commands"""
        for cmd_module in self.builtin_cmds:
            try:
                sys.path.insert(0, str(self.commands_path. parent))
                module = import_module(f'commands.{cmd_module}')
                
                if hasattr(module, 'COMMANDS'):
                    cmds_dict = module.COMMANDS
                    for cmd_name, cmd_func in cmds_dict.items():
                        if callable(cmd_func):
                            self.commands[cmd_name] = cmd_func
            except Exception as e:
                print(f"⚠️ Warning: Failed to load {cmd_module}: {e}", file=sys.stderr)
    
    def load_custom_commands(self):
        """Load custom commands from commands/ directory"""
        if not self.commands_path.exists():
            return
        
        for py_file in sorted(self.commands_path.glob('*.py')):
            if py_file.name.startswith('_') or py_file.name.startswith('.'):
                continue
            
            try:
                spec = __import__('importlib.util').util. spec_from_file_location(
                    f"custom_{py_file.stem}", py_file
                )
                if spec and spec.loader:
                    module = __import__('importlib.util').util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, 'run'):
                        self.commands[py_file.stem] = module.run
            except Exception as e:
                self.last_error = f"Failed to load command {py_file.stem}: {e}"
    
    def load_plugins(self):
        """Load plugins"""
        if not self.plugins_path.exists():
            return
        
        for py_file in sorted(self.plugins_path. glob('*.py')):
            if py_file.name.startswith('_'):
                continue
            
            try:
                spec = __import__('importlib.util').util.spec_from_file_location(
                    f"plugin_{py_file.stem}", py_file
                )
                if spec and spec.loader:
                    module = __import__('importlib.util').util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    self.plugins[py_file.stem] = module
                    if hasattr(module, 'initialize'):
                        module.initialize(self)
            except Exception as e:
                self.last_error = f"Failed to load plugin {py_file.stem}: {e}"
    
    def parse_command(self, cmd_str: str) -> List[str]:
        """Parse command string into tokens"""
        cmd_str = cmd_str.strip()
        if not cmd_str:
            return []
        
        if '#' in cmd_str:
            cmd_str = cmd_str[:cmd_str.index('#')]
        
        tokens = re.split(r'(\|{1,2}|&&|\|\||>>?  |\s+)', cmd_str)
        tokens = [t for t in tokens if t and not t.isspace()]
        
        return tokens
    
    def execute(self, cmd_str: str) -> Tuple[int, str]:
        """Execute command string.  Returns (return_code, output)"""
        if not cmd_str. strip():
            return (0, "")
        
        self.last_command = cmd_str
        self.history.append(cmd_str)
        self.history_index = len(self.history) - 1
        self.pipe_chain = []
        
        start_time = time.time()
        
        try:
            tokens = self.parse_command(cmd_str)
            
            if not tokens:
                return (0, "")
            
            if '|' in tokens:
                result = self._execute_pipe(tokens)
            elif '&&' in tokens or '||' in tokens:
                result = self._execute_logical(tokens)
            else:
                result = self._execute_simple(tokens)
            
            self.last_command_time = time.time() - start_time
            return result
        
        except Exception as e: 
            self.last_error = str(e)
            return (1, f"❌ {self.i18n.t('error')}: {e}")
    
    def _execute_simple(self, tokens: List[str]) -> Tuple[int, str]:
        """Execute simple command"""
        if not tokens:
            return (0, "")
        
        cmd = tokens[0]
        args = tokens[1:]
        
        if cmd not in self.commands:
            self.last_error = f"{cmd}:  {self.i18n.t('command_not_found')}"
            return (127, f"❌ {self.last_error}")
        
        if self.dryrun_mode:
            return (0, f"[DRYRUN] Would execute: {cmd} {' '.join(args)}")
        
        if self.trace_mode:
            print(f"[TRACE] 📍 Executing: {cmd} {' '.join(args)}")
        
        try:
            result = self.commands[cmd](args, self)
            if isinstance(result, tuple):
                return result
            return (0, str(result))
        except Exception as e:
            self.last_error = str(e)
            return (1, f"❌ {e}")
    
    def _execute_pipe(self, tokens: List[str]) -> Tuple[int, str]:
        """Execute piped commands"""
        pipes = []
        current = []
        
        for token in tokens:
            if token == '|':
                if current: 
                    pipes.append(current)
                    current = []
            else:
                current. append(token)
        
        if current:
            pipes.append(current)
        
        input_data = ""
        for pipe in pipes:
            if not pipe:
                continue
            
            cmd = pipe[0]
            args = list(pipe[1:])
            
            if cmd not in self. commands:
                return (127, f"❌ {cmd}: {self.i18n. t('command_not_found')}")
            
            try:
                if input_data:
                    args.append(f"--stdin={input_data}")
                
                result = self.commands[cmd](args, self)
                input_data = str(result[1] if isinstance(result, tuple) else result)
                
                self.pipe_chain.append({
                    'command': cmd,
                    'args': args[: len(pipe)-1],
                    'output_lines': len(input_data.split('\n'))
                })
            except Exception as e:
                return (1, f"❌ {e}")
        
        self.last_output = input_data
        return (0, input_data)
    
    def _execute_logical(self, tokens: List[str]) -> Tuple[int, str]:
        """Execute with && and || operators"""
        result_code = 0
        result_output = ""
        
        i = 0
        while i < len(tokens):
            cmd_tokens = []
            while i < len(tokens) and tokens[i] not in ('&&', '||'):
                cmd_tokens.append(tokens[i])
                i += 1
            
            if cmd_tokens: 
                code, output = self._execute_simple(cmd_tokens)
                result_output += output
                result_code = code
            
            if i < len(tokens):
                operator = tokens[i]
                i += 1
                
                if operator == '&&' and result_code != 0:
                    break
                elif operator == '||' and result_code == 0:
                    break
        
        return (result_code, result_output)
    
    def reload_commands(self):
        """Hot-reload commands"""
        self.commands. clear()
        self.load_builtin_commands()
        self.load_custom_commands()
        return (0, "✅ Commands reloaded successfully")
    
    def save_session(self, filename: str = "session.json"):
        """Save session"""
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'language': self.i18n.language,
            'history': self.history[-50:],
            'cwd': str(self.cwd),
            'theme': self.current_theme,
        }
        
        try:
            session_file = Path(filename)
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            return (0, f"✅ {self.i18n.t('session_saved')}")
        except Exception as e:
            return (1, f"❌ {e}")
    
    def load_session(self, filename: str = "session.json"):
        """Load session"""
        session_file = Path(filename)
        if not session_file.exists():
            return (1, f"❌ {self.i18n.t('no_file')}")
        
        try: 
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            self.history = session_data.get('history', [])
            self.cwd = Path(session_data.get('cwd', '.'))
            self.current_theme = session_data. get('theme', 'dos')
            
            return (0, f"✅ {self. i18n.t('session_loaded')}")
        except Exception as e:
            return (1, f"❌ {e}")
    
    def get_prompt(self) -> str:
        """Generate shell prompt"""
        user = self.env.get('USER', 'user')
        cwd = str(self.cwd).replace(os.path.expanduser('~'), '~')
        
        GREEN = '\033[32m'
        CYAN = '\033[36m'
        RESET = '\033[0m'
        
        return f"{GREEN}{user}@nextgen{RESET}:{CYAN}{cwd}{RESET}$ "
    
    def _visualize_pipe_chain(self) -> str:
        """Visualize pipe chain"""
        if not self.pipe_chain:
            return "📊 No pipe chain to visualize"
        
        output = "\n┌─ PIPE CHAIN ──────────────────────┐\n│\n"
        
        for i, step in enumerate(self.pipe_chain):
            cmd = step['command']
            lines = step['output_lines']
            arrow = "→" if i < len(self. pipe_chain) - 1 else ""
            output += f"│ [{cmd}] {arrow} ({lines} lines)\n"
        
        output += "│\n└────────────────────────────────────┘\n"
        
        return output