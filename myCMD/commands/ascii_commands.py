# -*- coding: utf-8 -*-
"""
ASCII Art and visual commands with working themes
"""

from typing import List, Tuple
from datetime import datetime


THEMES = {
    'dos': {
        'name': 'MS-DOS',
        'description': 'Classic MS-DOS green on black',
        'banner': """
================================================================================
                    MS-DOS NEXTGEN-BASH v2.0
                Type 'help' for available commands
              Powered by Python 3.10+
================================================================================
        """,
    },
    'mac': {
        'name': 'macOS',
        'description': 'Modern macOS terminal style',
        'banner': """
================================================================================
                NEXTGEN-BASH - macOS Terminal Style
                   Type 'help' for commands
================================================================================
        """,
    },
    'hacker': {
        'name': 'Hacker',
        'description': 'Hacker/Matrix style',
        'banner': """
================================================================================
                        NEXTGEN-BASH
                      HACKER MODE
                Initializing kernel...
                All systems online
================================================================================
        """,
    },
    'minimal': {
        'name': 'Minimal',
        'description': 'Minimal design',
        'banner': """
NEXTGEN-BASH v2.0
Type 'help' for commands
        """,
    },
}


def cmd_theme(args: List[str], shell) -> Tuple[int, str]:
    """Manage themes"""
    if not args: 
        themes = ', '.join(THEMES.keys())
        return (0, f"[INFO] Available themes: {themes}\n[INFO] Usage: theme list | theme set <name>\n[INFO] Current theme: {shell.current_theme}")
    
    if args[0] == 'list':
        output = "\n[THEMES] Available:\n"
        output += "=" * 60 + "\n"
        for code, theme_data in THEMES.items():
            current = " <- CURRENT" if code == shell.current_theme else ""
            output += f"  {code:10s} : {theme_data['description']: 30s}{current}\n"
        return (0, output)
    
    if args[0] == 'set' and len(args) > 1:
        theme_name = args[1]
        if theme_name not in THEMES:
            return (1, f"[ERROR] Theme '{theme_name}' not found\n[INFO] Use 'theme list' to see available themes")
        
        shell.current_theme = theme_name
        return (0, f"[OK] Theme changed to {THEMES[theme_name]['name']}")
    
    return (1, "[ERROR] Usage: theme list | theme set <name>")


def cmd_ascii(args: List[str], shell) -> Tuple[int, str]: 
    """ASCII art utilities"""
    if not args: 
        return (1, "[ERROR] ascii:  missing subcommand\n[INFO] Usage: ascii banner | ascii clock | ascii matrix")
    
    subcmd = args[0]
    
    if subcmd == 'banner':
        theme_name = args[1] if len(args) > 1 else shell.current_theme
        if theme_name not in THEMES: 
            return (1, f"[ERROR] Theme '{theme_name}' not found")
        return (0, THEMES[theme_name]['banner'])
    
    elif subcmd == 'clock':
        now = datetime.now().strftime("%H:%M:%S")
        return (0, f"\n+------------------+\n| TIME: {now}  |\n+------------------+\n")
    
    elif subcmd == 'matrix':
        return (0, """
+--------------------+
| 0 1 0 1 1 0 1 0   |
| 1 0 1 0 0 1 0 1   |
| 0 1 0 1 1 0 1 0   |
| 1 0 1 0 0 1 0 1   |
+--------------------+
        """)
    
    return (1, f"[ERROR] Unknown subcommand 'ascii {subcmd}'")


def cmd_banner(args: List[str], shell) -> Tuple[int, str]:
    """Display banner"""
    return cmd_ascii(['banner'] + args, shell)


def cmd_map(args: List[str], shell) -> Tuple[int, str]:
    """Toggle system map"""
    if not args: 
        status = "ON" if shell.system_map_enabled else "OFF"
        return (0, f"[STATUS] System map: {status}")
    
    mode = args[0]. lower()
    
    if mode == 'on': 
        shell.system_map_enabled = True
        return (0, "[OK] System map:  ON")
    elif mode == 'off':
        shell.system_map_enabled = False
        return (0, "[OK] System map: OFF")
    elif mode == 'once':
        if shell.pipe_chain:
            return (0, shell._visualize_pipe_chain())
        return (0, "[INFO] No pipe chain to visualize")
    
    return (1, "[ERROR] Usage: map on | map off | map once")


COMMANDS = {
    'theme': cmd_theme,
    'ascii': cmd_ascii,
    'banner': cmd_banner,
    'map': cmd_map,
}