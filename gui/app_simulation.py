from simulation.tdoa import (
    simulate_arrival_times,
    compute_tdoa
)
from simulation.localization import (
    estimate_position  
)
import math

class SimulationMixin:
    def _start_simulation(self):
        stations = self.scene.get_stations()
        targets = self.scene.get_targets()

        if len(stations) < 4:
            self.log_panel.write("ERROR: Need at least 4 stations.")
            return
        if len(targets) < 1:
            self.log_panel.write("ERROR: Need at least 1 target.")
            return

        ref_id = self._prompt_reference_station()
        self.log_panel.write(f"Starting simulation. Reference station: {ref_id}")

        for t in targets:
            arrival = simulate_arrival_times(t, stations)
            tdoa = compute_tdoa(arrival, reference_id=ref_id)

            est = estimate_position(stations, reference_id=ref_id, tdoa=tdoa, initial_guess=(1000, 1000, 500))

            tx, ty, tz = t.get_position()
            ex, ey, ez = est
            err = math.dist((tx, ty, tz), (ex, ey, ez))
            err_xy = math.dist((tx, ty), (ex, ey))
            err_z = abs(tz - ez)


            self.log_panel.write(
                f"T{t.id} true=({tx:.2f},{ty:.2f},{tz:.2f})  "
                f"est=({ex:.2f},{ey:.2f},{ez:.2f})  err={err:.3f} m  err_xy={err_xy:.3f} m  err_z={err_z:.3f} m"
            )

        self._redraw_all()
        self._draw_hyperbolas_for_target(t, stations, ref_id, tdoa)
    
        return (tx, ty, tz), (ex, ey, ez), err, err_xy, err_z
