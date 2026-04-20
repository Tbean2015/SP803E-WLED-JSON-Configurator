import json
import copy
import csv
import os
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


# ---------------- GENERATE FROM CSV ----------------
def generate_from_csv():
    global master_data

    if master_data is None:
        messagebox.showerror("Error", "Load master_cfg.json first.")
        return

    # Select CSV
    csv_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv")]
    )

    if not csv_path:
        return

    # Select output folder
    output_folder = filedialog.askdirectory(title="Select Output Folder")

    if not output_folder:
        return

    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            count = 0

            for row in reader:
                try:
                    # Safely extract fields (handles messy CSVs)
                    ip_str = row.get("IP ADDRESS")
                    universe = row.get("Universe")
                    start_channel = row.get("DMX")

                    if not ip_str or universe is None or start_channel is None:
                        continue  # skip invalid rows

                    universe = int(universe)
                    start_channel = int(start_channel)

                    # Convert IP string to list
                    new_ip = [int(x) for x in ip_str.split(".")]

                    # Copy master config
                    new_cfg = copy.deepcopy(master_data)

                    # Set IP
                    new_cfg["nw"]["ins"][0]["ip"] = new_ip

                    # Set DMX values
                    new_cfg["if"]["live"]["dmx"]["uni"] = universe
                    new_cfg["if"]["live"]["dmx"]["addr"] = start_channel

                    # -------------------------------
                    # Universe-based folder structure
                    # -------------------------------
                    universe_folder = os.path.join(output_folder, f"universe_{universe}")
                    os.makedirs(universe_folder, exist_ok=True)

                    # Output filename
                    filename = f"cfg_{ip_str.replace('.', '_')}.json"
                    file_path = os.path.join(universe_folder, filename)

                    # Save JSON file
                    with open(file_path, "w") as f:
                        json.dump(new_cfg, f, indent=4)

                    count += 1

                except Exception as e:
                    print(f"Skipping row due to error: {e}")
                    continue

        messagebox.showinfo("Success", f"{count} config files generated.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- UI ----------------
root = tk.Tk()
root.title("WLED Config Generator")
root.geometry("320x200")

tk.Button(root, text="Load Master Config", command=load_master).pack(pady=10)

tk.Button(root, text="Generate from CSV", command=generate_from_csv).pack(pady=20)

root.mainloop()
