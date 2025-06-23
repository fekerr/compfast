import pygame
import json
import sys
import os

# Event types (should match InteractionRecorder)
EVENT_TYPE_PYGAME = "PYGAME_EVENT"
EVENT_TYPE_SIM_COMMAND = "SIM_COMMAND"
EVENT_TYPE_VIEW_CHANGE = "VIEW_CHANGE"
EVENT_TYPE_META = "META_EVENT" # For start/stop info

class InteractionPlayer:
    """Plays back recorded interactions and simulation events from a JSON file."""

    def __init__(self, app_interface):
        """
        Initializes the InteractionPlayer.
        Args:
            app_interface: An object/class instance that provides methods to interact
                           with the main application's state and functions.
        """
        self.events = []
        self.metadata = {}
        self.current_event_index = 0
        self.playback_start_time_ticks = 0 # Pygame ticks when playback actually starts
        self.recording_start_time_ticks = 0 # Pygame ticks from the recording's metadata (t_0 for recorded events)
        self.is_playing = False
        self.app_interface = app_interface

    def load_recording(self, filepath):
        """Loads a recording from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                recording_data = json.load(f)
            self.metadata = recording_data.get("metadata", {})
            self.events = recording_data.get("events", [])
            self.recording_start_time_ticks = self.metadata.get("start_time_ticks_ms_pygame", 0) # Match recorder key
            self.current_event_index = 0
            if not self.events:
                print(f"Warning: Recording file '{filepath}' contains no events.", file=sys.stderr)
                return False
            print(f"Loaded recording: {os.path.basename(filepath)} ({len(self.events)} events)")
            return True
        except FileNotFoundError:
            print(f"ERROR: Recording file not found: {filepath}", file=sys.stderr)
            return False
        except json.JSONDecodeError as e:
            print(f"ERROR: Could not decode JSON from '{filepath}': {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"ERROR: Unexpected error loading recording '{filepath}': {e}", file=sys.stderr)
            return False

    def start_playback(self):
        """
        Prepares and starts the playback process.
        Assumes the main application has been reset to a suitable initial state.
        """
        if not self.events:
            print("ERROR: No events loaded to start playback.", file=sys.stderr)
            self.is_playing = False
            return False

        # Reset simulation via app interface - this is crucial for determinism
        if hasattr(self.app_interface, "reset_simulation_for_playback") and            callable(self.app_interface.reset_simulation_for_playback):
            self.app_interface.reset_simulation_for_playback()
            print("Player: Requested simulation reset via app interface.")
        else:
            print("Warning: Player could not request simulation reset from app interface.", file=sys.stderr)

        self.current_event_index = 0
        self.playback_start_time_ticks = pygame.time.get_ticks() # Current time when playback begins
        self.is_playing = True
        print("Playback started.")
        return True

    def stop_playback(self):
        """Stops playback."""
        self.is_playing = False
        print("Playback stopped.")


    def process_next_events(self):
        """
        Processes and dispatches all events that are due based on the current playback time.
        This should be called once per game frame during playback mode.
        """
        if not self.is_playing or self.is_finished():
            if self.is_playing and self.is_finished(): # Was playing but just finished
                self.stop_playback()
            return

        # Effective time that should have elapsed in the recording's timeline
        current_recording_timeline_ticks = (pygame.time.get_ticks() - self.playback_start_time_ticks) # + self.recording_start_time_ticks if events are relative to it
                                                                                                   # The events are already relative to their recording_start_time_ticks (timestamp_ms)

        while self.current_event_index < len(self.events):
            event_record = self.events[self.current_event_index]
            event_timestamp_ms_in_recording = event_record.get("timestamp_ms", 0) # This is already relative to its recording's start

            if event_timestamp_ms_in_recording <= current_recording_timeline_ticks:
                self._dispatch_event(event_record)
                self.current_event_index += 1
            else:
                # Next event is in the future relative to current playback progress
                break

    def _dispatch_event(self, event_record):
        """Dispatches a single event record to the application via the app_interface."""
        category = event_record.get("category")
        data = event_record.get("data", {})

        # For debugging: print(f"Playback Dispatch @{current_recording_timeline_ticks}ms (Event ts {event_timestamp_ms_in_recording}ms): Cat='{category}', Data='{data}'")

        if category == EVENT_TYPE_PYGAME:
            try:
                event_type = data.get('type')
                # Filter out attributes not part of pygame.event.Event constructor or problematic ones
                # For example, 'type_name' was added for recorder logging, not for Event creation
                valid_attrs = {k: v for k, v in data.items() if k not in ['type', 'type_name', 'name', 'key_name']}

                if event_type is not None:
                    new_event = pygame.event.Event(event_type, **valid_attrs)
                    pygame.event.post(new_event)
                else:
                    print(f"Warning: Pygame event in recording missing 'type': {data}", file=sys.stderr)
            except Exception as e:
                print(f"ERROR dispatching Pygame event {data}: {e}", file=sys.stderr)

        elif category == EVENT_TYPE_SIM_COMMAND:
            command = data.get("command") # In recorder, some are data.get("cmd")
            if 'cmd' in data and 'command' not in data: command = data.get("cmd") # Handle key mismatch

            if hasattr(self.app_interface, "handle_sim_command_for_playback"):
                self.app_interface.handle_sim_command_for_playback(command, data)
            else:
                print(f"Warning: App interface cannot handle sim command: {command}", file=sys.stderr)

        elif category == EVENT_TYPE_VIEW_CHANGE:
            pane_id = data.get("pane")
            if hasattr(self.app_interface, "handle_view_change_for_playback"):
                self.app_interface.handle_view_change_for_playback(pane_id, data)
            else:
                print(f"Warning: App interface cannot handle view change for pane: {pane_id}", file=sys.stderr)

        elif category == EVENT_TYPE_META: # E.g. "RECORDING_START", "RECORDING_STOP"
            pass # Usually not re-enacted, but could be logged by player
        else:
            print(f"Warning: Unknown event category in recording: {category}", file=sys.stderr)

    def is_finished(self):
        """Checks if all recorded events have been processed."""
        return self.current_event_index >= len(self.events)
