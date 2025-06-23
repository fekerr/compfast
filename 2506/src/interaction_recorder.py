# src/interaction_recorder.py
"""
Provides InteractionRecorder for capturing events to JSON.
"""
import pygame
import json
import time
import os
import sys

class InteractionRecorder:
    EVENT_TYPE_PYGAME="PYGAME_EVENT"; EVENT_TYPE_SIM_COMMAND="SIM_COMMAND"; EVENT_TYPE_VIEW_CHANGE="VIEW_CHANGE"; EVENT_TYPE_META="META_EVENT"
    RECORDING_FORMAT_VERSION = "1.0.1" # Incremented version for metadata change

    def __init__(self,output_dir="recordings",config_snapshot=None):
        # (Docstring from previous step)
        self.events=[]; self.start_time_ticks=0; self.start_time_wall=0.0; self.output_dir=output_dir
        self.config_snapshot=config_snapshot if config_snapshot else {}
        self.is_recording=False; self.frame_count_at_recording_start=0; self.current_recording_frame=0
        if not os.path.exists(self.output_dir):
            try: os.makedirs(self.output_dir); print(f"Info: Created recordings directory: {self.output_dir}")
            except OSError as e: print(f"ERROR: Could not create recordings directory '{self.output_dir}': {e}. Recordings will be saved to current directory ('.').",file=sys.stderr); self.output_dir="."

    def start(self,main_loop_frame_count=0): # Unchanged from previous refactor
        self.events=[]; self.start_time_ticks=pygame.time.get_ticks(); self.start_time_wall=time.time()
        self.frame_count_at_recording_start=main_loop_frame_count; self.current_recording_frame=0; self.is_recording=True
        print(f"Info: Recording started. Output directory: {self.output_dir}")
        self.record_event(self.EVENT_TYPE_META,{"command":"RECORDING_START","main_loop_frame_at_start":self.frame_count_at_recording_start})

    def stop(self): # Unchanged from previous refactor
        if not self.is_recording: return None
        self.record_event(self.EVENT_TYPE_META,{"command":"RECORDING_STOP","main_loop_frame_at_stop":self.frame_count_at_recording_start+self.current_recording_frame})
        self.is_recording=False; filepath=self.save_to_file()
        if filepath: print(f"Info: Recording stopped. Saved {len(self.events)} events to {filepath}")
        else: print("Warning: Recording stopped but save failed or no events were recorded.", file=sys.stderr)
        return filepath

    def toggle_recording(self,main_loop_frame_count=0): return self.stop() if self.is_recording else self.start(main_loop_frame_count)

    def record_pygame_event(self,event): # Adding more pygame event attributes
        if not self.is_recording: return
        serializable_event={'type':event.type,'type_name':pygame.event.event_name(event.type)}
        if hasattr(event,'key'): serializable_event.update({'key':event.key,'key_name':pygame.key.name(event.key),'mod':event.mod,'unicode':event.unicode,'scancode':getattr(event,'scancode',None)})
        if hasattr(event,'pos'): serializable_event['pos']=event.pos
        if hasattr(event,'rel'): serializable_event['rel']=event.rel # For MOUSEMOTION
        if hasattr(event,'button'): serializable_event['button']=event.button # For MOUSEBUTTONUP/DOWN
        if hasattr(event,'buttons'): serializable_event['buttons']=event.buttons # For MOUSEMOTION
        if event.type == pygame.MOUSEWHEEL: # Explicit MOUSEWHEEL handling
             serializable_event.update({'y':event.y, 'x':getattr(event,'x',0), 'flipped':getattr(event,'flipped',False)})
        self.record_event(self.EVENT_TYPE_PYGAME,serializable_event)

    def record_sim_command(self,command_details): self.record_event(self.EVENT_TYPE_SIM_COMMAND,command_details) if self.is_recording else None
    def record_view_change(self,pane_id,view_params): self.record_event(self.EVENT_TYPE_VIEW_CHANGE,{'pane':pane_id,**view_params}) if self.is_recording else None

    def record_event(self,category,data): # Renamed from _record_event_raw
        if not self.is_recording: return
        ts_rel_ms=pygame.time.get_ticks()-self.start_time_ticks
        self.events.append({"timestamp_ms":ts_rel_ms,"frame_in_recording":self.current_recording_frame,"category":category,"data":data})

    def increment_frame_count(self):
        if self.is_recording: self.current_recording_frame+=1

    def save_to_file(self): # Unchanged from previous refactor, uses ISO time
        if not self.events: print("Info: No events recorded to save.", file=sys.stderr); return None
        ts_str=time.strftime("%Y%m%d_%H%M%S",time.localtime(self.start_time_wall)); filename=f"rec_{ts_str}.json"; filepath=os.path.join(self.output_dir,filename)
        metadata={"recording_format_version":self.RECORDING_FORMAT_VERSION, "start_time_wall_iso":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(self.start_time_wall)),
                  "start_time_ticks_ms_pygame":self.start_time_ticks, "start_main_loop_frame":self.frame_count_at_recording_start,
                  "total_duration_recorded_ms":self.events[-1]["timestamp_ms"] if self.events else 0, "total_frames_in_recording":self.current_recording_frame,
                  "source_config_snapshot":self.config_snapshot}
        try:
            with open(filepath,'w') as f: json.dump({"metadata":meta,"events":self.events},f,indent=2)
            return filepath
        except IOError as e: print(f"ERROR saving recording to '{filepath}': {e}",file=sys.stderr); return None
        except Exception as e: print(f"ERROR unexpected while saving recording: {e}",file=sys.stderr); return None
