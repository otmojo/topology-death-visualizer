import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

df = df.dropna(subset=["delta_t"])

plt.figure(figsize=(6, 4))
plt.hist(df["delta_t"], bins=15, edgecolor="black")
plt.axvline(0, color="red", linestyle="--", label="t_real")
plt.xlabel("Δt = t_real - t_human")
plt.ylabel("Count")
plt.title("Human Prediction of Topological Death")
plt.legend()
plt.tight_layout()
plt.show()

print("Mean Δt :", df["delta_t"].mean())
print("Median Δt :", df["delta_t"].median())
