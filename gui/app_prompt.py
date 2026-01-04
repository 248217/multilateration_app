import customtkinter as ctk
from gui.app_statsConfigDiag import StatsConfigDialog

class AppPromptMixin:
    def _prompt_triangle_vertex_zs(self):
        zs = []
        for i in range(1, 4):
            z = self._prompt_z(f" (triangle vertex {i})")
            if z is None:
                return None
            zs.append(z)
        return zs

    def _prompt_z(self, id):
        dialog = ctk.CTkInputDialog(text=f"Enter station{id} Z coordinate:", title="Z value")
        raw = dialog.get_input()
        if raw is None:
            return None
        raw = raw.strip()
        if raw == "":
            return None
        try:
            return float(raw)
        except ValueError:
            self.log_panel.write("ERROR: Z must be a number.")
            return None
        
    def _prompt_reference_station(self):
        dialog = ctk.CTkInputDialog(text=f"Enter reference station ID:", title="Reference Station")
        raw = dialog.get_input()
        if raw is None:
            return None
        raw = raw.strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            self.log_panel.write("ERROR: Reference station ID must be a number.")
            return None
        

    def _prompt_stats_config(self):
        parent = self.winfo_toplevel() if hasattr(self, "winfo_toplevel") else self.root

        dlg = StatsConfigDialog(parent, self.log_panel, default_runs="50")
        parent.wait_window(dlg)
        return dlg.result
