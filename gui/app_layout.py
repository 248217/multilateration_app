import customtkinter as ctk
from gui.canvas_views import XYView, XZView, YZView
from gui.log_panel import LogPanel


class LayoutMixin:
    def _configure_window(self):
        self.title("Multilateration Simulator")
        self.geometry("1200x800")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

    def _build_main_layout(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)

        self.main_frame.grid_columnconfigure(0, weight=2)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.xy_box = ctk.CTkFrame(self.main_frame)
        self.xy_box.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        self.side_box = ctk.CTkFrame(self.main_frame)
        self.side_box.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        self.side_box.grid_rowconfigure(0, weight=1)
        self.side_box.grid_rowconfigure(1, weight=1)

    def _build_views(self):
        self.xy_view = XYView(self.xy_box)
        self.xy_view.pack(fill="both", expand=True, padx=6, pady=6)

        self.xz_view = XZView(self.side_box)
        self.xz_view.pack(fill="both", expand=True, padx=6, pady=(6, 3))

        self.yz_view = YZView(self.side_box)
        self.yz_view.pack(fill="both", expand=True, padx=6, pady=(3, 6))

    def _build_log_panel(self):
        self.log_panel = LogPanel(self)
        self.log_panel.grid(row=2, column=0, sticky="nsew", padx=8, pady=(4, 8))
