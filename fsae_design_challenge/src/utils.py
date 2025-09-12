# src/utils.py
import numpy as np

def moving_avg(x, w=9):
    if w <= 1: return x
    pad = w // 2
    xpad = np.pad(x, (pad, pad), mode="edge")
    kernel = np.ones(w) / w
    return np.convolve(xpad, kernel, mode="valid")

def clamp(x, lo, hi):
    return np.minimum(np.maximum(x, lo), hi)

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))