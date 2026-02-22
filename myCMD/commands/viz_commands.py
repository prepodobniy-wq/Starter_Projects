# -*- coding: utf-8 -*-
"""
Data visualization commands
"""

from pathlib import Path
from typing import List, Tuple


def cmd_tree_plus(args: List[str], shell) -> Tuple[int, str]:
    """Display directory tree"""
    path = Path(args[0]) if args else shell.cwd
    max_depth = int(args[1]) if len(args) > 1 else 3
    
    def tree_render(directory, prefix="", depth=0):
        if depth >= max_depth:
            return ""
        
        output = ""
        try:
            items = sorted(list(directory.iterdir()))
        except: 
            return output
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "L-- " if is_last else "|-- "
            dir_marker = "[D] " if item.is_dir() else "[F] "
            output += f"{prefix}{current_prefix}{dir_marker}{item.name}\n"
            
            if item.is_dir() and depth < max_depth - 1:
                next_prefix = prefix + ("    " if is_last else "|   ")
                output += tree_render(item, next_prefix, depth + 1)
        
        return output
    
    try:
        return (0, f"[TREE] {path}/\n" + tree_render(path))
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_ls_plus(args: List[str], shell) -> Tuple[int, str]:
    """ls with symbols"""
    path = Path(args[0]) if args else shell.cwd
    
    try:
        items = sorted(list(path.iterdir()))
        output = "[LS+]\n"
        for item in items:
            marker = "[D]" if item.is_dir() else "[F]"
            output += f"  {marker} {item.name}\n"
        
        return (0, output if output != "[LS+]\n" else "[LS+] (empty)")
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_cat_plus(args: List[str], shell) -> Tuple[int, str]:
    """cat with formatting"""
    if not args:
        return (1, "[ERROR] cat+: missing filename")
    
    try:
        content = Path(args[0]).read_text()
        
        lines = []
        for i, line in enumerate(content.split('\n'), 1):
            if line.strip().startswith('#'):
                line = f"[COMMENT] {line}"
            elif line.strip().startswith('def '):
                line = f"[FUNC] {line}"
            lines.append(f"{i:4d}: {line}")
        
        return (0, '\n'.join(lines))
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_preview(args: List[str], shell) -> Tuple[int, str]:
    """Preview file"""
    if not args:
        return (1, "[ERROR] preview:  missing filename")
    
    try:
        content = Path(args[0]).read_text()
        lines = content.split('\n')[:20]
        
        output = f"[PREVIEW] {args[0]}\n"
        output += "=" * 60 + "\n"
        
        if len(content. split('\n')) > 20:
            more = len(content.split('\n')) - 20
            lines.append(f"\n...  ({more} more lines)")
        
        output += '\n'.join(lines)
        return (0, output)
    except Exception as e:
        return (1, f"[ERROR] {e}")


def cmd_pipeviz(args: List[str], shell) -> Tuple[int, str]:
    """Visualize pipe chain"""
    if not shell.pipe_chain:
        return (0, "[INFO] No pipe chain to visualize")
    
    return (0, shell._visualize_pipe_chain())


def cmd_dna(args: List[str], shell) -> Tuple[int, str]:
    """Show command structure"""
    if not shell.last_command:
        return (0, "[INFO] No command to analyze")
    
    cmd = shell.last_command
    tokens = shell. parse_command(cmd)
    
    output = f"\n[DNA] Command: {cmd}\n"
    output += "Tokens:\n"
    for i, token in enumerate(tokens, 1):
        output += f"  {i}. {token}\n"
    
    return (0, output)


def cmd_fsmap(args: List[str], shell) -> Tuple[int, str]:
    """Watch filesystem"""
    if not args:
        return (1, "[ERROR] fsmap: missing subcommand (watch, scan)")
    
    if args[0] == 'watch':
        path = shell.cwd
        
        def show_tree(directory, prefix="", max_depth=2, depth=0):
            if depth >= max_depth:
                return ""
            
            output = ""
            try:
                items = sorted(list(directory.iterdir()))[: 10]
            except:
                return output
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                marker = "[D]" if item. is_dir() else "[F]"
                output += f"{prefix}{'L-- ' if is_last else '|-- '}{marker} {item. name}\n"
                
                if item.is_dir() and depth < max_depth - 1:
                    next_prefix = prefix + ("    " if is_last else "|   ")
                    output += show_tree(item, next_prefix, max_depth, depth + 1)
            
            return output
        
        return (0, f"\n[FSMAP] {path}\n" + show_tree(path))
    
    return (1, f"[ERROR] fsmap: unknown subcommand '{args[0]}'")


def cmd_timeflow(args: List[str], shell) -> Tuple[int, str]:
    """Timeline of commands"""
    if not shell.history:
        return (0, "[INFO] No command history")
    
    output = "\n[TIMELINE]\n"
    output += "=" * 60 + "\n"
    for i, cmd in enumerate(shell.history[-10:], 1):
        output += f"  {i}. {cmd}\n"
    
    return (0, output)


def cmd_simulate(args: List[str], shell) -> Tuple[int, str]:
    """Simulate command execution"""
    if not args: 
        return (1, "[ERROR] simulate: missing command")
    
    cmd_str = ' '.join(args)
    
    output = f"\n[SIMULATE] {cmd_str}\n"
    output += "Step 1: Parse command\n"
    output += "Step 2: Check sandbox\n"
    output += "Step 3: Execute\n"
    output += "Step 4: Return result\n"
    
    return (0, output)


COMMANDS = {
    'tree+': cmd_tree_plus,
    'ls+': cmd_ls_plus,
    'cat+': cmd_cat_plus,
    'preview': cmd_preview,
    'pipeviz': cmd_pipeviz,
    'dna': cmd_dna,
    'fsmap': cmd_fsmap,
    'timeflow': cmd_timeflow,
    'simulate': cmd_simulate,
}