# -*- coding: utf-8 -*-
"""
🌍 Internationalization (i18n) module
Support:  English, Russian, Spanish, French, German, Chinese, Japanese
"""

from typing import Dict, Optional

TRANSLATIONS = {
    'en': {
        'welcome': '🚀 Welcome to nextgen-bash!  Type "help" for commands.',
        'goodbye': '👋 Goodbye!  Your session has been saved.',
        'error': 'Error',
        'command_not_found': 'command not found',
        'permission_denied': 'Permission denied',
        'no_file': 'No such file or directory',
        'invalid_syntax': 'Invalid syntax',
        'session_saved': 'Session saved successfully! ',
        'session_loaded': 'Session loaded! ',
        'session_reset': 'Session reset.',
        'sandbox_enabled': 'Sandbox mode:  ON 🔒',
        'sandbox_disabled':  'Sandbox mode: OFF 🔓',
        'theme_changed': 'Theme changed to',
        'help_text': '📚 nextgen-bash:  Next generation bash console\nUsage: command [args]\nType "help" for all commands.',
    },
    'ru': {
        'welcome': '🚀 Добро пожаловать в nextgen-bash!  Напишите "help" для списка команд.',
        'goodbye': '👋 До свидания! Ваша сессия сохранена.',
        'error': 'Ошибка',
        'command_not_found':  'команда не найдена',
        'permission_denied': 'Доступ запрещён',
        'no_file':  'Файл или каталог не найдены',
        'invalid_syntax': 'Неверный синтаксис',
        'session_saved': 'Сессия успешно сохранена!',
        'session_loaded': 'Сессия загружена!',
        'session_reset': 'Сессия очищена.',
        'sandbox_enabled': 'Режим sandbox: ВКЛ 🔒',
        'sandbox_disabled': 'Режим sandbox: ВЫКЛ 🔓',
        'theme_changed': 'Тема изменена на',
        'help_text': '📚 nextgen-bash: Консоль bash нового поколения\nИспользование: команда [аргументы]\nНапишите "help" для списка команд.',
    },
    'es': {
        'welcome':  '🚀 ¡Bienvenido a nextgen-bash! Escribe "help" para ver los comandos.',
        'goodbye': '👋 ¡Adiós! Tu sesión ha sido guardada.',
        'error':  'Error',
        'command_not_found': 'comando no encontrado',
        'permission_denied': 'Permiso denegado',
        'no_file': 'Archivo o directorio no encontrado',
        'invalid_syntax': 'Sintaxis inválida',
        'session_saved': '¡Sesión guardada exitosamente!',
        'session_loaded': '¡Sesión cargada!',
        'session_reset': 'Sesión reiniciada.',
        'sandbox_enabled': 'Modo sandbox:  ACTIVADO 🔒',
        'sandbox_disabled': 'Modo sandbox: DESACTIVADO 🔓',
        'theme_changed': 'Tema cambiado a',
        'help_text': '📚 nextgen-bash: Consola bash de próxima generación\nUso: comando [argumentos]\nEscribe "help" para ver los comandos.',
    },
    'fr': {
        'welcome': '🚀 Bienvenue dans nextgen-bash!  Tapez "help" pour les commandes.',
        'goodbye':  '👋 Au revoir! Votre session a été sauvegardée.',
        'error': 'Erreur',
        'command_not_found': 'commande non trouvée',
        'permission_denied': 'Permission refusée',
        'no_file': 'Fichier ou répertoire non trouvé',
        'invalid_syntax': 'Syntaxe invalide',
        'session_saved': 'Session sauvegardée avec succès!',
        'session_loaded': 'Session chargée!',
        'session_reset': 'Session réinitialisée.',
        'sandbox_enabled': 'Mode sandbox:  ACTIVÉ 🔒',
        'sandbox_disabled': 'Mode sandbox: DÉSACTIVÉ 🔓',
        'theme_changed': 'Thème changé en',
        'help_text':  '📚 nextgen-bash: Console bash de nouvelle génération\nUtilisation:  commande [arguments]\nTapez "help" pour les commandes.',
    },
    'de': {
        'welcome': '🚀 Willkommen bei nextgen-bash! Geben Sie "help" für Befehle ein.',
        'goodbye': '👋 Auf Wiedersehen! Ihre Sitzung wurde gespeichert.',
        'error': 'Fehler',
        'command_not_found': 'Befehl nicht gefunden',
        'permission_denied': 'Zugriff verweigert',
        'no_file': 'Datei oder Verzeichnis nicht gefunden',
        'invalid_syntax':  'Ungültige Syntax',
        'session_saved':  'Sitzung erfolgreich gespeichert!',
        'session_loaded': 'Sitzung geladen! ',
        'session_reset':  'Sitzung zurückgesetzt.',
        'sandbox_enabled': 'Sandbox-Modus: AKTIVIERT 🔒',
        'sandbox_disabled': 'Sandbox-Modus: DEAKTIVIERT 🔓',
        'theme_changed': 'Design geändert in',
        'help_text':  '📚 nextgen-bash: Bash-Konsole der nächsten Generation\nVerwendung:  Befehl [Argumente]\nGeben Sie "help" für Befehle ein.',
    },
    'zh': {
        'welcome': '🚀 欢迎来到 nextgen-bash！输入 "help" 查看命令。',
        'goodbye': '👋 再见！您的会话已保存。',
        'error': '错误',
        'command_not_found': '命令未找到',
        'permission_denied': '权限被拒绝',
        'no_file': '文件或目录不存在',
        'invalid_syntax': '语法无效',
        'session_saved': '会话已成功保存！',
        'session_loaded': '会话已加载！',
        'session_reset': '会话已重置。',
        'sandbox_enabled': '沙箱模式：打开 🔒',
        'sandbox_disabled': '沙箱模式：关闭 🔓',
        'theme_changed': '主题已更改为',
        'help_text': '📚 nextgen-bash:  新一代 bash 控制台\n用法:  命令 [参数]\n输入 "help" 查看命令。',
    },
    'ja': {
        'welcome': '🚀 nextgen-bash へようこそ！コマンドを表示するには "help" と入力してく��さい。',
        'goodbye': '👋 さようなら！セッションが保存されました。',
        'error': 'エラー',
        'command_not_found': 'コマンドが見つかりません',
        'permission_denied': 'アクセス権限がありません',
        'no_file':  'ファイルまたはディレクトリが見つかりません',
        'invalid_syntax': '構文が無効です',
        'session_saved': 'セッションが正常に保存されました！',
        'session_loaded': 'セッションが読み込まれました！',
        'session_reset': 'セッションがリセットされました。',
        'sandbox_enabled': 'サンドボックスモード: ON 🔒',
        'sandbox_disabled': 'サンドボックスモード: OFF 🔓',
        'theme_changed': 'テーマが変更されました',
        'help_text': '📚 nextgen-bash:  次世代 bash コンソール\n使用法: コマンド [引数]\n"help" でコマンドを表示します。',
    }
}


class I18n:
    """Internationalization manager"""
    
    def __init__(self, language: str = 'en'):
        """Initialize with language code"""
        self.language = language if language in TRANSLATIONS else 'en'
        self.translations = TRANSLATIONS[self.language]
    
    def t(self, key: str, **kwargs) -> str:
        """Translate key to current language"""
        text = self.translations.get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text
    
    def set_language(self, language: str) -> bool:
        """Change language at runtime"""
        if language in TRANSLATIONS:
            self.language = language
            self.translations = TRANSLATIONS[language]
            return True
        return False
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get all available languages"""
        return {
            'en': 'English',
            'ru':  'Русский',
            'es':  'Español',
            'fr': 'Français',
            'de': 'Deutsch',
            'zh': '中文',
            'ja': '日本語',
        }