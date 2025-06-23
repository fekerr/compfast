# src/simulation_engine.py
"""
Provides the SimulationEngine class for managing orbital mechanics simulation.
"""
from celestial_body import CelestialBody, vec_add, vec_scale # Minimal imports
import sys

class SimulationEngine:
    """Manages and simulates orbital mechanics of celestial bodies."""
    def __init__(self, celestial_bodies, base_time_step, integration_method='rk4'):
        # (Docstring from previous step assumed sufficient)
        self.bodies = list(celestial_bodies)
        self.base_time_step = float(base_time_step)
        if self.base_time_step <= 0:
            print(f"Warning: Simulation base_time_step is {self.base_time_step}s. Must be positive. Clamping to 0.1s.", file=sys.stderr)
            self.base_time_step = 0.1 # Fallback to a small positive time step
        self.integration_method = str(integration_method).lower()
        if not self.bodies: print("Warning: SimulationEngine initialized with no bodies.", file=sys.stderr)
        if self.integration_method not in ['rk4', 'euler']:
            print(f"Warning: Unknown integration method '{self.integration_method}'. Defaulting to 'rk4'.", file=sys.stderr)
            self.integration_method = 'rk4'

    def _calculate_all_forces_at_state(self, temp_states): # Unchanged from previous refactor
        all_net_forces={}; original_positions={b:b.position[:] for b in self.bodies}
        try:
            for body,(pos,_) in temp_states.items():
                if body in self.bodies: body.position=pos
            for target in self.bodies:
                net_f=[0.0,0.0,0.0]
                for other in self.bodies:
                    if target is other: continue
                    net_f=vec_add(net_f,target.calculate_gravitational_force(other))
                all_net_forces[target]=net_f
        finally:
            for body,pos in original_positions.items():
                if body in self.bodies: body.position=pos
        return all_net_forces

    def update_simulation(self, current_time_step=None): # Unchanged from previous refactor
        dt=current_time_step if current_time_step is not None else self.base_time_step
        if dt <= 0: # Prevent non-positive time steps at point of use
             print(f"Warning: Simulation update called with non-positive time_step {dt}s. Skipping update.", file=sys.stderr)
             return
        if not self.bodies: return
        if self.integration_method=='rk4': self._update_rk4(dt)
        elif self.integration_method=='euler': self._update_euler_basic(dt)
        else: print(f"Error: Unsupported integration method '{self.integration_method}'. No update performed.", file=sys.stderr)

    def _update_euler_basic(self, time_step): # Unchanged from previous refactor
        states={b:(b.position[:],b.velocity[:]) for b in self.bodies}; forces=self._calculate_all_forces_at_state(states)
        for b in self.bodies:
            acc=vec_scale(forces[b],1.0/b.mass) if b.mass!=0 else [0.0,0.0,0.0]
            b.velocity=vec_add(b.velocity,vec_scale(acc,time_step))
            b.position=vec_add(b.position,vec_scale(b.velocity,time_step))
            b.update_post_simulation()

    def _update_rk4(self, time_step): # Unchanged from previous refactor
        initial_states={b:(b.position[:],b.velocity[:]) for b in self.bodies}
        k1d,k2d,k3d,k4d={},{},{},{}
        f_k1=self._calculate_all_forces_at_state(initial_states)
        for b in self.bodies: (p,v)=initial_states[b]; f=f_k1[b]; (vd,ad)=b.get_state_derivatives(p,v,f); k1d[b]=(vec_scale(vd,time_step),vec_scale(ad,time_step))
        ts_k2={}; for b in self.bodies: (p,v)=initial_states[b];(dp,dv)=k1d[b]; ts_k2[b]=(vec_add(p,vec_scale(dp,0.5)),vec_add(v,vec_scale(dv,0.5)))
        f_k2=self._calculate_all_forces_at_state(ts_k2)
        for b in self.bodies: (p,v)=ts_k2[b]; f=f_k2[b]; (vd,ad)=b.get_state_derivatives(p,v,f); k2d[b]=(vec_scale(vd,time_step),vec_scale(ad,time_step))
        ts_k3={}; for b in self.bodies: (p,v)=initial_states[b];(dp,dv)=k2d[b]; ts_k3[b]=(vec_add(p,vec_scale(dp,0.5)),vec_add(v,vec_scale(dv,0.5)))
        f_k3=self._calculate_all_forces_at_state(ts_k3)
        for b in self.bodies: (p,v)=ts_k3[b]; f=f_k3[b]; (vd,ad)=b.get_state_derivatives(p,v,f); k3d[b]=(vec_scale(vd,time_step),vec_scale(ad,time_step))
        ts_k4={}; for b in self.bodies: (p,v)=initial_states[b];(dp,dv)=k3d[b]; ts_k4[b]=(vec_add(p,dp),vec_add(v,dv))
        f_k4=self._calculate_all_forces_at_state(ts_k4)
        for b in self.bodies: (p,v)=ts_k4[b]; f=f_k4[b]; (vd,ad)=b.get_state_derivatives(p,v,f); k4d[b]=(vec_scale(vd,time_step),vec_scale(ad,time_step))
        for b in self.bodies:
            (pn,vn)=initial_states[b]; (k1dp,k1dv)=k1d[b]; (k2dp,k2dv)=k2d[b]; (k3dp,k3dv)=k3d[b]; (k4dp,k4dv)=k4d[b]
            fdp=vec_scale(vec_add(vec_add(k1dp,vec_scale(k2dp,2.0)),vec_add(vec_scale(k3dp,2.0),k4dp)),1.0/6.0)
            fdv=vec_scale(vec_add(vec_add(k1dv,vec_scale(k2dv,2.0)),vec_add(vec_scale(k3dv,2.0),k4dv)),1.0/6.0)
            b.position=vec_add(pn,fdp); b.velocity=vec_add(vn,fdv)
            b.acceleration=vec_scale(f_k1[b],1.0/b.mass) if b.mass!=0 else [0.0,0.0,0.0]
            b.update_post_simulation()
