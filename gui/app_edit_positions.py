import customtkinter as ctk

class EditPositionsMixin:
    def _open_edit_positions(self):
        win = ctk.CTkToplevel(self)
        win.title("Edit positions")
        win.geometry("420x260")
        win.transient(self)
        win.grab_set()

        def get_entities(kind: str):
            return self.scene.get_stations() if kind == "Station" else self.scene.get_targets()

        def get_entity_by_id(kind: str, entity_id: int):
            for e in get_entities(kind):
                if e.id == entity_id:
                    return e
            return None

        kind_var = ctk.StringVar(value="Station")
        id_var = ctk.StringVar(value="")
        x_var = ctk.StringVar(value="")
        y_var = ctk.StringVar(value="")
        z_var = ctk.StringVar(value="")

        # --- UI layout ---
        frm = ctk.CTkFrame(win)
        frm.pack(fill="both", expand=True, padx=12, pady=12)
        frm.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frm, text="Type").grid(row=0, column=0, sticky="w", pady=4)
        kind_menu = ctk.CTkOptionMenu(frm, variable=kind_var, values=["Station", "Target"])
        kind_menu.grid(row=0, column=1, sticky="ew", pady=4)

        ctk.CTkLabel(frm, text="ID").grid(row=1, column=0, sticky="w", pady=4)
        id_menu = ctk.CTkOptionMenu(frm, variable=id_var, values=[""])
        id_menu.grid(row=1, column=1, sticky="ew", pady=4)

        ctk.CTkLabel(frm, text="X").grid(row=2, column=0, sticky="w", pady=4)
        x_entry = ctk.CTkEntry(frm, textvariable=x_var)
        x_entry.grid(row=2, column=1, sticky="ew", pady=4)

        ctk.CTkLabel(frm, text="Y").grid(row=3, column=0, sticky="w", pady=4)
        y_entry = ctk.CTkEntry(frm, textvariable=y_var)
        y_entry.grid(row=3, column=1, sticky="ew", pady=4)

        ctk.CTkLabel(frm, text="Z").grid(row=4, column=0, sticky="w", pady=4)
        z_entry = ctk.CTkEntry(frm, textvariable=z_var)
        z_entry.grid(row=4, column=1, sticky="ew", pady=4)

        btn_row = ctk.CTkFrame(frm, fg_color="transparent")
        btn_row.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        btn_row.grid_columnconfigure((0, 1, 2), weight=1)

        def refresh_id_list(*_):
            entities = get_entities(kind_var.get())
            ids = [str(e.id) for e in entities]
            if not ids:
                ids = [""]
            id_menu.configure(values=ids)
            id_var.set(ids[0])
            load_selected()

        def load_selected(*_):
            if not id_var.get().strip():
                x_var.set(""); y_var.set(""); z_var.set("")
                return
            e = get_entity_by_id(kind_var.get(), int(id_var.get()))
            if e is None:
                x_var.set(""); y_var.set(""); z_var.set("")
                return
            x, y, z = e.get_position()
            x_var.set(str(x))
            y_var.set(str(y))
            z_var.set(str(z))

        def apply_changes():
            if not id_var.get().strip():
                self.log_panel.write("ERROR: No entity selected.")
                return
            try:
                x = float(x_var.get()); y = float(y_var.get()); z = float(z_var.get())
            except ValueError:
                self.log_panel.write("ERROR: X/Y/Z must be numbers.")
                return

            e = get_entity_by_id(kind_var.get(), int(id_var.get()))
            if e is None:
                self.log_panel.write("ERROR: Entity not found.")
                return

            if hasattr(e, "set_position") and callable(getattr(e, "set_position")):
                e.set_position((x, y, z))
            else:
                if hasattr(e, "_pos"):
                    e._pos = (x, y, z)
                elif hasattr(e, "pos"):
                    e.pos = (x, y, z)
                else:
                    self.log_panel.write("ERROR: No way to set position on this object.")
                    return

            self.log_panel.write(f"Updated {kind_var.get()} {e.id}: ({x:.2f}, {y:.2f}, {z:.2f})")
            self._redraw_all()

        def delete_selected():
            if not id_var.get().strip():
                return
            e = get_entity_by_id(kind_var.get(), int(id_var.get()))
            if e is None:
                return

            removed = False
            if kind_var.get() == "Station" and hasattr(self.scene, "remove_station"):
                self.scene.remove_station(e.id); removed = True
            elif kind_var.get() == "Target" and hasattr(self.scene, "remove_target"):
                self.scene.remove_target(e.id); removed = True

            if removed:
                self.log_panel.write(f"Removed {kind_var.get()} {e.id}")
                refresh_id_list()
                self._redraw_all()
            else:
                self.log_panel.write("ERROR: Scene has no remove_station/remove_target methods.")

        ctk.CTkButton(btn_row, text="Apply", command=apply_changes).grid(row=0, column=0, padx=4, sticky="ew")
        ctk.CTkButton(btn_row, text="Delete", command=delete_selected).grid(row=0, column=1, padx=4, sticky="ew")
        ctk.CTkButton(btn_row, text="Close", command=win.destroy).grid(row=0, column=2, padx=4, sticky="ew")

        kind_var.trace_add("write", refresh_id_list)
        id_var.trace_add("write", load_selected)

        refresh_id_list()
