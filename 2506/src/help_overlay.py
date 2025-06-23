# src/help_overlay.py
"""
Provides the HelpOverlay class for displaying a pop-up help screen.
"""
import pygame
import sys

class HelpOverlay:
    """Manages and renders a pop-up help screen overlay with formatted text."""
    DEFAULT_FONT_SIZE = 20
    DEFAULT_BG_COLOR = (30, 30, 50, 230) # Dark blue-gray, semi-transparent (RGBA)
    DEFAULT_TEXT_COLOR = (220, 220, 220)
    DEFAULT_BORDER_COLOR = (100, 100, 120)
    BORDER_WIDTH = 2
    PADDING = 20

    def __init__(self, screen_width, screen_height, font_size=DEFAULT_FONT_SIZE,
                 bg_color=DEFAULT_BG_COLOR, text_color=DEFAULT_TEXT_COLOR,
                 border_color=DEFAULT_BORDER_COLOR, font_name=None):
        # (Docstring from previous step)
        self.overlay_width = int(screen_width * 0.8); self.overlay_height = int(screen_height * 0.8)
        self.overlay_x = (screen_width - self.overlay_width)//2; self.overlay_y = (screen_height - self.overlay_height)//2
        self.rect = pygame.Rect(self.overlay_x, self.overlay_y, self.overlay_width, self.overlay_height)
        self.surface = pygame.Surface((self.overlay_width, self.overlay_height), pygame.SRCALPHA)
        self.bg_color = bg_color; self.text_color = text_color; self.border_color = border_color
        self.font_regular, self.font_bold = None, None # Initialize

        try:
            self.font_regular = pygame.font.SysFont(font_name, font_size)
            self.font_bold = pygame.font.SysFont(font_name, font_size + 2, bold=True)
        except Exception as e_sysfont:
            print(f"Warning: HelpOverlay SysFont('{font_name}', {font_size}) failed: {e_sysfont}. Using Pygame default.", file=sys.stderr)
            try:
                self.font_regular = pygame.font.Font(None, font_size)
                self.font_bold = pygame.font.Font(None, font_size + 2)
                if self.font_bold: self.font_bold.set_bold(True) # Attempt to set bold for default
            except Exception as e_defaultfont:
                print(f"CRITICAL ERROR: HelpOverlay Pygame default font also failed: {e_defaultfont}. Help text may not render.", file=sys.stderr)

        self.line_spacing = font_size // 2; self.is_active = False; self.help_content = []

    def set_content(self, content_list_of_tuples): self.help_content = content_list_of_tuples
    def toggle_visibility(self): self.is_active = not self.is_active; return self.is_active

    def _wrap_text(self, text, font, max_width): # Unchanged from previous refactor
        words=text.split(' '); lines=[]; current_line=""
        for word in words:
            if not font: lines.append(word); continue # Should not happen if __init__ is fine
            if not current_line: current_line=word
            else: test_line=current_line+" "+word
                  if font.size(test_line)[0]<=max_width: current_line=test_line
                  else: lines.append(current_line); current_line=word
        lines.append(current_line); return lines

    def draw(self, target_main_surface):
        if not self.is_active or not self.font_regular: return # Do nothing if inactive or font failed
        self.surface.fill(self.bg_color); pygame.draw.rect(self.surface,self.border_color,self.surface.get_rect(),self.BORDER_WIDTH)
        current_y=self.PADDING; max_text_width=self.overlay_width-(2*self.PADDING)
        for text_item,is_heading in self.help_content:
            font_to_use=self.font_bold if is_heading and self.font_bold else self.font_regular # Fallback to regular if bold failed
            if not font_to_use: continue # Skip if even regular font is missing
            wrapped_lines=self._wrap_text(text_item,font_to_use,max_text_width)
            for line_text in wrapped_lines:
                if current_y+font_to_use.get_linesize()>self.overlay_height-self.PADDING: target_main_surface.blit(self.surface,self.rect); return
                try: text_render_surface=font_to_use.render(line_text,True,self.text_color); self.surface.blit(text_render_surface,(self.PADDING,current_y)); current_y+=font_to_use.get_linesize()
                except Exception as e:
                    error_message = f"ERR! Help Line Failed."[:50]
                    try: error_surface=self.font_regular.render(error_message,True,(255,0,0)); self.surface.blit(error_surface,(self.PADDING,current_y)); current_y+=self.font_regular.get_linesize()
                    except: pass
            if is_heading: current_y+=self.line_spacing//2
            current_y+=self.line_spacing
        target_main_surface.blit(self.surface,self.rect)
