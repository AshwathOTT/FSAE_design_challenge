# src/config.py

DURATION_S = 45.0      # seconds
FS_HZ = 200            # sampling rate
WHEEL_RADIUS_M = 0.235 # ~ 18 inch tires

# Brake pressure range (psi)
PRESSURE_BASE_NOISE_PSI = 8.0
PRESSURE_SPIKE_PSI = 300.0      # simulates a sudden spike or anomaly
PRESSURE_SPIKE_TIME_S = 28.4
PRESSURE_SPIKE_LEN_S = 0.06

# Brake bias
FRONT_BIAS_MEAN = 0.65
FRONT_BIAS_JITTER = 0.02        # simulates random variations in bias

# Slip thresholds
SLIP_WARN = 0.20        # at this point, tire is around peak friction
SLIP_LOCK = 0.85        # beyond this, wheel will start to lock up and skid

# Lock pressures (psi)
LOCK_THRESH_FRONT_PSI = 1150.0         # this pressure is when front wheels will tend to lock up
LOCK_THRESH_REAR_PSI = 950.0           # this pressure is when rear wheels will tend to lock up

# Wheel load factors; random loads to add variance between wheels during simulations
WHEEL_FACTOR = {
    "FL": 1.00,
    "FR": 0.97,
    "RL": 1.05,
    "RR": 1.02,
}

# Sensor dropout
DROPOUT_WHEEL = "FR"
DROPOUT_START_S = 12.7
DROPOUT_LEN_S = 0.12

# Plot resolution
SAVE_DPI = 140