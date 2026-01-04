import customtkinter as ctk
from simulation.scene import Scene

from gui.app_toolbar import ToolbarMixin
from gui.app_layout import LayoutMixin
from gui.app_events import EventsMixin
from gui.app_draw import DrawMixin
from gui.app_simulation import SimulationMixin
from gui.app_edit_positions import EditPositionsMixin
from gui.app_prompt import AppPromptMixin
from gui.app_stats import StatsMixin


class App(
    ToolbarMixin,
    LayoutMixin,
    EventsMixin,
    DrawMixin,
    SimulationMixin,
    EditPositionsMixin,
    AppPromptMixin,
    StatsMixin,
    ctk.CTk,
):
    def __init__(self):
        ctk.CTk.__init__(self)

        self.scene = Scene()
        self.mode = None
        self._station_id = 1
        self._target_id = 1
        self._triangle_centroid = None

        self._configure_window()
        self._build_toolbar()
        self._build_main_layout()
        self._build_views()
        self._build_log_panel()

        self._bind_events()
        self._redraw_all()
