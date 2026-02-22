# -*- coding: utf-8 -*-
"""
Basic Bash-compatible commands
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple


def cmd_ls(args: List[str], shell) -> Tuple[int, str]:  
    """List directory contents"""
    path = args[0] if args else '.'
    
    try:
        p = Path(path)
        if not p.exists():
            return (1, f"[ERROR] {shell.i18n. t('no_file')}: {path}")
        
        if not p.is_dir():
            return (0, str(p. name))
        
        items = sorted([item. name for item in p.iterdir()])
        if not items:
            return (0, "[DIR] (empty)")
        
        output = "[DIR] Contents:\n"
        for item in items:
            full_path = p / item
            if full_path.is_dir():
                output += f"  [D] {item}/\n"
            else:  
                size = full_path.stat().st_size
                output += f"  [F] {item} ({size} bytes)\n"
        
        return (0, output)
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_cd(args: List[str], shell) -> Tuple[int, str]: 
    """Change directory"""
    if not args:
        new_path = Path. home()
    else:
        new_path = Path(args[0])
        if not new_path.is_absolute():
            new_path = shell.cwd / new_path
    
    try:
        if not new_path.exists():
            return (1, f"[ERROR] {shell.i18n.t('no_file')}: {args[0] if args else '~'}")
        
        if not new_path.is_dir():
            return (1, f"[ERROR] Not a directory")
        
        shell.cwd = new_path
        os.chdir(new_path)
        return (0, f"[OK] Changed to:  {shell.cwd}")
    except Exception as e:  
        return (1, f"[ERROR] {e}")


def cmd_pwd(args: List[str], shell) -> Tuple[int, str]:
    """Print working directory"""
    return (0, f"[PATH] {str(shell.cwd)}")


def cmd_clear(args: List[str], shell) -> Tuple[int, str]:
    """Clear screen"""
    os.system('clear' if os.name != 'nt' else 'cls')
    return (0, "")


def cmd_exit(args: List[str], shell) -> Tuple[int, str]:
    """Exit shell"""
    shell.session_active = False
    return (0, "[EXIT] Goodbye!")


def cmd_cat(args: List[str], shell) -> Tuple[int, str]:
    """Display file contents"""
    if not args:
        return (1, "[ERROR] cat: missing filename")
    
    content = ""
    for arg in args:
        if arg.startswith('--stdin='):
            content += arg[8:]
        else:
            try:  
                p = Path(arg)
                if p.exists() and p.is_file():
                    content += p.read_text()
                else:
                    return (1, f"[ERROR] {shell.i18n.t('no_file')}: {arg}")
            except Exception as e:  
                return (1, f"[ERROR] {e}")
    
    return (0, content)


def cmd_head(args: List[str], shell) -> Tuple[int, str]:  
    """Display first lines"""
    lines = 10
    filename = None
    
    for arg in args:
        if arg.startswith('-n'):
            lines = int(arg[2:] or 10)
        else:
            filename = arg
    
    if not filename:
        return (1, "[ERROR] head: missing filename")
    
    try:
        content = Path(filename).read_text().split('\n')
        output = f"[HEAD] First {lines} lines of {filename}:\n"
        output += '\n'.join(content[: lines])
        return (0, output)
    except Exception as e:  
        return (1, f"[ERROR] {e}")


def cmd_tail(args: List[str], shell) -> Tuple[int, str]:
    """Display last lines"""
    lines = 10
    filename = None
    
    for arg in args: 
        if arg.startswith('-n'):
            lines = int(arg[2:] or 10)
        else:
            filename = arg
    
    if not filename:  
        return (1, "[ERROR] tail: missing filename")
    
    try:
        content = Path(filename).read_text().split('\n')
        output = f"[TAIL] Last {lines} lines of {filename}:\n"
        output += '\n'.join(content[-lines:])
        return (0, output)
    except Exception as e: 
        return (1, f"[ERROR] {e}")


def cmd_grep(args: List[str], shell) -> Tuple[int, str]:
    """Search text patterns"""
    if len(args) < 2:
        return (1, "[ERROR] grep: missing operands")
    
    pattern = args[0]
    filename = args[1]
    
    try:
        content = Path(filename).read_text()
        matching = [line for line in content.split('\n') if pattern in line]
        
        if not matching:
            return (0, f"[GREP] No matches for '{pattern}' in {filename}")
        
        output = f"[GREP] Found {len(matching)} match(es) for '{pattern}':\n"
        output += '\n'.join(matching)
        return (0, output)
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_find(args: List[str], shell) -> Tuple[int, str]:
    """Find files by pattern"""
    if not args:
        return (1, "[ERROR] find: missing pattern")
    
    pattern = args[0]
    search_path = Path(args[1]) if len(args) > 1 else shell.cwd
    
    try:  
        results = []
        for p in search_path.rglob(f'*{pattern}*'):
            results.append(str(p))
        
        if not results:  
            return (0, f"[FIND] No matches for '{pattern}'")
        
        output = f"[FIND] Found {len(results)} file(s):\n"
        output += '\n'.join(results)
        return (0, output)
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_echo(args: List[str], shell) -> Tuple[int, str]:
    """Print text"""
    return (0, ' '.join(args))


def cmd_touch(args: List[str], shell) -> Tuple[int, str]:
    """Create empty file"""
    if not args:  
        return (1, "[ERROR] touch: missing filename")
    
    try:
        for filename in args:
            Path(filename).touch()
        return (0, f"[OK] Created {len(args)} file(s)")
    except Exception as e:  
        return (1, f"[ERROR] {e}")


def cmd_mkdir(args: List[str], shell) -> Tuple[int, str]:
    """Create directory"""
    if not args:
        return (1, "[ERROR] mkdir: missing dirname")
    
    try:
        for dirname in args:
            Path(dirname).mkdir(parents=True, exist_ok=True)
        return (0, f"[OK] Created {len(args)} directory/ies")
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_rm(args: List[str], shell) -> Tuple[int, str]:
    """Remove files or directories"""
    if not args:  
        return (1, "[ERROR] rm: missing operand")
    
    try:
        for item in args:
            p = Path(item)
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                shutil. rmtree(p)
            else:
                return (1, f"[ERROR] {shell.i18n.t('no_file')}: {item}")
        return (0, f"[OK] Removed {len(args)} item(s)")
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_open(args: List[str], shell) -> Tuple[int, str]:
    """Open and display file"""
    if not args: 
        return (1, "[ERROR] open: missing filename")
    
    filename = args[0]
    
    try:
        file_path = Path(filename)
        if not file_path.is_absolute():
            file_path = shell.cwd / file_path
        
        if not file_path.exists():
            return (1, f"[ERROR] File not found: {filename}")
        
        if not file_path. is_file():
            return (1, f"[ERROR] Not a file: {filename}")
        
        content = file_path.read_text()
        output = f"\n[FILE] {file_path.name}\n"
        output += "=" * 70 + "\n"
        output += content
        output += "\n" + "=" * 70 + "\n"
        
        return (0, output)
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_create(args: List[str], shell) -> Tuple[int, str]:
    """Create a new file"""
    if not args:  
        return (1, "[ERROR] create: missing filename")
    
    filename = args[0]
    
    try:  
        file_path = Path(filename)
        if not file_path.is_absolute():
            file_path = shell.cwd / file_path
        
        if file_path.exists():
            return (1, f"[ERROR] File already exists: {filename}")
        
        if len(args) > 1:
            content = ' '.join(args[1:])
        else:
            content = ""
        
        file_path.write_text(content)
        
        return (0, f"[OK] Created file:  {filename}\n[PATH] {file_path}")
    except Exception as e: 
        return (1, f"[ERROR] {e}")


def cmd_ui(args: List[str], shell) -> Tuple[int, str]:
    """Show ASCII UI menu"""
    ui_menu = """
 _________________________________________________________________
|                                                                 |
|                    NEXTGEN-BASH UI SYSTEM                      |
|                       Mac OS 9 Classic                          |
|_________________________________________________________________|
|                                                                 |
|  FILE     EDIT     VIEW     UTILITIES    HELP                  |
|  ----     ----     ----     ---------    ----                  |
|                                                                 |
|  [+] About nextgen-bash...                                      |
|  [+] Preferences                                               |
|  [+] Open File...                   Cmd+O                       |
|  [+] Create File...                Cmd+N                       |
|  [-] -----------------------------------------------           |
|  [+] Quit                           Cmd+Q                      |
|                                                                 |
|_________________________________________________________________|
|                                                                 |
|  THEMES & CUSTOMIZATION                                        |
|  _________________                                             |
|                                                                 |
|  [ ] DOS Theme         [ ] Mac Theme       [ ] Hacker         |
|  [ ] Minimal           [ ] Custom...                            |
|                                                                 |
|  FONT SIZE:  [--------====-----]  Current: 11px                 |
|             Min 8            Max 20                            |
|                                                                 |
|_________________________________________________________________|
|                                                                 |
|  COMMANDS QUICK ACCESS                                         |
|  _____________________                                         |
|                                                                 |
|  [FILE]      [TEXT]      [AI]        [SESSION]                |
|  ls          grep        ai help     history                  |
|  cd          echo        ai fix      session save              |
|  pwd         find        ai explain  stats                     |
|  cat         head        ai bash     timeline                  |
|  mkdir       tail                                              |
|  rm          touch                                             |
|  open                                                          |
|  create                                                        |
|                                                                 |
|_________________________________________________________________|
|                                                                 |
|  SYSTEM INFO                                                   |
|  ___________                                                   |
|                                                                 |
|  Shell: nextgen-bash v2.0                                      |
|  Font: Monaco/Courier New                                      |
|  Colors: 256-color support                                     |
|  Shortcuts: F11=Fullscreen  F2=Help  F3=UI  Ctrl+/-=Font      |
|                                                                 |
|_________________________________________________________________|
|                                                                 |
|  VERSION HISTORY                                               |
|  _______________                                               |
|                                                                 |
|  v2.0  - Modern Terminal UI with AI commands                  |
|  v1.5  - Multi-language support added                         |
|  v1.0  - Initial release                                      |
|                                                                 |
|_________________________________________________________________|
"""
    return (0, ui_menu)


def cmd_help(args: List[str], shell) -> Tuple[int, str]:
    """Display help"""
    if args:
        cmd = args[0]
        if cmd in shell.commands:
            doc = shell.commands[cmd].__doc__ or "No help available"
            return (0, f"[HELP] {cmd}:  {doc}")
        return (1, f"[ERROR] Help:  command '{cmd}' not found")
    
    help_text = """
[HELP] NEXTGEN-BASH - Available Commands
================================================================================

FILES:
  ls [path]           - List directory
  cd [path]           - Change directory
  pwd                 - Print working directory
  cat <file>          - Display file
  open <file>         - Open file
  create <file>       - Create file
  touch <file>        - Create empty file
  mkdir <dir>         - Create directory
  rm <file>           - Remove file

TEXT: 
  grep <pattern> <file> - Search text
  echo <text>           - Print text
  head [-n N] <file>    - Show first lines
  tail [-n N] <file>    - Show last lines
  find <pattern>        - Find files

AI:
  ai help <cmd>       - Explain command
  ai fix              - Fix last error
  ai explain          - Explain last command
  ai bash <text>      - Convert to bash

EXTEND:
  mkcmd <name>        - Create custom command
  editcmd <name>      - Edit command
  reloadcmd           - Reload commands
  cmds                - List all commands

SANDBOX:
  sandbox on|off      - Toggle sandbox
  dryrun <cmd>        - Simulate command
  trace <cmd>         - Trace execution

ASCII:
  theme list          - Show themes
  theme set <name>    - Change theme
  ascii banner        - Show banner
  ascii clock         - Show clock

VISUALIZE:
  tree+               - Directory tree
  ls+                 - Files with symbols
  cat+                - Cat with highlights
  preview <file>      - File preview
  pipeviz             - Pipe visualization

SESSION:
  session save        - Save session
  session load        - Load session
  history [N]         - Show history
  stats               - Statistics

LANGUAGE:
  lang list           - Show languages
  lang set <code>     - Change language

UTILITIES:
  ui                  - Show this UI
  help                - Show help
  clear               - Clear screen
  exit                - Exit shell

EXAMPLES:
  → ls
  → cd projects
  → cat file.txt
  → ai help grep
  → ui
  → lang set ru
  → theme set dos
  → history 20

================================================================================
"""
    return (0, help_text)


COMMANDS = {
    'ls': cmd_ls,
    'cd': cmd_cd,
    'pwd': cmd_pwd,
    'clear': cmd_clear,
    'exit': cmd_exit,
    'cat': cmd_cat,
    'head': cmd_head,
    'tail': cmd_tail,
    'grep': cmd_grep,
    'find': cmd_find,
    'echo':  cmd_echo,
    'touch': cmd_touch,
    'mkdir': cmd_mkdir,
    'rm': cmd_rm,
    'open': cmd_open,
    'create': cmd_create,
    'ui': cmd_ui,
    'help': cmd_help,
}