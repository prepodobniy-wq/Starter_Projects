# -*- coding: utf-8 -*-
"""
Session and history management
"""

from typing import List, Tuple
from collections import Counter
import time


def cmd_session(args: List[str], shell) -> Tuple[int, str]:
    """Manage sessions"""
    if not args: 
        return (1, "[ERROR] session: missing subcommand (save, load, reset)")
    
    subcmd = args[0]
    filename = args[1] if len(args) > 1 else "session.json"
    
    if subcmd == 'save':
        return shell.save_session(filename)
    elif subcmd == 'load':
        return shell.load_session(filename)
    elif subcmd == 'reset':
        shell.history. clear()
        shell.history_index = -1
        return (0, f"[OK] Session reset")
    else:
        return (1, f"[ERROR] session: unknown subcommand '{subcmd}'")


def cmd_history(args: List[str], shell) -> Tuple[int, str]: 
    """Show command history"""
    limit = int(args[0]) if args else 20
    
    if not shell. history:
        return (0, "[INFO] No command history")
    
    output = f"\n[HISTORY] Last {limit} commands\n"
    output += "=" * 60 + "\n"
    for i, cmd in enumerate(shell. history[-limit:], len(shell.history) - limit + 1):
        output += f"  {i: 3d}. {cmd}\n"
    
    return (0, output)


def cmd_stats(args: List[str], shell) -> Tuple[int, str]:
    """Show usage statistics"""
    if not shell.history:
        return (0, "[INFO] No statistics available")
    
    commands_used = [cmd. split()[0] for cmd in shell. history if cmd.split()]
    top_commands = Counter(commands_used).most_common(5)
    
    output = f"\n[STATS]\n"
    output += "=" * 60 + "\n"
    output += f"Total commands: {len(shell.history)}\n"
    output += f"Unique commands: {len(set(commands_used))}\n"
    output += f"\nTop 5 commands:\n"
    
    for cmd, count in top_commands:
        output += f"  {cmd}: {count} times\n"
    
    return (0, output)


def cmd_profile(args: List[str], shell) -> Tuple[int, str]:
    """Profile command performance"""
    if not args: 
        return (1, "[ERROR] profile: missing command")
    
    cmd_str = ' '.join(args)
    
    start = time.time()
    code, output = shell.execute(cmd_str)
    elapsed = time.time() - start
    
    output_msg = f"\n[PROFILE]\n"
    output_msg += "=" * 60 + "\n"
    output_msg += f"Command: {cmd_str}\n"
    output_msg += f"Time: {elapsed:.4f}s\n"
    output_msg += f"Exit code: {code}\n"
    output_msg += f"Output size: {len(output)} chars\n"
    
    return (0, output_msg)


def cmd_timeline(args: List[str], shell) -> Tuple[int, str]:
    """Timeline visualization"""
    if not shell.history:
        return (0, "[INFO] No history")
    
    output = "\n[TIMELINE]\n"
    output += "=" * 60 + "\n"
    for i, cmd in enumerate(shell. history[-10:], 1):
        output += f"  {i}. {cmd}\n"
    
    return (0, output)


COMMANDS = {
    'session':  cmd_session,
    'history': cmd_history,
    'stats': cmd_stats,
    'profile': cmd_profile,
    'timeline': cmd_timeline,
}