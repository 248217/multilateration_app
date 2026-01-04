import customtkinter as ctk

class StatsConfigDialog(ctk.CTkToplevel):
    def __init__(self, parent, log_panel, default_runs="50"):
        super().__init__(parent)

        self.log_panel = log_panel
        self.result = None

        self.title("Get Stats")
        self.resizable(False, False)
        self.geometry("420x200")

        self.transient(parent)
        self.deiconify()
        self.lift()
        self.attributes("-topmost", True)
        self.after(50, lambda: self.attributes("-topmost", False))
        self.after(10, self.focus_force)

        self.grab_set()

        self.grid_columnconfigure(1, weight=1)

        self.test_var = ctk.StringVar()
        self.runs_var = ctk.StringVar(value=str(default_runs))
        self.ref_var  = ctk.StringVar()

        ctk.CTkLabel(self, text="Test name").grid(row=0, column=0, padx=12, pady=(12, 6), sticky="w")
        ctk.CTkEntry(self, textvariable=self.test_var).grid(row=0, column=1, padx=12, pady=(12, 6), sticky="ew")

        ctk.CTkLabel(self, text="Number of runs").grid(row=1, column=0, padx=12, pady=6, sticky="w")
        ctk.CTkEntry(self, textvariable=self.runs_var).grid(row=1, column=1, padx=12, pady=6, sticky="ew")

        ctk.CTkLabel(self, text="Reference station ID").grid(row=2, column=0, padx=12, pady=6, sticky="w")
        ctk.CTkEntry(self, textvariable=self.ref_var).grid(row=2, column=1, padx=12, pady=6, sticky="ew")

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.grid(row=3, column=0, columnspan=2, padx=12, pady=(10, 12), sticky="e")

        ctk.CTkButton(btns, text="Cancel", command=self._cancel).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btns, text="OK", command=self._ok).pack(side="right")

        self.bind("<Escape>", lambda e: self._cancel())
        self.bind("<Return>", lambda e: self._ok())

    def _ok(self):
        name = self.test_var.get().strip()
        if not name:
            self.log_panel.write("ERROR: Test name is required.")
            return

        try:
            runs = int(self.runs_var.get().strip())
            if runs <= 0:
                raise ValueError
        except ValueError:
            self.log_panel.write("ERROR: Number of runs must be a positive integer.")
            return

        try:
            ref_id = int(self.ref_var.get().strip())
        except ValueError:
            self.log_panel.write("ERROR: Reference station ID must be a number.")
            return

        self.result = (name, runs, ref_id)
        self.destroy()

    def _cancel(self):
        self.result = None
        self.destroy()



