# -*- coding: utf-8 -*-
"""
Language management
"""

from typing import List, Tuple


def cmd_lang_list(args: List[str], shell) -> Tuple[int, str]:
    """List all available languages"""
    langs = shell.i18n.get_available_languages()
    
    output = "\n[LANGUAGES] Available:\n"
    output += "=" * 60 + "\n"
    for code, name in langs.items():
        current = " <- CURRENT" if code == shell.i18n.language else ""
        output += f"  {code: 5s} :  {name: 20s}{current}\n"
    
    return (0, output)


def cmd_lang_set(args: List[str], shell) -> Tuple[int, str]:
    """Set language"""
    if not args: 
        return (1, "[ERROR] lang set:  missing language code\nUsage: lang set <code>\nExample: lang set ru")
    
    lang_code = args[0]
    
    if shell.i18n.set_language(lang_code):
        lang_name = shell.i18n.get_available_languages().get(lang_code, lang_code)
        return (0, f"[OK] Language changed to {lang_name}\n[INFO] Run 'help' to see commands in new language")
    else:
        return (1, f"[ERROR] Language '{lang_code}' not found\n[INFO] Use 'lang list' to see available languages")


def cmd_lang_current(args: List[str], shell) -> Tuple[int, str]:
    """Show current language"""
    current_lang = shell.i18n. language
    langs = shell.i18n.get_available_languages()
    lang_name = langs.get(current_lang, current_lang)
    
    return (0, f"[STATUS] Current language: {current_lang} ({lang_name})")


def cmd_lang(args: List[str], shell) -> Tuple[int, str]: 
    """Language management (entry point)"""
    if not args:
        return cmd_lang_list(args, shell)
    
    subcmd = args[0]
    remaining_args = args[1:]
    
    if subcmd == 'list':
        return cmd_lang_list(remaining_args, shell)
    elif subcmd == 'set':
        return cmd_lang_set(remaining_args, shell)
    elif subcmd == 'current':
        return cmd_lang_current(remaining_args, shell)
    else:
        return (1, f"[ERROR] Unknown subcommand 'lang {subcmd}'\n[INFO] Use:  lang list, lang set <code>, lang current")


COMMANDS = {
    'lang':  cmd_lang,
}