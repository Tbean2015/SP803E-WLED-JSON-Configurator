import json
import copy
import tkinter as tk
from tkinter import messagebox, filedialog

master_data = None


# ---------------- LOAD MASTER ----------------
def load_master():
    global master_data

    file_path = filedialog.askopenfilename(
        title="Select master_cfg.json",
        filetypes=[("JSON files", "*.json")]
    )

    if not file_path:
        return

    with open(file_path, "r") as f:
        master_data = json.load(f)

    messagebox.showinfo("Loaded", "Master config loaded successfully.")


# ---------------- GENERATE FILE ----------------
def generate_file():
    global master_data

    if master_data is None:
        messagebox.showerror("Error", "Load master_cfg.json first.")
        return

    try:
        # Inputs
        new_ip = [int(x) for x in entry_ip.get().split(".")]
        universe = int(entry_universe.get())
        start_channel = int(entry_dmx.get())

        new_cfg = copy.deepcopy(master_data)

        # --------------------
        # STATIC IP (your structure)
        # nw → ins[0] → ip
        # --------------------
        new_cfg["nw"]["ins"][0]["ip"] = new_ip

        # --------------------
        # DMX SETTINGS (your structure)
        # if → live → dmx
        # --------------------
        new_cfg["if"]["live"]["dmx"]["uni"] = universe
        new_cfg["if"]["live"]["dmx"]["addr"] = start_channel

        # Save dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=f"cfg_{entry_ip.get()}.json",
            filetypes=[("JSON files", "*.json")]
        )

        if not file_path:
            return

        with open(file_path, "w") as f:
            json.dump(new_cfg, f, indent=4)

        messagebox.showinfo("Success", "Config file created successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- UI ----------------
root = tk.Tk()
root.title("WLED Config Generator")
root.geometry("320x260")


tk.Button(root, text="Load Master Config", command=load_master).pack(pady=10)

tk.Label(root, text="New Static IP").pack()
entry_ip = tk.Entry(root)
entry_ip.pack()

tk.Label(root, text="Universe").pack()
entry_universe = tk.Entry(root)
entry_universe.pack()

tk.Label(root, text="DMX Start Address").pack()
entry_dmx = tk.Entry(root)
entry_dmx.pack()

tk.Button(root, text="Generate Config File", command=generate_file).pack(pady=15)

root.mainloop()
