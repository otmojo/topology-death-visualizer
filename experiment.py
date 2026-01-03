import csv
import time

class ExperimentLogger:
    def __init__(self, filename="results.csv"):
        self.filename = filename
        with open(self.filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "mode",
                "t_real",
                "t_human",
                "delta_t"
            ])

    def log(self, mode, t_real, t_human):
        delta = None
        if t_human is not None and t_real is not None:
            try:
                delta = t_real - t_human
            except:
                delta = "Error"
        
        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([mode, t_real, t_human, delta])
