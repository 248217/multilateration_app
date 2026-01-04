

# gui/app_stats.py
import csv
import os
import math
import statistics as stats
import customtkinter as ctk

from simulation.tdoa import simulate_arrival_times, compute_tdoa
from simulation.localization import estimate_position


class StatsMixin:

    def _run_one_localization(self, target, stations, ref_id):
        arrival = simulate_arrival_times(target, stations)
        tdoa = compute_tdoa(arrival, reference_id=ref_id)

        ex, ey, ez = estimate_position(
            stations,
            reference_id=ref_id,
            tdoa=tdoa,
            initial_guess=(1000, 1000, 500),
        )

        tx, ty, tz = target.get_position()
        err = math.dist((tx, ty, tz), (ex, ey, ez))
        err_xy = math.dist((tx, ty), (ex, ey))
        err_z = abs(tz - ez)

        return (tx, ty, tz), (ex, ey, ez), err, err_xy, err_z

    def _get_stats(self):
        stations = self.scene.get_stations()
        targets = self.scene.get_targets()

        if len(stations) < 4:
            self.log_panel.write("ERROR: Need at least 4 stations to run stats.")
            return
        if len(targets) < 1:
            self.log_panel.write("ERROR: Need at least 1 target to run stats.")
            return

        cfg = self._prompt_stats_config()
        if cfg is None:
            return
        test_name, n_runs, ref_id = cfg

        def mean(a): return sum(a) / len(a)
        def rmse(a): return (sum(v * v for v in a) / len(a)) ** 0.5
        def stdev(a): return stats.stdev(a) if len(a) > 1 else 0.0

        rows = []
        for t in targets:
            errs, errs_xy, errs_z = [], [], []
            est_xs, est_ys, est_zs = [], [], []

            tx, ty, tz = t.get_position()

            for _ in range(n_runs):
                _, (ex, ey, ez), err, err_xy, err_z = self._run_one_localization(
                    t, stations, ref_id
                )
                errs.append(err)
                errs_xy.append(err_xy)
                errs_z.append(err_z)

                est_xs.append(ex)
                est_ys.append(ey)
                est_zs.append(ez)

            row = {
                "test_name": test_name,

                "target_id": getattr(t, "id", None),
                "n_runs": n_runs,
                "ref_station_id": ref_id,

                "true_x": tx, "true_y": ty, "true_z": tz,

                "mean_est_x": mean(est_xs),
                "mean_est_y": mean(est_ys),
                "mean_est_z": mean(est_zs),

                "mean_err": mean(errs),
                "rmse_err": rmse(errs),
                "std_err": stdev(errs),
                "min_err": min(errs),
                "max_err": max(errs),

                "mean_err_xy": mean(errs_xy),
                "rmse_err_xy": rmse(errs_xy),
                "std_err_xy": stdev(errs_xy),

                "mean_err_z": mean(errs_z),
                "rmse_err_z": rmse(errs_z),
                "std_err_z": stdev(errs_z),
            }
            rows.append(row)

            self.log_panel.write(
                f"Stats T{getattr(t, 'id', '?')}: "
                f"mean_err={row['mean_err']:.3f}  rmse_err={row['rmse_err']:.3f}  "
                f"mean_xy={row['mean_err_xy']:.3f}  mean_z={row['mean_err_z']:.3f}"
            )

        if not rows:
            self.log_panel.write("No rows produced.")
            return

        csv_path = "stats.csv"
        fieldnames = list(rows[0].keys())
        write_header = (not os.path.exists(csv_path)) or (os.path.getsize(csv_path) == 0)

        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                w.writeheader()
            w.writerows(rows)

        self.log_panel.write(f"OK: appended {len(rows)} row(s) to {csv_path}")

        # optional redraw if you want
        if hasattr(self, "_redraw_all"):
            self._redraw_all()
