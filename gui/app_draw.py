from simulation.tdoa import (
    range_diff_field,
    range_diff_level
)

import numpy as np
import matplotlib.cm as cm


class DrawMixin:
    def _redraw_all(self):
        self._draw_xy()
        self._draw_xz()
        self._draw_yz()

    def _station_color(self, station_id: int):
        cmap = cm.get_cmap("tab10")
        return cmap((station_id - 1) % 10)
    
    def _draw_xy(self):
        ax = self.xy_view.ax
        ax.clear()
        self.xy_view.reset_axes()

        for s in self.scene.get_stations():
            x, y, z = s.get_position()
            c = self._station_color(s.id)
            ax.plot([x], [y], marker="^", markersize=8, color=c)
            ax.text(x+10, y+10, f"S{s.id}: (z={z})", fontsize=8,  color=c )

        for t in self.scene.get_targets():
            x, y, z= t.get_position()
            c = self._station_color(t.id)
            ax.plot([x], [y], marker="o", markersize=8, color=c)
            ax.text(x+10, y+10, f"T{t.id}: (z={z})", fontsize=8, color=c)

        self.xy_view.canvas.draw_idle()

    def _draw_xz(self):
        ax = self.xz_view.ax
        ax.clear()
        self.xz_view.reset_axes()

        for s in self.scene.get_stations():
            x, _, z = s.get_position()
            c = self._station_color(s.id)
            ax.plot([x], [z], marker="^", markersize=6, color=c)
            ax.text(x+10, z+10, f"S{s.id}", fontsize=8, color=c)

        for t in self.scene.get_targets():
            x, _, z = t.get_position()
            c = self._station_color(t.id)
            ax.plot([x], [z], marker="o", markersize=6, color=c)
            ax.text(x+10, z+10, f"T{t.id}", fontsize=8, color=c)

        self.xz_view.canvas.draw_idle()

    def _draw_yz(self):
        ax = self.yz_view.ax
        ax.clear()
        self.yz_view.reset_axes()

        for s in self.scene.get_stations():
            _, y, z = s.get_position()
            c = self._station_color(s.id)
            ax.plot([y], [z], marker="^", markersize=6, color=c )
            ax.text(y+10, z+10, f"S{s.id}", fontsize=8, color=c)

        for t in self.scene.get_targets():
            _, y, z = t.get_position()
            c = self._station_color(t.id)
            ax.plot([y], [z], marker="o", markersize=6, color=c)
            ax.text(y+10, z+10, f"T{t.id}", fontsize=8, color=c)

        self.yz_view.canvas.draw_idle()

    def _draw_hyperbolas_for_target(self, target, stations, ref_id, tdoa):
        specs = [
            ("xy", self.xy_view, 200, 0, 1, 2),  
            ("xz", self.xz_view, 180, 0, 2, 1),
            ("yz", self.yz_view, 180, 1, 2, 0),
        ]
        for plane, view, n, axis0, axis1, fixed_axis in specs:
            self._draw_hyperbolas_plane(
                plane=plane,
                view=view,
                target=target,
                stations=stations,
                ref_id=ref_id,
                tdoa=tdoa,
                n=n,
                axis0=axis0,
                axis1=axis1,
                fixed_axis=fixed_axis,
            )

    def _draw_hyperbolas_plane(
        self,
        plane: str,
        view,
        target,
        stations,
        ref_id,
        tdoa,
        n: int,
        axis0: int,
        axis1: int,
        fixed_axis: int,
    ):
        bounds = self.scene.bounds  

        fixed_value = target.get_position()[fixed_axis]

        s_ref = next(s for s in stations if s.id == ref_id)
        ref_pos = s_ref.get_position()

        (lo0, hi0) = bounds[axis0]
        (lo1, hi1) = bounds[axis1]

        v0 = np.linspace(lo0, hi0, n)
        v1 = np.linspace(lo1, hi1, n)
        A0, A1 = np.meshgrid(v0, v1)

        ax = view.ax

        for s in stations:
            if s.id == ref_id:
                continue

            F = range_diff_field(A0, A1, plane, fixed_value, s.get_position(), ref_pos)
            level = range_diff_level(tdoa[s.id])
            c = self._station_color(s.id)
            ax.contour(A0, A1, F, levels=[level], linewidths=1, colors=[c])


        view.canvas.draw_idle()
