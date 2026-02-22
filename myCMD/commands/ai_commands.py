# -*- coding: utf-8 -*-
"""
AI-powered commands
"""

from typing import List, Tuple


EXPLANATIONS = {
    'en': {
        'ls': 'Lists files and directories in folder',
        'cd': 'Changes directory',
        'pwd':  'Shows current directory path',
        'grep': 'Searches for text patterns in files',
        'cat': 'Displays file contents',
        'echo': 'Prints text',
        'rm': 'Removes files (be careful!)',
        'mkdir': 'Creates directories',
        'find': 'Finds files matching pattern',
        'touch': 'Creates empty file',
        'head': 'Shows first lines',
        'tail': 'Shows last lines',
    },
    'ru': {
        'ls': 'Выводит содержимое каталога',
        'cd':  'Переходит в каталог',
        'pwd': 'Показывает текущий каталог',
        'grep': 'Ищет текст по шаблону',
        'cat': 'Выводит содержимое файла',
        'echo':  'Печатает текст',
        'rm': 'Удаляет файлы (осторожно!)',
        'mkdir': 'Создаёт каталоги',
        'find': 'Ищет файлы по шаблону',
        'touch': 'Создаёт пустой файл',
        'head': 'Показывает первые строки',
        'tail': 'Показывает последние строки',
    },
}


def cmd_ai_help(args: List[str], shell) -> Tuple[int, str]:
    """AI explanation of a command"""
    if not args:
        return (1, "[ERROR] ai help: missing command")
    
    cmd = args[0]
    lang = shell.i18n.language
    expl_dict = EXPLANATIONS. get(lang, EXPLANATIONS['en'])
    
    if cmd in expl_dict:
        return (0, f"[AI-HELP] {cmd}: {expl_dict[cmd]}")
    
    return (1, f"[ERROR] ai help: no explanation for '{cmd}'")


def cmd_ai_fix(args: List[str], shell) -> Tuple[int, str]:
    """AI fix for last error"""
    if not shell.last_error:
        return (0, "[OK] No errors to fix")
    
    error = shell.last_error. lower()
    
    if 'not found' in error:
        return (0, "[AI-FIX] Try:  ls, cd, grep, cat, echo")
    elif 'no such' in error:
        return (0, "[AI-FIX] Check file path or use 'ls' to see available files")
    elif 'permission' in error:
        return (0, "[AI-FIX] You may need different permissions or location")
    
    return (0, f"[AI-FIX] {shell.last_error}")


def cmd_ai_explain(args: List[str], shell) -> Tuple[int, str]:
    """Explain last command"""
    if not shell.last_command:
        return (0, "[INFO] No previous command")
    
    cmd = shell. last_command
    
    explanation = f"[AI-EXPLAIN] Command: {cmd}\n\n"
    
    if 'grep' in cmd:
        explanation += "This searches for text matching a pattern in files."
    elif 'cat' in cmd:
        explanation += "This displays the contents of files."
    elif 'ls' in cmd:
        explanation += "This lists files and directories."
    elif '|' in cmd:
        explanation += "This pipes output from one command to another (chains commands)."
    elif '&&' in cmd:
        explanation += "This runs the next command only if the previous one succeeds."
    elif '||' in cmd:
        explanation += "This runs the next command only if the previous one fails."
    else:
        explanation += "This performs operations on files and directories."
    
    return (0, explanation)


def cmd_ai_suggest(args: List[str], shell) -> Tuple[int, str]:
    """Optimization suggestions"""
    if not shell.last_command:
        return (0, "[INFO] No command to optimize")
    
    cmd = shell.last_command
    suggestions = "[AI-SUGGEST] Tips:\n"
    
    if 'grep' in cmd: 
        suggestions += "- Use -i for case-insensitive search\n"
        suggestions += "- Use -c to count matches\n"
    elif 'find' in cmd:
        suggestions += "- Limit depth with -maxdepth for speed\n"
    
    suggestions += "- Pipes speed up processing by chaining commands"
    
    return (0, suggestions)


def cmd_ai_bash(args: List[str], shell) -> Tuple[int, str]:
    """Translate English to bash"""
    if not args: 
        return (1, "[ERROR] ai bash: missing text")
    
    text = ' '.join(args).lower()
    
    translations = {
        'list files': 'ls',
        'show files': 'ls',
        'change directory': 'cd <dir>',
        'search': 'grep <pattern> <file>',
        'find':  'find <pattern>',
        'show file': 'cat <file>',
        'create file': 'touch <file>',
        'make directory': 'mkdir <dir>',
        'remove':  'rm <file>',
        'delete':  'rm <file>',
    }
    
    for key, value in translations.items():
        if key in text:
            return (0, f"[AI-BASH] {value}")
    
    return (1, f"[ERROR] Couldn't translate: {text}")


COMMANDS = {
    'ai':  cmd_ai_help,
}