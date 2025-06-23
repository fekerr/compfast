# tests/test_text_display.py
"""
Unit tests for the TextDisplay class.
"""
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Conditional import for pygame for testing environment
try:
    import pygame
    pygame_available = True
except ImportError:
    pygame_available = False
    # Mock Pygame if not available (e.g. in CI without display)
    pygame = MagicMock()
    pygame.font.SysFont = MagicMock(return_value=MagicMock(get_linesize=lambda: 15, render=MagicMock()))
    pygame.font.Font = MagicMock(return_value=MagicMock(get_linesize=lambda: 15, render=MagicMock()))
    pygame.Color = MagicMock(return_value=(0,0,0))


from text_display import TextDisplay # Now import after potential pygame mock

@unittest.skipIf(not pygame_available, "Pygame not available, skipping TextDisplay tests that rely on it.")
class TestTextDisplay(unittest.TestCase):
    """Test suite for the TextDisplay class."""

    def setUp(self):
        """Initialize pygame.font if it hasn't been, for font-dependent tests."""
        if pygame_available and not pygame.font.get_init():
            pygame.font.init() # Ensures font module is ready
        self.font_size = 18
        self.line_spacing = 2
        # Mock font for consistent line height if needed, or use actual font if Pygame init works
        self.mock_font_instance = MagicMock()
        self.mock_font_instance.get_linesize.return_value = self.font_size # Approx line height
        self.mock_font_instance.render.return_value = MagicMock() # Dummy surface

    @patch('pygame.font.SysFont') # Mock SysFont
    @patch('pygame.font.Font')    # Mock Font (fallback)
    def test_initialization(self, MockPygameFont, MockPygameSysFont):
        """Test TextDisplay initialization."""
        MockPygameSysFont.return_value = self.mock_font_instance
        MockPygameFont.return_value = self.mock_font_instance # For fallback path

        td = TextDisplay(font_size=self.font_size, line_spacing=self.line_spacing)
        self.assertEqual(td.max_lines, TextDisplay.DEFAULT_MAX_LINES)
        self.assertIsNotNone(td.font)
        self.assertEqual(td.line_height, self.font_size + self.line_spacing)
        self.assertEqual(td.font_color, TextDisplay.DEFAULT_FONT_COLOR)

    @patch('pygame.font.SysFont')
    @patch('pygame.font.Font')
    def test_initialization_font_fallback(self, MockPygameFont, MockPygameSysFont):
        """Test font fallback mechanism during initialization."""
        MockPygameSysFont.side_effect = Exception("SysFont failed") # Simulate SysFont failure
        MockPygameFont.return_value = self.mock_font_instance     # Fallback should use this

        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            td = TextDisplay(font_size=self.font_size)
            self.assertIn("Warning: Font 'None' with size 18 not found or error: SysFont failed. Using Pygame default.", mock_stderr.getvalue())
            self.assertIsNotNone(td.font) # Should have fallen back to pygame.font.Font
            MockPygameFont.assert_called_once_with(None, self.font_size)

    @patch('pygame.font.SysFont') # Mock to control font object
    def test_add_line(self, MockPygameSysFont):
        """Test adding lines and max_lines enforcement."""
        MockPygameSysFont.return_value = self.mock_font_instance
        td = TextDisplay(max_lines=3, font_size=self.font_size)

        td.add_line("Line 1")
        self.assertEqual(td.lines, ["Line 1"])
        td.add_line("Line 2")
        self.assertEqual(td.lines, ["Line 1", "Line 2"])
        td.add_line("Line 3")
        self.assertEqual(td.lines, ["Line 1", "Line 2", "Line 3"])
        td.add_line("Line 4 (pushes out Line 1)")
        self.assertEqual(td.lines, ["Line 2", "Line 3", "Line 4 (pushes out Line 1)"])
        self.assertEqual(len(td.lines), 3)

    @patch('pygame.font.SysFont')
    def test_render_to_surface(self, MockPygameSysFont):
        """Test rendering lines to a mock surface."""
        mock_font = MagicMock()
        mock_font.get_linesize.return_value = 20 # line_height will be 20 + spacing
        mock_font.render.return_value = MagicMock() # Dummy surface for rendered text
        MockPygameSysFont.return_value = mock_font

        td = TextDisplay(max_lines=5, font_size=18, line_spacing=2) # line_height = 20+2=22
        td.add_line("Test Line 1")
        td.add_line("Test Line 2")

        mock_surface = MagicMock()
        mock_surface.get_height.return_value = 100 # Allows approx 100/22 = 4 lines
        mock_surface.get_width.return_value = 200

        td.render_to_surface(mock_surface)

        # Verify font.render and surface.blit were called for each visible line
        self.assertEqual(mock_font.render.call_count, 2) # Two lines added
        mock_font.render.assert_any_call("Test Line 1", True, td.font_color)
        mock_font.render.assert_any_call("Test Line 2", True, td.font_color)

        self.assertEqual(mock_surface.blit.call_count, 2)
        # Check y positions (approximate, depends on line_spacing and TEXT_PADDING_X)
        expected_y1 = td.line_spacing
        expected_y2 = td.line_spacing + td.line_height
        mock_surface.blit.assert_any_call(mock_font.render.return_value, (td.TEXT_PADDING_X, expected_y1))
        mock_surface.blit.assert_any_call(mock_font.render.return_value, (td.TEXT_PADDING_X, expected_y2))

    @patch('pygame.font.SysFont')
    def test_render_to_surface_respects_max_visible_lines(self, MockPygameSysFont):
        """Test that only lines that fit on the surface are rendered."""
        mock_font = MagicMock(); mock_font.get_linesize.return_value = 20; mock_font.render.return_value = MagicMock()
        MockPygameSysFont.return_value = mock_font

        td = TextDisplay(max_lines=10, font_size=18, line_spacing=2) # line_height = 22
        for i in range(10): td.add_line(f"Line {i}")

        mock_surface = MagicMock()
        mock_surface.get_height.return_value = 50 # Allows 50/22 = 2 lines

        td.render_to_surface(mock_surface)

        # Only the last 2 lines should be rendered ("Line 8", "Line 9")
        self.assertEqual(mock_font.render.call_count, 2)
        mock_font.render.assert_any_call("Line 8", True, td.font_color)
        mock_font.render.assert_any_call("Line 9", True, td.font_color)
        self.assertEqual(mock_surface.blit.call_count, 2)

if __name__ == '__main__':
    # Initialize Pygame font module if running tests directly and Pygame is available
    if pygame_available:
        pygame.font.init()
    unittest.main()
