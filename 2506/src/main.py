# src/main.py
"""
Main application file for the Solar System Orbital Model.
Initializes Pygame, loads configuration, sets up UI panes,
handles user input, manages simulation, rendering, and other features.
"""
import pygame
import sys
import math
import os # For path.basename in playback mode status
import argparse

# --- Project Modules ---
from config_loader import load_config
from celestial_body import CelestialBody
from simulation_engine import SimulationEngine
from renderer import Renderer
from text_display import TextDisplay
from interaction_recorder import InteractionRecorder
from help_overlay import HelpOverlay
from interaction_player import InteractionPlayer

# --- Global Constants & Configuration ---
# Unit Conversion
AU_TO_METERS = 149.6e9
KM_TO_METERS = 1000
DAY_TO_SECONDS = 24 * 3600

# Configuration Data (loaded once)
CONFIG_DATA = load_config()

# Default Fallback Settings (used if CONFIG_DATA is empty or keys are missing)
DEFAULT_SCREEN_WIDTH = 800; DEFAULT_SCREEN_HEIGHT = 600
DEFAULT_BACKGROUND_HEX = "#000000"; DEFAULT_FPS = 60
DEFAULT_WINDOW_TITLE = "Solar System Model (Config Error)"
DEFAULT_SIM_TIME_STEP_DAYS = 0.1
DEFAULT_INITIAL_PIXELS_PER_AU = 50
DEFAULT_PANE_BORDER_COLOR = pygame.Color("gray30")
DEFAULT_PANE_BORDER_WIDTH = 1
DEFAULT_FALLBACK_FONT_SIZE = 36
PLANET_CLICK_BUFFER = 5 # Pixels around planet radius for easier clicking

# UI Pane Layout Ratios (Defaults)
DEFAULT_LP_RATIO = 0.35; DEFAULT_RP_RATIO = 0.35; DEFAULT_BP_RATIO = 0.20

# Apply Configuration or Defaults
APP_SETTINGS = {} # Dictionary to hold all runtime settings
if not CONFIG_DATA:
    print("CRITICAL: Configuration load failed. Using full fallback defaults.", file=sys.stderr)
    APP_SETTINGS['screen_width'] = DEFAULT_SCREEN_WIDTH; APP_SETTINGS['screen_height'] = DEFAULT_SCREEN_HEIGHT
    APP_SETTINGS['background_color_hex'] = DEFAULT_BACKGROUND_HEX; APP_SETTINGS['fps'] = DEFAULT_FPS
    APP_SETTINGS['window_title'] = DEFAULT_WINDOW_TITLE
    APP_SETTINGS['base_simulation_time_step_seconds'] = DEFAULT_SIM_TIME_STEP_DAYS * DAY_TO_SECONDS
    initial_celestial_bodies_data = {} # No bodies if config fails
    APP_SETTINGS['initial_scale_pixels_per_au'] = DEFAULT_INITIAL_PIXELS_PER_AU
    APP_SETTINGS['ui_layout_ratios'] = {'left_pane_width_ratio':DEFAULT_LP_RATIO,'right_pane_width_ratio':DEFAULT_RP_RATIO,'bottom_pane_height_ratio':DEFAULT_BP_RATIO}
else:
    display_cfg = CONFIG_DATA.get('display', {})
    APP_SETTINGS['screen_width'] = display_cfg.get('screen_width',DEFAULT_SCR_W); APP_SETTINGS['screen_height'] = display_cfg.get('screen_height',DEFAULT_SCR_H)
    APP_SETTINGS['background_color_hex'] = display_cfg.get('background_color',DEFAULT_BG_HEX)
    APP_SETTINGS['fps'] = display_cfg.get('fps', DEFAULT_FPS) # Allow FPS config

    simulation_cfg = CONFIG_DATA.get('simulation', {})
    time_step_days = simulation_cfg.get('time_step', DEFAULT_SIM_TIME_STEP_DAYS)
    APP_SETTINGS['base_simulation_time_step_seconds'] = time_step_days * DAY_TO_SECONDS

    initial_celestial_bodies_data = CONFIG_DATA.get('celestial_bodies', {}).copy() # Keep a pristine copy for resets

    ui_cfg = CONFIG_DATA.get('ui_layout', {})
    APP_SETTINGS['ui_layout_ratios'] = {
        'left_pane_width_ratio':ui_cfg.get('left_pane_width_ratio',DEFAULT_LP_RATIO),
        'right_pane_width_ratio':ui_cfg.get('right_pane_width_ratio',DEFAULT_RP_RATIO),
        'bottom_pane_height_ratio':ui_cfg.get('bottom_pane_height_ratio',DEFAULT_BP_RATIO)}
    APP_SETTINGS['window_title'] = "Solar System Orbital Model"
    APP_SETTINGS['initial_scale_pixels_per_au'] = display_cfg.get('initial_pixels_per_au',DEFAULT_PIX_PER_AU)

APP_SETTINGS['initial_scale_pixels_per_meter'] = APP_SETTINGS['initial_scale_pixels_per_au'] / AU_TO_METERS
try: APP_SETTINGS['background_color_rgb'] = pygame.Color(APP_SETTINGS['background_color_hex'])
except ValueError: APP_SETTINGS['background_color_rgb'] = pygame.Color(DEFAULT_BG_HEX); print(f"WARN: Invalid BG hex. Default black.",file=sys.stderr)

# --- Helper Functions (Mostly unchanged, ensure they use APP_SETTINGS or passed vals) ---
def calculate_pane_rects(screen_w, screen_h, ratios_dict): # As before
    bph=int(screen_h*ratios_dict['bottom_pane_height_ratio']); gah=screen_h-bph; lpw=int(screen_w*ratios_dict['left_pane_width_ratio']); rpw=int(screen_w*ratios_dict['right_pane_width_ratio'])
    rects={'bottom':pygame.Rect(0,gah,screen_w,bph),'left_graphics':pygame.Rect(0,0,lpw,gah),'right_graphics':pygame.Rect(lpw,0,rpw,gah)}
    if rects['right_graphics'].right>screen_w: rects['right_graphics'].width=screen_w-rects['right_graphics'].left
    if rects['right_graphics'].width<0: rects['right_graphics'].width=0; return rects
    return rects

def create_celestial_bodies_from_config(bodies_data_cfg, text_logger_func=None): # text_logger_func to add lines
    bodies_list=[]; creation_errors=0
    if not bodies_data_cfg: print("WARN: No celestial bodies in config to create.",file=sys.stderr); return bodies_list, creation_errors
    for body_name,data in bodies_data_cfg.items():
        try:
            m=float(data['mass']); r=float(data['radius']); c=data['color']; pa=data['initial_position']; pm=[p*AU_TO_METERS for p in pa]; vk=data['initial_velocity']; vm=[v*KM_TO_METERS for v in vk]
            bodies_list.append(CelestialBody(name=body_name,mass=m,radius=r,color=c,position=pm,velocity=vm))
        except KeyError as e: err_msg=f"ERROR Body '{body_name}': Missing key {e}."; print(err_msg,file=sys.stderr); creation_errors+=1; text_logger_func(err_msg) if text_logger_func else None
        except ValueError as e: err_msg=f"ERROR Body '{body_name}': Invalid value {e}."; print(err_msg,file=sys.stderr); creation_errors+=1; text_logger_func(err_msg) if text_logger_func else None
        except Exception as e: err_msg=f"ERROR Body '{body_name}': Unexpected {e}."; print(err_msg,file=sys.stderr); creation_errors+=1; text_logger_func(err_msg) if text_logger_func else None
    return bodies_list, creation_errors

def get_help_content_data(): # As before
    return [
        ("Help / Controls",True),("H: Toggle Help, ESC: Exit / Close Help",False),("",False),("Simulation Time",True),("  P: Play/Pause, ]: Speed Up, [: Speed Down, R: Reset",False),("",False),
        ("Camera (Left Pane)",True),("  Arrows: Pan, +/- or Wheel: Zoom",False),("",False),("Display",True),("  T: Toggle Orbital Paths",False),("",False),
        ("Interaction (Left Pane)",True),("  Left Mouse Click: Select Body (info in bottom pane)",False),("",False),("Recording",True),("  F9: Start/Stop Recording",False),("  (Files in 2506/recordings/)",False),("",False),
        ("UI Overview",True),("  Left Pane: Main interactive view",False),("  Right Pane: Secondary view (mirrors left)",False),("  Bottom Pane: Status messages and selected body info",False)]

# --- Main Application Class (Simplified Interface for Player) ---
class AppPlaybackInterface: # As before
    def __init__(self, game_state_ref, text_display_ref, recorder_ref, update_status_func_ref, reset_sim_func_ref):
        self.gs = game_state_ref; self.bottom_text_display = text_display_ref; self.recorder = recorder_ref
        self._update_status_text = update_status_func_ref; self._reset_simulation_state = reset_sim_func_ref
    def handle_sim_command_for_playback(self, command, data): # Logic as before
        if command=="TOGGLE_PAUSE":self.gs["is_paused"]=data.get("paused_state",not self.gs["is_paused"])
        elif command in ["SPEED_UP","SPEED_DOWN","SPEED_CHANGE"]:self.gs["simulation_speed_multiplier"]=data.get("new_multiplier",self.gs["simulation_speed_multiplier"])
        elif command=="RESET_SIMULATION":self._reset_simulation_state()
        elif command=="TOGGLE_PATHS":self.gs["show_orbital_paths"]=data.get("paths_visible",not self.gs["show_orbital_paths"])
        elif command=="SELECT_BODY":
            bn=data.get("body_name");self.gs["selected_body"]=next((b for b in self.gs["engine"].bodies if b.name==bn),None) if bn and self.gs["engine"] else None
        self._update_status_text()
    def handle_view_change_for_playback(self, pane_id, data): # Logic as before
        if pane_id=="left_graphics":
            if "scale" in data:self.gs["left_pane_scale"]=data["scale"]
            if "center" in data:self.gs["left_pane_view_center_m"]=data["center"]
    def reset_simulation_for_playback(self): self._reset_simulation_state()

# --- Main Function ---
def main(cli_args):
    try: pygame.init(); pygame.font.init()
    except pygame.error as e: print(f"CRITICAL: Pygame initialization failed: {e}", file=sys.stderr); sys.exit(1)

    try: screen=pygame.display.set_mode((APP_SETTINGS['screen_width'],APP_SETTINGS['screen_height']))
    except pygame.error as e: print(f"CRITICAL: Pygame set_mode failed: {e}", file=sys.stderr); sys.exit(1)
    pygame.display.set_caption(APP_SETTINGS['window_title']); clock=pygame.time.Clock()

    pane_rects=calculate_pane_rects(APP_SETTINGS['screen_width'],APP_SETTINGS['screen_height'],APP_SETTINGS['ui_layout_ratios'])
    try: lgs=screen.subsurface(pane_rects['left_graphics']); rgs=screen.subsurface(pane_rects['right_graphics']); bts=screen.subsurface(pane_rects['bottom'])
    except ValueError as e: print(f"CRITICAL: Subsurface creation failed: {e}\nRects: {pane_rects}",file=sys.stderr); sys.exit(1)
    pane_surfaces={'left_graphics':lgs,'right_graphics':rgs,'bottom':bts}
    PANE_BG_COLORS={'left_graphics':pygame.Color("#101010"),'right_graphics':pygame.Color("#151515"),'bottom':pygame.Color("#202020")}
    renderer=Renderer(CONFIG_DATA) # Pass original CONFIG_DATA

    game_state = { # Using more descriptive names now
        "is_paused": False, "_sim_was_paused_before_help": False, "simulation_speed_multiplier": 1.0,
        "selected_body": None, "show_orbital_paths": True, "left_pane_scale": APP_SETTINGS['initial_scale_pixels_per_meter'],
        "left_pane_view_center_m": [0.0,0.0,0.0], "right_pane_scale": APP_SETTINGS['initial_scale_pixels_per_meter'],
        "right_pane_view_center_m": [0.0,0.0,0.0], "engine": None, "list_of_bodies": [],
        "bottom_text_display": TextDisplay(font_size=16,font_color=pygame.Color("lightgray"),max_lines=60),
        "recorder": InteractionRecorder(output_dir="2506/recordings",config_snapshot=CONFIG_DATA), # Pass CONFIG_DATA
        "help_overlay": HelpOverlay(APP_SETTINGS['screen_width'],APP_SETTINGS['screen_height']) }
    game_state["help_overlay"].set_content(get_help_content_data())

    def reset_simulation_state_internal(): # Closure for main's reset logic
        game_state["list_of_bodies"],errs = create_celestial_bodies_from_config(initial_bodies_config_data, game_state["bottom_text_display"].add_line)
        if errs > 0: game_state["bottom_text_display"].add_line(f"--- {errs} ERRORS CREATING BODIES ---")
        if CONFIG_DATA and game_state["list_of_bodies"]:
            game_state["engine"]=SimulationEngine(game_state["list_of_bodies"],APP_SETTINGS['base_simulation_time_step_seconds'])
            if game_state["engine"].bodies: [b.position_history.clear() for b in game_state["engine"].bodies]; [b.position_history.append(b.position[:]) for b in game_state["engine"].bodies]
        else: game_state["engine"]=None; print("CRITICAL: Engine not init on reset.",file=sys.stderr); game_state["bottom_text_display"].add_line("CRIT: Engine not init (no bodies/cfg).")
        game_state["is_paused"]=False; game_state["simulation_speed_multiplier"]=1.0; game_state["selected_body"]=None; game_state["show_orbital_paths"]=True
        if game_state["engine"] and game_state["engine"].bodies:
            sun=next((b for b in game_state["engine"].bodies if b.name.lower()=="sun"),None)
            init_center = sun.position[:] if sun else game_state["engine"].bodies[0].position[:]
            game_state["left_pane_view_center_m"]=init_center; game_state["right_pane_view_center_m"]=init_center[:]
        else: game_state["left_pane_view_center_m"]=[0,0,0]; game_state["right_pane_view_center_m"]=[0,0,0]
        game_state["left_pane_scale"]=APP_SETTINGS['initial_scale_pixels_per_meter']; game_state["right_pane_scale"]=APP_SETTINGS['initial_scale_pixels_per_meter']
        if game_state["bottom_text_display"]: game_state["bottom_text_display"].add_line("--- Simulation Reset ---")
        print("Info: Simulation Reset.")

    app_player_interface = AppPlaybackInterface(game_state, game_state["bottom_text_display"], game_state["recorder"],
                                            lambda: update_status_text_display_internal(game_state), reset_simulation_state_internal)

    def update_status_text_display_internal(current_gs): # Takes game_state
        btd=current_gs["bottom_text_display"]; btd.add_line("-" * 80)
        status="Playing" if not current_gs["is_paused"] else "Paused"; paths_stat="Vis" if current_gs["show_orbital_paths"] else "Hid"
        rec_stat="REC" if current_gs["recorder"].is_recording else ("PLAYING" if cli_args.playback_file and player and player.is_playing else "Off")
        help_stat="ON" if current_gs["help_overlay"].is_active else "Off"
        btd.add_line(f"Status:{status}|Speed:x{current_gs['simulation_speed_multiplier']:.3f}|Paths(T):{paths_stat}|Rec(F9):{rec_stat}|Help(H):{help_stat}")
        if current_gs["engine"]: eff_dt=current_gs["engine"].base_time_step*current_gs['simulation_speed_multiplier']; btd.add_line(f"Sim:{len(current_gs['engine'].bodies)} bodies|Eff.dt:{eff_dt:.2f}s/fr")
        else: btd.add_line("Sim: Engine inactive.")
        sel_b=current_gs["selected_body"]
        if sel_b: pos=[p/AU_TO_METERS for p in sel_b.position]; vel=[v/KM_TO_METERS for v in sel_b.velocity]; btd.add_line(f"Sel:{sel_b.name}|Pos(AU):[{pos[0]:.2f},{pos[1]:.2f}]|Vel(km/s):[{vel[0]:.1f},{vel[1]:.1f}]") # Shorter info
        else: btd.add_line("Selected: None")

    reset_simulation_state_internal(); update_status_text_display_internal(game_state)

    player=None
    if cli_args.playback_file:
        player=InteractionPlayer(app_player_interface)
        if player.load_recording(cli_args.playback_file):
            if player.start_playback(): game_state["is_paused"]=False; print(f"Playback Mode: {os.path.basename(cli_args.playback_file)}"); game_state["bottom_text_display"].add_line(f"--- PLAYBACK: {os.path.basename(cli_args.playback_file)} ---")
            else: player=None
        else: player=None
        if not player: print(f"Could not start playback for {cli_args.playback_file}. Running interactive.",file=sys.stderr); game_state["bottom_text_display"].add_line(f"ERR: Playback failed for {os.path.basename(cli_args.playback_file)}")
        update_status_text_display_internal(game_state)

    running=True; main_loop_fc=0
    # Re-scope constants for main loop for clarity
    MIN_SIM_SPEED,MAX_SIM_SPEED,SIM_SPEED_FACTOR=(0.125,64.0,2.0)
    CAM_ZOOM_FACTOR=1.2; CAM_PAN_FRAC=0.1; MIN_CAM_SCALE=APP_SETTINGS['initial_scale_pixels_per_meter']/10000; MAX_CAM_SCALE=APP_SETTINGS['initial_scale_pixels_per_meter']*1000

    while running:
        main_loop_fc+=1;
        if game_state["recorder"].is_recording: game_state["recorder"].increment_frame_count()

        old_selected_body = game_state["selected_body"]
        old_left_scale = game_state["left_pane_scale"]
        old_left_center_x, old_left_center_y = game_state["left_pane_view_center_m"][0], game_state["left_pane_view_center_m"][1]

        if player and player.is_playing:
            player.process_next_events()
            if player.is_finished(): game_state["bottom_text_display"].add_line("--- Playback Finished ---"); player.stop_playback(); game_state["is_paused"]=True; update_status_text_display_internal(game_state)

        for ev in pygame.event.get():
            if not player or not player.is_playing: # Only record live events if not in active playback
                if game_state["recorder"]: game_state["recorder"].record_pygame_event(ev)
            if ev.type==pygame.QUIT: running=False
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_ESCAPE:
                    if game_state["help_overlay"].is_active: game_state["help_overlay"].toggle_visibility();game_state["is_paused"]=game_state["_sim_was_paused_before_help"]
                    else: running=False
                    update_status_text_display_internal(game_state)
                elif ev.key==pygame.K_h:
                    if game_state["help_overlay"].is_active: game_state["help_overlay"].toggle_visibility();game_state["is_paused"]=game_state["_sim_was_paused_before_help"]
                    else: game_state["_sim_was_paused_before_help"]=game_state["is_paused"];game_state["is_paused"]=True;game_state["help_overlay"].toggle_visibility()
                    update_status_text_display_internal(game_state)

                if not game_state["help_overlay"].is_active and (not player or not player.is_playing): # Live input for controls
                    if ev.key==pygame.K_F9: game_state["recorder"].toggle_recording(main_loop_fc); update_status_text_display_internal(game_state)
                    elif ev.key==pygame.K_p: game_state["is_paused"]=not game_state["is_paused"]; game_state["recorder"].record_sim_command({"cmd":"T_PAUSE","p_state":game_state["is_paused"]}); update_status_text_display_internal(game_state)
                    elif ev.key==pygame.K_LEFTBRACKET: old_m=game_state["simulation_speed_multiplier"]; game_state["simulation_speed_multiplier"]=max(MIN_SIM_SPEED,game_state["simulation_speed_multiplier"]/SIM_SPEED_FACTOR); if old_m!=game_state["simulation_speed_multiplier"]: game_state["recorder"].record_sim_command({"cmd":"SPD_CHG","val":game_state["simulation_speed_multiplier"]}); update_status_text_display_internal(game_state)
                    elif ev.key==pygame.K_RIGHTBRACKET:old_m=game_state["simulation_speed_multiplier"]; game_state["simulation_speed_multiplier"]=min(MAX_SIM_SPEED,game_state["simulation_speed_multiplier"]*SIM_SPEED_FACTOR); if old_m!=game_state["simulation_speed_multiplier"]: game_state["recorder"].record_sim_command({"cmd":"SPD_CHG","val":game_state["simulation_speed_multiplier"]}); update_status_text_display_internal(game_state)
                    elif ev.key==pygame.K_t: game_state["show_orbital_paths"]=not game_state["show_orbital_paths"]; game_state["recorder"].record_sim_command({"cmd":"T_PATHS","vis":game_state["show_orbital_paths"]}); update_status_text_display_internal(game_state)
                    elif ev.key==pygame.K_r: reset_simulation_state_internal(); game_state["recorder"].record_sim_command({"cmd":"RESET"}); update_status_text_display_internal(game_state)
                    elif ev.key==pygame.K_PLUS or ev.key==pygame.K_EQUALS : game_state["left_pane_scale"]=min(MAX_CAM_SCALE,game_state["left_pane_scale"]*CAM_ZOOM_FACTOR)
                    elif ev.key==pygame.K_MINUS : game_state["left_pane_scale"]=max(MIN_CAM_SCALE,game_state["left_pane_scale"]/CAM_ZOOM_FACTOR)

            if not game_state["help_overlay"].is_active and (not player or not player.is_playing): # Live mouse input
                if ev.type==pygame.MOUSEBUTTONDOWN:
                    if ev.button==1 and pane_surfaces['left_graphics'].get_rect().collidepoint(ev.pos[0]-pane_rects['left_graphics'].left, ev.pos[1]-pane_rects['left_graphics'].top):
                        if game_state["engine"] and game_state["engine"].bodies:
                            lc=(ev.pos[0]-pane_rects['left_graphics'].left,ev.pos[1]-pane_rects['left_graphics'].top); fo=None;mdsq=float('inf')
                            for b in game_state["engine"].bodies: bsp,ar=renderer.draw_body_on_surface(lgs,b,game_state["left_pane_view_center_m"],game_state["left_pane_scale"]); if not bsp:continue;dsq=(lc[0]-bsp[0])**2+(lc[1]-bsp[1])**2;if dsq<=(ar+PLANET_CLICK_BUFFER)**2 and dsq<mdsq:mdsq=dsq;fo=b
                            game_state["selected_body"]=fo
                    elif ev.button==4: game_state["left_pane_scale"]=min(MAX_CAM_SCALE,game_state["left_pane_scale"]*CAM_ZOOM_FACTOR)
                    elif ev.button==5: game_state["left_pane_scale"]=max(MIN_CAM_SCALE,game_state["left_pane_scale"]/CAM_ZOOM_FACTOR)

        if not player or not player.is_playing: # Record changes from live input
            if game_state["selected_body"] is not old_selected_body: game_state["recorder"].record_sim_command({"cmd":"SELECT","body":game_state["selected_body"].name if game_state["selected_body"] else None}); update_status_text_display_internal(game_state)
            if game_state["left_pane_scale"]!=old_left_scale: game_state["recorder"].record_view_change("left_graphics",{"scale":game_state["left_pane_scale"]})
            if not game_state["help_overlay"].is_active:
                k_pressed=pygame.key.get_pressed();pan_s=(pane_surfaces['left_graphics'].get_width()/game_state["left_pane_scale"] if game_state["left_pane_scale"]!=0 else 0)*CAM_PAN_FRAC
                if k_pressed[pygame.K_LEFT]:game_state["left_pane_view_center_m"][0]-=pan_s; elif k_pressed[pygame.K_RIGHT]:game_state["left_pane_view_center_m"][0]+=pan_s
                if k_pressed[pygame.K_UP]:game_state["left_pane_view_center_m"][1]+=pan_s; elif k_pressed[pygame.K_DOWN]:game_state["left_pane_view_center_m"][1]-=pan_s
                if old_left_center_x!=game_state["left_pane_view_center_m"][0] or old_left_center_y!=game_state["left_pane_view_center_m"][1]: game_state["recorder"].record_view_change("left_graphics",{"center":game_state["left_pane_view_center_m"][:]})

        if game_state["engine"] and not game_state["is_paused"]: game_state["engine"].update_simulation(APP_SETTINGS['base_simulation_time_step_seconds']*game_state["simulation_speed_multiplier"])

        screen.fill(APP_SETTINGS['background_color_rgb']);[s.fill(PANE_BG_COLORS[k])for k,s in pane_surfaces.items()]
        sbn_name=game_state["selected_body"].name if game_state["selected_body"] else None
        if game_state["engine"] and game_state["engine"].bodies:
            renderer.render_all_bodies_to_surface(lgs,game_state["engine"].bodies,game_state["left_pane_view_center_m"],game_state["left_pane_scale"],sbn_name,game_state["show_orbital_paths"])
            renderer.render_all_bodies_to_surface(rgs,game_state["engine"].bodies,game_state["right_pane_view_center_m"],game_state["right_pane_scale"],None,game_state["show_orbital_paths"])
        else: font_fb=pygame.font.SysFont(None,DEFAULT_FALLBACK_FONT_SIZE);ts_fb=font_fb.render("No sim data.",True,pygame.Color("darkgray"));[s.blit(ts_fb,ts_fb.get_rect(center=(s.get_width()//2,s.get_height()//2))) for k,s in pane_surfaces.items() if k!='bottom']
        game_state["bottom_text_display"].render_to_surface(bts);[pygame.draw.rect(screen,DEFAULT_PANE_BORDER_COLOR,r,DEFAULT_PANE_BORDER_WIDTH)for r in pane_rects.values()]
        if game_state["help_overlay"].is_active:game_state["help_overlay"].draw(screen)
        if main_loop_fc%(APP_SETTINGS['fps']*10)==0 and APP_SETTINGS['fps']>0 and main_loop_fc>0 and (not game_state["help_overlay"].is_active and (game_state["selected_body"] or not game_state["is_paused"])): update_status_text_display_internal(game_state)
        pygame.display.flip();clock.tick(APP_SETTINGS['fps'])

    if game_state["recorder"] and game_state["recorder"].is_recording:game_state["recorder"].stop()
    pygame.quit();sys.exit()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description="Interactive Solar System Orbital Model."); parser.add_argument("--playback",type=str,help="Path to interaction recording JSON file to play back.")
    cli_args=parser.parse_args()
    if not CONFIG_DATA and not cli_args.playback_file: print("CRITICAL ERR: Config load failed & not in playback. Exiting.",file=sys.stderr); sys.exit(1)
    main(cli_args)
