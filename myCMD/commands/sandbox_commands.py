# -*- coding: utf-8 -*-
"""
Sandbox and safety commands
"""

from typing import List, Tuple


def cmd_sandbox(args: List[str], shell) -> Tuple[int, str]:
    """Toggle sandbox mode"""
    if not args:
        status = "ON" if shell.sandbox_enabled else "OFF"
        return (0, f"[STATUS] Sandbox:  {status}")
    
    mode = args[0]. lower()
    
    if mode == 'on':
        shell.sandbox_enabled = True
        return (0, f"[OK] Sandbox mode:  ON")
    elif mode == 'off':
        shell.sandbox_enabled = False
        return (0, f"[OK] Sandbox mode: OFF")
    else:
        return (1, "[ERROR] Use:  on or off")


def cmd_dryrun(args: List[str], shell) -> Tuple[int, str]:
    """Show what command would do"""
    if not args: 
        return (1, "[ERROR] dryrun: missing command")
    
    shell.dryrun_mode = True
    cmd_str = ' '.join(args)
    code, output = shell.execute(cmd_str)
    shell.dryrun_mode = False
    
    return (code, f"[DRYRUN]\n{output}")


def cmd_trace(args: List[str], shell) -> Tuple[int, str]:
    """Step-by-step execution"""
    if not args:
        return (1, "[ERROR] trace: missing command")
    
    shell.trace_mode = True
    cmd_str = ' '.join(args)
    code, output = shell.execute(cmd_str)
    shell.trace_mode = False
    
    return (code, f"[TRACE]\n{output}")


COMMANDS = {
    'sandbox':  cmd_sandbox,
    'dryrun': cmd_dryrun,
    'trace': cmd_trace,
}