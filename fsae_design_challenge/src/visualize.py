# src/visualize.py
import argparse, pandas as pd, numpy as np, matplotlib.pyplot as plt
import config as C

def plot_heatmap(df, out_dir=None):
    wheels = ["FL", "FR", "RL", "RR"]


    # Stack slip arrays into a 2D matrix
    m = np.vstack([df[f"slip_{w}"].to_numpy() for w in wheels])

    plt.figure(figsize=(10, 4))
    plt.imshow(
        m,
        aspect="auto",
        interpolation="nearest",
        extent=(float(df["t_s"].iloc[0]), float(df["t_s"].iloc[-1]), 0.0, float(len(wheels))),
        cmap="inferno"
    )
    plt.yticks(np.arange(0.5, len(wheels) + 0.5), wheels)
    plt.colorbar(label="Slip Ratio (0–1)")
    plt.title("Slip Heatmap (time × wheel)")
    plt.xlabel("Time (s)")
    plt.show()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--infile", type=str, required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.infile)
    plot_heatmap(df)

if __name__ == "__main__":
    main()