# -*- coding: utf-8 -*-
"""
File operations - open and create files from console
"""

from typing import List, Tuple
from pathlib import Path


def cmd_open(args: List[str], shell) -> Tuple[int, str]:
    """Open and display file (similar to cat)"""
    if not args:
        return (1, "[ERROR] open: missing filename\nUsage: open <filename>")
    
    filename = args[0]
    
    try:
        file_path = Path(filename)
        if not file_path.is_absolute():
            file_path = shell.cwd / file_path
        
        if not file_path.exists():
            return (1, f"[ERROR] File not found: {filename}")
        
        if not file_path.is_file():
            return (1, f"[ERROR] Not a file: {filename}")
        
        content = file_path.read_text()
        output = f"\n[FILE] {file_path.name}\n"
        output += "=" * 80 + "\n"
        output += content
        output += "\n" + "=" * 80 + "\n"
        
        return (0, output)
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_create(args: List[str], shell) -> Tuple[int, str]: 
    """Create a new file with content from console"""
    if not args: 
        return (1, "[ERROR] create: missing filename\nUsage: create <filename>")
    
    filename = args[0]
    
    try: 
        file_path = Path(filename)
        if not file_path.is_absolute():
            file_path = shell.cwd / file_path
        
        if file_path.exists():
            return (1, f"[ERROR] File already exists: {filename}\n[INFO] Use 'rm {filename}' to delete first")
        
        # Get content from remaining args or ask user
        if len(args) > 1:
            content = ' '.join(args[1:])
        else:
            content = ""
        
        file_path. write_text(content)
        
        return (0, f"[OK] Created file: {filename}\n[INFO] Path: {file_path}")
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_edit(args: List[str], shell) -> Tuple[int, str]:
    """Edit file (show content and instructions)"""
    if not args: 
        return (1, "[ERROR] edit: missing filename\nUsage: edit <filename>")
    
    filename = args[0]
    
    try: 
        file_path = Path(filename)
        if not file_path.is_absolute():
            file_path = shell.cwd / file_path
        
        if not file_path.exists():
            return (1, f"[ERROR] File not found: {filename}")
        
        content = file_path.read_text()
        
        output = f"\n[EDIT] {file_path.name}\n"
        output += "=" * 80 + "\n"
        output += content
        output += "\n" + "=" * 80 + "\n"
        output += "[INFO] Use 'Create File' button in GUI to edit and save\n"
        
        return (0, output)
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_ls_long(args: List[str], shell) -> Tuple[int, str]:
    """List files with details (ls -la style)"""
    path = args[0] if args else '.'
    
    try:
        p = Path(path)
        if not p.exists():
            return (1, f"[ERROR] Not found: {path}")
        
        if not p.is_dir():
            return (0, f"[FILE] {p.name}")
        
        output = f"\n[DIRECTORY] {p}\n"
        output += "=" * 80 + "\n"
        output += f"{'NAME':<40} {'TYPE':<10} {'SIZE': <15}\n"
        output += "-" * 80 + "\n"
        
        try:
            items = sorted(p.iterdir())
        except PermissionError:
            return (1, f"[ERROR] Permission denied: {path}")
        
        for item in items:
            if item.is_dir():
                type_str = "[DIR]"
                size_str = "-"
            else:
                type_str = "[FILE]"
                size_str = f"{item. stat().st_size} bytes"
            
            name = item.name
            if len(name) > 35:
                name = name[:32] + "..."
            
            output += f"{name:<40} {type_str:<10} {size_str: <15}\n"
        
        return (0, output)
    except Exception as e:
        return (1, f"[ERROR] {e}")


COMMANDS = {
    'open':  cmd_open,
    'create': cmd_create,
    'edit': cmd_edit,
    'ls-la': cmd_ls_long,
}