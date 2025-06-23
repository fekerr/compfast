# src/renderer.py
"""
Provides the Renderer class for drawing simulation state.
"""
import pygame
import math
import sys

class Renderer:
    """Handles rendering of the simulation state to a target Pygame surface."""
    # Default value for planet color if not specified or invalid in config
    DEFAULT_PLANET_COLOR_HEX = "#FFFFFF" # White
    # Threshold for switching to log scaling for planet radii (when very zoomed out)
    LOG_SCALE_RADIUS_THRESHOLD = 1e-9 # Pixels per meter
    # Min/max display radii for planets
    MIN_PLANET_PIXEL_RADIUS = 2
    MAX_PLANET_PIXEL_RADIUS = 50
    # Min display radius for the Sun
    MIN_SUN_PIXEL_RADIUS = 2


    def __init__(self, config):
        # (Docstring from previous step assumed sufficient)
        self.config = config if config else {} # Ensure config is a dict

        planet_default_hex_cfg = self.config.get('display', {}).get('planet_default_color', self.DEFAULT_PLANET_COLOR_HEX)
        try:
            self.planet_default_color_rgb = pygame.Color(planet_default_hex_cfg)
        except ValueError:
            print(f"Warning: Invalid default planet hex color '{planet_default_hex_cfg}' in config. "
                  f"Defaulting to {self.DEFAULT_PLANET_COLOR_HEX}.", file=sys.stderr)
            self.planet_default_color_rgb = pygame.Color(self.DEFAULT_PLANET_COLOR_HEX)

    def world_to_screen(self, target_surface_dims, world_pos_m, view_center_world_m, scale_pixels_per_m, is_top_down=True):
        # (Docstring from previous step assumed sufficient, logic unchanged)
        surface_width, surface_height = target_surface_dims
        relative_pos_m_x = world_pos_m[0] - view_center_world_m[0]
        if is_top_down: relative_pos_m_y = world_pos_m[1] - view_center_world_m[1]
        else: relative_pos_m_y = world_pos_m[2] - view_center_world_m[2]
        pixel_offset_x = relative_pos_m_x * scale_pixels_per_m
        pixel_offset_y = relative_pos_m_y * scale_pixels_per_m
        screen_x = int(surface_width / 2 + pixel_offset_x)
        screen_y = int(surface_height / 2 - pixel_offset_y)
        return screen_x, screen_y

    def draw_selection_indicator(self, target_surface, screen_coords, pixel_radius):
        # (Docstring from previous step assumed sufficient, logic unchanged)
        indicator_color = pygame.Color("yellow")
        pygame.draw.circle(target_surface, indicator_color, screen_coords, pixel_radius + 4, 2) # 2px thick border

    def _calculate_display_radius(self, body, scale_pixels_per_m):
        # (Docstring from previous step assumed sufficient)
        display_radius_m = body.radius * 1000 # km to m
        pixel_radius = display_radius_m * scale_pixels_per_m

        if body.name.lower() == "sun":
            # Sun can be larger and doesn't use the general planet max radius.
            pixel_radius = max(self.MIN_SUN_PIXEL_RADIUS, int(pixel_radius))
        else:
            scaled_planet_radius_km = body.radius # Original radius in km for log scaling reference
            if scale_pixels_per_m < self.LOG_SCALE_RADIUS_THRESHOLD and scaled_planet_radius_km > 0:
                 # Log scaling for visibility when zoomed out, ensures larger planets are still visibly distinct
                 pixel_radius = self.MIN_PLANET_PIXEL_RADIUS + int(math.log1p(scaled_planet_radius_km) / math.log1p(1.5)) # Tune log1p(1.5) for scaling rate
            elif scaled_planet_radius_km == 0 : # For point-like objects if radius is 0
                pixel_radius = self.MIN_PLANET_PIXEL_RADIUS
            else: # Zoomed in closer, or normal scale
                 pixel_radius = max(self.MIN_PLANET_PIXEL_RADIUS, int(pixel_radius))
            pixel_radius = min(pixel_radius, self.MAX_PLANET_PIXEL_RADIUS) # Apply max cap for planets

        return max(1, int(pixel_radius)) # Ensure radius is at least 1 pixel to be drawn

    def draw_body_on_surface(self, target_surface, body, view_center_world_m, scale_pixels_per_m):
        # (Docstring from previous step assumed sufficient)
        target_surface_dims = target_surface.get_size()
        screen_coords = self.world_to_screen(target_surface_dims, body.position, view_center_world_m, scale_pixels_per_m)
        actual_drawn_radius = self._calculate_display_radius(body, scale_pixels_per_m)

        if screen_coords: # Should always be true unless world_to_screen adds culling
            try: body_color_rgb = pygame.Color(body.color)
            except ValueError:
                print(f"Warning: Invalid color '{body.color}' for body '{body.name}'. Using default.", file=sys.stderr)
                body_color_rgb = self.planet_default_color_rgb

            pygame.draw.circle(target_surface, body_color_rgb, screen_coords, actual_drawn_radius)
        return screen_coords, actual_drawn_radius

    def render_all_bodies_to_surface(self, target_surface, bodies, view_center_world_m, scale_pixels_per_m,
                                     selected_body_name=None, show_paths=True):
        # (Docstring from previous step assumed sufficient)
        target_surface_dims = target_surface.get_size()
        if not bodies: return # Nothing to render

        for body in bodies:
            # --- Draw Orbital Path ---
            if show_paths and body.position_history and len(body.position_history) > 1:
                path_screen_points = []
                for hist_pos in body.position_history:
                    screen_point = self.world_to_screen(target_surface_dims, hist_pos, view_center_world_m, scale_pixels_per_m)
                    path_screen_points.append(screen_point)

                if len(path_screen_points) > 1:
                    try: path_color = pygame.Color(body.color) # Use body color for its path
                    except ValueError: path_color = self.planet_default_color_rgb
                    pygame.draw.lines(target_surface, path_color, False, path_screen_points, 1) # 1px thick path

            # --- Draw Body ---
            screen_coords, actual_drawn_radius = self.draw_body_on_surface(
                target_surface, body, view_center_world_m, scale_pixels_per_m
            )

            # --- Draw Selection Indicator ---
            if selected_body_name and body.name == selected_body_name and screen_coords:
                self.draw_selection_indicator(target_surface, screen_coords, actual_drawn_radius)
