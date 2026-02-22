# -*- coding: utf-8 -*-
"""
Command extension system
"""

from pathlib import Path
from typing import List, Tuple


def cmd_mkcmd(args: List[str], shell) -> Tuple[int, str]:
    """Create new custom command"""
    if not args: 
        return (1, "[ERROR] mkcmd: missing command name")
    
    cmd_name = args[0]
    cmd_file = shell.commands_path / f"{cmd_name}.py"
    
    template = f'''# -*- coding: utf-8 -*-
"""
Custom command:  {cmd_name}
"""


def run(args, shell):
    """Execute {cmd_name}
    
    Args:
        args: Command arguments
        shell: ShellCore instance
    
    Returns: 
        (return_code, output)
    """
    return (0, "[OK] Hello from {cmd_name}!")
'''
    
    try:
        if cmd_file.exists():
            return (1, f"[ERROR] Command '{cmd_name}' already exists")
        
        cmd_file.write_text(template)
        shell.load_custom_commands()
        return (0, f"[OK] Created command '{cmd_name}'")
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_editcmd(args: List[str], shell) -> Tuple[int, str]:
    """Edit custom command"""
    if not args: 
        return (1, "[ERROR] editcmd: missing command name")
    
    cmd_name = args[0]
    cmd_file = shell.commands_path / f"{cmd_name}.py"
    
    if not cmd_file.exists():
        return (1, f"[ERROR] Command '{cmd_name}' not found")
    
    content = cmd_file.read_text()
    return (0, f"[EDIT] File:  {cmd_file}\n\n{content}")


def cmd_reloadcmd(args: List[str], shell) -> Tuple[int, str]: 
    """Reload commands"""
    try:
        shell.reload_commands()
        return (0, "[OK] Commands reloaded")
    except Exception as e: 
        return (1, f"[ERROR] {e}")


def cmd_cmds(args: List[str], shell) -> Tuple[int, str]:
    """List all commands"""
    cmds_list = sorted(list(shell.commands.keys()))
    
    output = f"\n[COMMANDS] Total:  {len(cmds_list)}\n"
    output += "=" * 60 + "\n"
    
    for cmd in cmds_list:
        output += f"  {cmd}\n"
    
    return (0, output)


COMMANDS = {
    'mkcmd': cmd_mkcmd,
    'editcmd': cmd_editcmd,
    'reloadcmd': cmd_reloadcmd,
    'cmds': cmd_cmds,
}