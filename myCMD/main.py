"""
myCMD
"""
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.shell import ShellCore
from core.i18n import I18n
from ui.gui_window import GUITerminalWindow

# Doesn't matter which one, because it only in English
LANGUAGES = {
    '1': 'en',
    '2': 'ru',
    '3': 'es',
    '4': 'fr',
    '5': 'de',
    '6':  'zh',
    '7': 'ja',
}


def select_language_cli():
    """Language selection in console"""
    print("\n" + "="*60)
    print("SELECT LANGUAGE")
    print("="*60)
    print("""
    1. English
    2. Русский
    3. Español
    4. Français
    5. Deutsch
    6. 中文
    7. 日本語
    """)
    print("="*60)
    
    while True:  
        choice = input("Enter choice (1-7): ").strip()
        if choice in LANGUAGES:
            lang_code = LANGUAGES[choice]
            print(f"[OK] Language:  {lang_code}\n")
            return lang_code
        print("[ERROR] Invalid choice")


def main():
    """Main entry point"""
    try:
        language = select_language_cli()
        
        i18n = I18n(language)
        
        # Create directories
        for dir_name in ["commands", "plugins", "themes", "ui", "core", "ai", "sandbox"]:
            (PROJECT_ROOT / dir_name).mkdir(exist_ok=True)
        
        # Initialize shell
        shell = ShellCore(
            commands_path=PROJECT_ROOT / "commands",
            plugins_path=PROJECT_ROOT / "plugins",
            sandbox_enabled=True,
            i18n=i18n
        )
        
        # Launch GUI
        window = GUITerminalWindow(shell=shell, i18n=i18n)
        window.run()
        
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:  
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()