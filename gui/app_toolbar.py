import customtkinter as ctk
from simulation.scene import Scene


class ToolbarMixin(Scene):
    def _build_toolbar(self):
        self.toolbar = ctk.CTkFrame(self, height=50)
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        self.toolbar.grid_columnconfigure(10, weight=1)

        self.btn_place_station = ctk.CTkButton(
            self.toolbar, text="Place Station", command=self._set_mode_station
        )
        self.btn_place_station.grid(row=0, column=0, padx=6, pady=6, sticky="w")

        self.btn_triangle = ctk.CTkButton(
            self.toolbar, text="Place Triangle", command=self._set_mode_triangle
        )
        self.btn_triangle.grid(row=0, column=1, padx=6, pady=6, sticky="w")  

        self.btn_place_target = ctk.CTkButton(
            self.toolbar, text="Place Target", command=self._set_mode_target
        )
        self.btn_place_target.grid(row=0, column=2, padx=6, pady=6, sticky="w")

        self.btn_start = ctk.CTkButton(
            self.toolbar, text="Start Simulation", command=self._start_simulation
        )
        self.btn_start.grid(row=0, column=3, padx=6, pady=6, sticky="w")

        self.btn_clear = ctk.CTkButton(
            self.toolbar, text="Clear", command=self._clear_scene
        )
        self.btn_clear.grid(row=0, column=4, padx=6, pady=6, sticky="w")

        self.btn_clear = ctk.CTkButton(
            self.toolbar, text="Clear stations", command=self._clear_stations
        )
        self.btn_clear.grid(row=0, column=5, padx=6, pady=6, sticky="w")

        self.btn_clear = ctk.CTkButton(
            self.toolbar, text="Clear targets", command=self._clear_targets
        )
        self.btn_clear.grid(row=0, column=6, padx=6, pady=6, sticky="w")

        self.btn_edit = ctk.CTkButton(
        self.toolbar, text="Edit positions", command=self._open_edit_positions
        )
        self.btn_edit.grid(row=0, column=7, padx=6, pady=6, sticky="w")

        self.btn_edit = ctk.CTkButton(
        self.toolbar, text="Get stats", command=self._get_stats
        )
        self.btn_edit.grid(row=0, column=8, padx=6, pady=6, sticky="w")

  


    def _set_mode_triangle(self):
        self.mode = "triangle"
        self.log_panel.write("Mode: TRIANGLE placement. Click centroid in XY.")

    def _set_mode_station(self):
        self.mode = "station"
        self.log_panel.write("Mode: place STATION (click in XY).")

    def _set_mode_target(self):
        self.mode = "target"
        self.log_panel.write("Mode: place TARGET (click in XY).")

    def _clear_scene(self):
        self.scene.reset()
        self._station_id = 1
        self._target_id = 1
        self.log_panel.write("Scene cleared.")
        self._redraw_all()

    def _clear_stations(self):
        self.scene.reset_stations()
        self._station_id = 1
        self.log_panel.write("Stations cleared.")
        self._redraw_all()
    
    def _clear_targets(self):
        self.scene.reset_targets()
        self._target_id = 1
        self.log_panel.write("Targets cleared.")
        self._redraw_all()