from simulation.station import Station
from simulation.target import Target
import math


class EventsMixin:
    def _bind_events(self):
        self.xy_view.canvas.mpl_connect("button_press_event", self._on_xy_click)

    def _on_xy_click(self, event):
        xy = self._validate_xy_click(event)
        if xy is None:
            return
        x, y = xy

        handler = {
            "station": self._handle_station_click,
            "target": self._handle_target_click,
            "triangle": self._handle_triangle_click,
        }.get(self.mode)

        if handler is None:
            return

        handler(x, y)
        self._redraw_all()

    def _validate_xy_click(self, event):
        if self.mode not in ("station", "target", "triangle"):
            return None
        if event.inaxes != self.xy_view.ax:
            return None
        if event.xdata is None or event.ydata is None:
            return None
        return float(event.xdata), float(event.ydata)
    
    def _add_station(self, x, y, z, prefix="Added Station"):
        s = Station(self._station_id, (x, y, z))
        try:
            self.scene.add_station(s)
        except ValueError as e:
            self.log_panel.write(f"ERROR: {e}")
            return None

        self.log_panel.write(f"{prefix} {s.id}: ({x:.1f}, {y:.1f}, {z:.1f})")
        self._station_id += 1
        return s
    
    def _handle_station_click(self, x, y):
        z = self._prompt_z(self._station_id)
        if z is None:
            return
        self._add_station(x, y, z)

    def _handle_target_click(self, x, y):
        z = self._prompt_z(self._target_id)
        if z is None:
            return

        t = Target(self._target_id, (x, y, z))
        try:
            self.scene.add_target(t)
        except ValueError as e:
            self.log_panel.write(f"ERROR: {e}")
            return

        self.log_panel.write(f"Added Target {t.id}: ({x:.1f}, {y:.1f}, {z:.1f})")
        self._target_id += 1

    def _handle_triangle_click(self, x, y):
        if self._triangle_centroid is None:
            z = self._prompt_z(self._station_id)
            if z is None:
                return

            self._triangle_centroid = (x, y, z)

            self._add_station(x, y, z, prefix="Triangle centroid station")

            self.log_panel.write(
                f"Triangle centroid set at ({x:.1f}, {y:.1f}, {z:.1f}). Click a vertex to set size."
            )
            return

        centroid = self._triangle_centroid
        vertex_xy = (x, y)

        positions = self.equilateral_triangle_positions_from_centroid_and_vertex(
            centroid, vertex_xy
        )

        for (px, py, pz) in positions:
            self._add_station(px, py, pz, prefix="Triangle vertex station")

        self._triangle_centroid = None  

    def equilateral_triangle_positions_from_centroid_and_vertex(self, centroid, vertex_xy):
        cx, cy, _ = centroid
        vx, vy = vertex_xy

        zs = self._prompt_triangle_vertex_zs()
        if zs is None:
            return None
        z1, z2, z3 = zs

        dx = vx - cx
        dy = vy - cy
        R = math.hypot(dx, dy)
        if R == 0:
            raise ValueError("Vertex cannot equal centroid")

        cos120 = -0.5
        sin120 = math.sqrt(3) / 2

        rx1 = dx * cos120 - dy * sin120
        ry1 = dx * sin120 + dy * cos120

        rx2 = dx * cos120 + dy * sin120
        ry2 = -dx * sin120 + dy * cos120

        p1 = (vx, vy, z1)
        p2 = (cx + rx1, cy + ry1, z2)
        p3 = (cx + rx2, cy + ry2, z3)

        return [p1, p2, p3]
