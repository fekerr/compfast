# src/text_display.py
"""
Provides the TextDisplay class for managing and rendering multiple lines of text
onto a Pygame surface, typically used for information panes or logs.
"""
import pygame
import sys

class TextDisplay:
    """
    Manages and renders a scrollable list of text lines for a designated pane.
    Handles font initialization, line management, and rendering to a target surface.
    """
    DEFAULT_MAX_LINES = 100
    DEFAULT_FONT_SIZE = 18
    DEFAULT_FONT_COLOR = (200, 200, 200) # Light gray
    DEFAULT_LINE_SPACING = 2
    TEXT_PADDING_X = 5 # Horizontal padding from the edge of the surface

    def __init__(self, max_lines=DEFAULT_MAX_LINES, font_size=DEFAULT_FONT_SIZE,
                 font_color=DEFAULT_FONT_COLOR, line_spacing=DEFAULT_LINE_SPACING,
                 font_name=None): # Allow specifying font name
        """
        Initializes the TextDisplay.

        Args:
            max_lines (int): Maximum number of lines to store.
            font_size (int): Font size.
            font_color (tuple[int,int,int]): RGB text color.
            line_spacing (int): Extra vertical spacing between lines.
            font_name (str, optional): Name of the system font. Pygame default if None.
        """
        self.lines = []
        self.max_lines = max_lines
        self.font_color = font_color
        self.line_spacing = line_spacing
        self.font = None # Initialize font to None

        try:
            self.font = pygame.font.SysFont(font_name, font_size)
        except Exception as e_sysfont: # Catch errors from SysFont
            print(f"Warning: TextDisplay SysFont('{font_name}', {font_size}) failed: {e_sysfont}. "
                  "Falling back to Pygame default font.", file=sys.stderr)
            try:
                self.font = pygame.font.Font(None, font_size) # Pygame's internal default font
            except Exception as e_defaultfont:
                print(f"CRITICAL ERROR: TextDisplay Pygame default font (size {font_size}) also failed: {e_defaultfont}. "
                      "Text will not render.", file=sys.stderr)
                # self.font remains None

        if self.font:
            self.line_height = self.font.get_linesize() + self.line_spacing
        else: # Fallback line height if no font could be loaded
            self.line_height = font_size + line_spacing # Estimate

    def add_line(self, text):
        """Adds a new line of text to the display history."""
        if not self.font: return # Cannot process text without a font

        self.lines.append(str(text))
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

    def render_to_surface(self, target_surface):
        """
        Renders the stored text lines onto the target_surface.
        Displays the most recent lines that fit, rendering from top-down.

        Args:
            target_surface (pygame.Surface): The Pygame surface to render text onto.
        """
        if not self.font: # Cannot render if font initialization failed
            # Optionally, draw an error message directly on the surface if possible
            # For now, console message from __init__ must suffice.
            return

        surface_height = target_surface.get_height()

        num_visible_lines_can_fit = surface_height // self.line_height if self.line_height > 0 else 0

        start_index = max(0, len(self.lines) - num_visible_lines_can_fit)
        visible_lines_to_render = self.lines[start_index:]

        current_y = self.line_spacing
        for text_line in visible_lines_to_render:
            if current_y + self.font.get_linesize() > surface_height:
                break
            try:
                text_surf = self.font.render(text_line, True, self.font_color)
                target_surface.blit(text_surf, (self.TEXT_PADDING_X, current_y))
            except Exception as e:
                error_message = f"ERR! Line: '{text_line[:30]}...': {e}"[:70] # Truncated
                try:
                    error_surf = self.font.render(error_message, True, (255, 50, 50))
                    target_surface.blit(error_surf, (self.TEXT_PADDING_X, current_y))
                except: pass # Give up if rendering the error message itself also fails
            current_y += self.line_height
