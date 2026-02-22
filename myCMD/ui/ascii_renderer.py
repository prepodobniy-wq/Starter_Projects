# -*- coding: utf-8 -*-
"""
ASCII Renderer - Visual elements
"""

class ASCIIRenderer:
    """Renders ASCII elements"""
    
    @staticmethod
    def draw_box(title: str, content: str, width: int = 50) -> str:
        """Draw ASCII box"""
        output = f"╔{'═' * (width - 2)}╗\n"
        output += f"║ {title. center(width - 4)} ║\n"
        output += f"╠{'═' * (width - 2)}╣\n"
        
        for line in content.split('\n'):
            padded = line.ljust(width - 4)
            output += f"║ {padded} ║\n"
        
        output += f"╚{'═' * (width - 2)}╝\n"
        return output
    
    @staticmethod
    def draw_progressbar(progress: float, width: int = 30) -> str:
        """Draw ASCII progress bar"""
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}] {int(progress * 100)}%"
    
    @staticmethod
    def draw_table(headers: list, rows: list, col_widths: list = None) -> str:
        """Draw ASCII table"""
        output = ""
        
        if col_widths is None:
            col_widths = [15] * len(headers)
        
        # Header
        output += "┌" + "┬". join("─" * w for w in col_widths) + "┐\n"
        output += "│" + "│".join(h.center(w) for h, w in zip(headers, col_widths)) + "│\n"
        output += "├" + "┼".join("─" * w for w in col_widths) + "┤\n"
        
        # Rows
        for row in rows:
            output += "│" + "│".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)) + "│\n"
        
        output += "└" + "┴".join("─" * w for w in col_widths) + "┘\n"
        return output