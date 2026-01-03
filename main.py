import numpy as np
import matplotlib.pyplot as plt
import time

from data import make_ring
from geometry import OrthogonalRotation, LinearInterpolation, LinearInterpNormalized
from projection import FixedProjection
from topology import TopologyMetric
from death import DeathDetector, HumanPrediction
from render import Renderer
from experiment import ExperimentLogger

# ==========================================
# EXPERIMENT CONFIGURATION
# ==========================================
MAX_WAIT = 3.0  # Seconds to wait for prediction
PREDICTION_START_T = 0.3 # Simulation time to start prediction mode
DT = 0.005 # Simulation time step per frame

# ==========================================
# SETUP
# ==========================================
X0 = make_ring()
dim = X0.shape[1]

transforms = [
    OrthogonalRotation(dim),
    LinearInterpolation(dim),
    LinearInterpNormalized(dim)
]

projector = FixedProjection(dim)
topology = TopologyMetric(X0)
detector = DeathDetector()
renderer = Renderer()
logger = ExperimentLogger()

# State Machine Variables
STATE_OBSERVE = "OBSERVE"
STATE_PREDICT = "PREDICT"
STATE_DEAD = "DEAD"
STATE_DONE = "DONE" # Used when prediction is finished but death hasn't happened yet

mode = STATE_OBSERVE
t_human = None
death_detected = False
prediction_prompt_time = 0.0

# Render State (Decoupled from Simulation)
render_projections = None
render_colors = None
frozen_projections = None
frozen_colors = None

# Input Handling
user_pressed_space = False
def on_key(event):
    global user_pressed_space
    if event.key == " ":
        user_pressed_space = True

plt.gcf().canvas.mpl_connect("key_press_event", on_key)

# Prepare edges for visualization
edges = topology.get_edges()

# ==========================================
# MAIN LOOP
# ==========================================
t = 0.0
print("Experiment Started. Mode: OBSERVE")

while True:
    # -----------------------------
    # 1. Physics & Algorithm (ALWAYS RUNNING)
    # -----------------------------
    t += DT
    
    current_projections = []
    current_colors = []
    
    for tf in transforms:
        Y = tf.step(X0, t)
        Z = projector.project(Y)
        current_projections.append(Z)

    S, local = topology.score(current_projections[2]) # Score based on Linear+Norm
    stress = topology.calculate_stress(current_projections[2]) # Calculate stress for Linear+Norm
    
    # Update Death Detector (ALWAYS RUNNING)
    detector.update(t, S)
    
    # Prepare current colors
    for _ in range(3):
        current_colors.append(local)

    # -----------------------------
    # 2. State Machine Logic (Strict Priority)
    # -----------------------------
    
    # PRIORITY 1: DEATH (Highest)
    if detector.dead:
        if not detector.reported:
            print(f"[DEATH] detected at t={detector.t_death:.3f}")
            detector.reported = True
            death_detected = True
        
        mode = STATE_DEAD
    
    # PRIORITY 2: Transition OBSERVE -> PREDICT
    elif mode == STATE_OBSERVE and t > PREDICTION_START_T:
        mode = STATE_PREDICT
        prediction_prompt_time = time.time()
        # Capture state for freezing
        frozen_projections = current_projections
        frozen_colors = current_colors
        print(f"[SYSTEM] Entered PREDICT mode at t={t:.3f}. Screen Frozen.")
        
    # PRIORITY 3: Handle PREDICT Mode
    elif mode == STATE_PREDICT:
        # Check User Input
        if user_pressed_space:
            user_pressed_space = False
            t_human = t
            mode = STATE_DONE
            print(f"[HUMAN] Predicted at t={t:.3f}")
        
        # Check Timeout
        elif time.time() - prediction_prompt_time > MAX_WAIT:
            t_human = float('inf')
            mode = STATE_DONE
            print("[HUMAN] Timed out (inf)")

    # -----------------------------
    # 3. Rendering Logic (Decoupled)
    # -----------------------------
    
    # Decision: What to show?
    show_too_late = False
    
    if mode == STATE_PREDICT:
        # Show FROZEN state (Past)
        if frozen_projections is not None:
            render_projections = frozen_projections
            render_colors = frozen_colors
    else:
        # Show CURRENT state (Present)
        # This handles OBSERVE, DONE, and DEAD
        render_projections = current_projections
        render_colors = current_colors
        
        # Determine if we should show TOO LATE warning during render
        # Only show if dead, and human hasn't predicted yet (or is too late)
        # Note: t_human is only set if mode is DONE. If mode is DEAD, t_human might be None.
        if mode == STATE_DEAD:
            # If we are in DEAD state, it means we died.
            # Did human predict?
            if t_human is None or (t_human >= detector.t_death):
                 show_too_late = True
            
    # Draw
    renderer.draw(
        render_projections, 
        render_colors,
        edges=edges,
        death_detected=death_detected, 
        mode=mode,
        show_too_late=show_too_late,
        stats={"score": S, "stress": stress}
    )
    
    plt.pause(0.01) # Small pause for GUI events
    
    # -----------------------------
    # 4. Exit Condition
    # -----------------------------
    # Safety timeout
    if t > 2.0:
        break

plt.show(block=True)

# ==========================================
# RESULT LOGGING
# ==========================================
print("\n==== RESULT ====")
print(f"t_real   : {detector.t_death}")
print(f"t_human  : {t_human}")

if t_human is None:
    t_human = float('inf')
    
# Logic for HUMAN TOO LATE or NO DEATH
# 1. No Death Observed
if detector.t_death is None:
    print("[SYSTEM] NO DEATH OBSERVED")

# 2. Death Observed
else:
    # 2a. Human too late (or never predicted)
    if t_human == float('inf') or t_human >= detector.t_death:
        print("[SYSTEM] HUMAN TOO LATE")
    
    # 2b. Human anticipated death
    else:
        print("[SYSTEM] HUMAN ANTICIPATED DEATH")
        print(f"Δt       : {detector.t_death - t_human:.3f}")

logger.log(
    mode="Linear+Norm",
    t_real=detector.t_death,
    t_human=t_human
)
