# -*- coding: utf-8 -*-
"""
Test plugin showing how to extend nextgen-bash
"""


def initialize(shell):
    """Initialize plugin
    
    Called when shell loads plugin
    """
    print("✅ Test plugin loaded")
    
    # You can add commands, hooks, etc here
    # Example: shell.commands['custom'] = my_function


def on_command_execute(shell, cmd_str):
    """Hook:  before command execution"""
    pass


def on_command_complete(shell, cmd_str, code, output):
    """Hook: after command execution"""
    pass


def on_exit(shell):
    """Hook: on shell exit"""
    print("📝 Test plugin unloaded")