import numpy as np
import matplotlib.pyplot as plt
from topology import TopologyMetric
from geometry import OrthogonalRotation
from projection import FixedProjection
from data import make_ring

def test_stress_rotation():
    # Setup
    X0 = make_ring()
    dim = X0.shape[1]
    
    topology = TopologyMetric(X0, k=5)
    rotator = OrthogonalRotation(dim)
    projector = FixedProjection(dim)
    
    t_values = np.linspace(0, 2, 50)
    stresses = []
    scores = []
    
    print("Simulating rotation...")
    for t in t_values:
        # Rotate without deforming
        Y = rotator.step(X0, t)
        # Project
        Z = projector.project(Y)
        
        # Calculate metrics
        stress = topology.calculate_stress(Z)
        s_score, _ = topology.score(Z)
        
        stresses.append(stress)
        scores.append(s_score)
        
    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(t_values, stresses, label='Stress (Length Ratio)', color='red')
    plt.plot(t_values, scores, label='Score (KNN Overlap)', color='blue')
    plt.title("Metric Stability under Rigid Rotation")
    plt.xlabel("Time")
    plt.legend()
    plt.grid(True)
    plt.savefig("stress_test.png")
    print("Test complete. Saved stress_test.png")
    
    print(f"Stress Variation: {np.min(stresses):.3f} - {np.max(stresses):.3f}")
    print(f"Score Variation: {np.min(scores):.3f} - {np.max(scores):.3f}")

if __name__ == "__main__":
    test_stress_rotation()