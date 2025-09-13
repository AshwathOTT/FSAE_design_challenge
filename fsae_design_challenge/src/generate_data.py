# src/generate_data.py
import argparse, numpy as np, pandas as pd
import math
from utils import moving_avg, clamp, sigmoid
import config as C

def build_timebase(duration_s, fs_hz):
    return np.arange(int(duration_s * fs_hz)) / fs_hz

def synth_vehicle_speed(t):
    v = 18.0 + 2.5*np.sin(2*math.pi*t/20.0)
    for (t0, t1) in [(8.0, 10.0), (20.0, 22.5), (34.0, 37.0)]:
        mask = (t >= t0) & (t <= t1)
        tau = (t[mask] - t0) / (t1 - t0 + 1e-6)
        decel = 7.0 * (1 - np.cos(math.pi * clamp(tau, 0, 1))) / 2.0
        v[mask] -= decel
    v = np.clip(v, 2.0, None) + np.random.normal(0, 0.05, size=v.shape)
    return moving_avg(v, 5)

def synth_pressure(t):
    p = np.zeros_like(t)
    for (t0, t1) in [(7.8, 10.2), (19.7, 22.7), (33.5, 37.2)]:
        mask = (t >= t0) & (t <= t1)
        tau = (t[mask] - t0) / (t1 - t0 + 1e-6)
        shape = np.sin(math.pi * clamp(tau, 0, 1))
        peak = np.random.uniform(950, 1300)
        p[mask] = peak * shape
    p += np.random.normal(0, C.PRESSURE_BASE_NOISE_PSI, size=p.shape)
    p = np.clip(p, 0, None)
    spike = (t >= C.PRESSURE_SPIKE_TIME_S) & (t <= C.PRESSURE_SPIKE_TIME_S + C.PRESSURE_SPIKE_LEN_S)
    p[spike] += C.PRESSURE_SPIKE_PSI
    return p

def slip_from_pressure(p_wheel, is_front=True):
    thresh = C.LOCK_THRESH_FRONT_PSI if is_front else C.LOCK_THRESH_REAR_PSI
    z = (p_wheel - thresh) / 110.0
    s = sigmoid(z)
    s *= clamp(p_wheel / (0.5*thresh + 1e-6), 0, 1.2)
    return clamp(s, 0.0, 0.98)

def synth_wheel_speeds(t, v, p_front, p_rear):
    wspd, slips = {}, {}
    for w in ["FL", "FR", "RL", "RR"]:
        is_front = w.startswith("F")
        p = p_front if is_front else p_rear
        s = slip_from_pressure(p, is_front) + np.random.normal(0, 0.03, size=p.shape)
        s = clamp(s * C.WHEEL_FACTOR[w], 0.0, 0.98)
        wsp = v * (1 - s) + np.random.normal(0, 0.08, size=v.shape)
        wspd[w], slips[w] = np.maximum(wsp, 0.0), s

    # dropout
    m = (t >= C.DROPOUT_START_S) & (t <= C.DROPOUT_START_S + C.DROPOUT_LEN_S)
    wspd[C.DROPOUT_WHEEL][m] = np.nan

    return wspd, slips

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="data/session.csv")
    args = ap.parse_args()

    t = build_timebase(C.DURATION_S, C.FS_HZ)
    v = synth_vehicle_speed(t)
    p_line = synth_pressure(t)
    bias = C.FRONT_BIAS_MEAN + np.random.normal(0, C.FRONT_BIAS_JITTER, size=t.shape)
    p_front, p_rear = p_line * bias, p_line * (1 - bias)
    wspd, slips = synth_wheel_speeds(t, v, p_front, p_rear)

    df = pd.DataFrame({
        "t_s": t, "veh_speed_mps": v,
        "brake_pressure_psi": p_line,
        "wheel_FL_mps": wspd["FL"], "wheel_FR_mps": wspd["FR"],
        "wheel_RL_mps": wspd["RL"], "wheel_RR_mps": wspd["RR"],
        "slip_FL": slips["FL"], "slip_FR": slips["FR"],
        "slip_RL": slips["RL"], "slip_RR": slips["RR"],
    })
    df.to_csv(args.out, index=False)
    print(f"Saved dataset to {args.out}")

if __name__ == "__main__":
    main()
