import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

class Renderer:
    def __init__(self):
        # Setup 3 subplots for the 3 projections
        self.fig, self.axes = plt.subplots(1, 3, figsize=(15, 5))
        titles = ["Orthogonal", "Linear", "Linear + Norm"]
        # Set dark theme
        self.fig.patch.set_facecolor('black')
        
        for ax, t in zip(self.axes, titles):
            ax.set_title(t, color='white')
            ax.set_aspect("equal")
            ax.axis("off")
            ax.set_facecolor('black')

    def draw(self, projections, colors, edges=None, death_detected=False, mode="OBSERVE", show_too_late=False, stats=None):
        # projections: list of 3 arrays
        # colors: list of 3 arrays
        
        # Visual Constants
        bg_color = 'black'
        text_color = 'white'
        point_color = 'cyan'
        
        if death_detected:
            point_color = 'gray'
            text_color = 'red'
        elif mode == "PREDICT":
            point_color = 'yellow' # Highlight predict mode
            
        titles = ["Orthogonal", "Linear", "Linear + Norm"]
        if stats:
             titles[2] += f"\nScore: {stats.get('score',0):.2f} | Stress: {stats.get('stress',0):.2f}"

        for i, (ax, Z, c) in enumerate(zip(self.axes, projections, colors)):
            ax.clear()
            ax.set_aspect("equal")
            ax.axis("off")
            ax.set_facecolor(bg_color)
            ax.set_title(titles[i], color=text_color)
            
            # 1. Draw Topology Edges (The "Structure")
            if edges is not None:
                # edges is (N_edges, 2) indices
                start_points = Z[edges[:, 0]]
                end_points = Z[edges[:, 1]]
                segments = np.stack((start_points, end_points), axis=1)
                
                # Style
                edge_color = 'white'
                edge_alpha = 0.15
                edge_width = 0.5
                
                if death_detected:
                     edge_color = 'red' # Show the broken mesh
                     edge_alpha = 0.4
                     edge_width = 0.8
                elif mode == "PREDICT":
                    edge_color = 'yellow'
                    edge_alpha = 0.3
                
                lc = LineCollection(segments, colors=edge_color, alpha=edge_alpha, linewidths=edge_width)
                ax.add_collection(lc)

            # 2. Draw Points (The "Data")
            ax.scatter(Z[:, 0], Z[:, 1], c=point_color, s=15, alpha=0.9, edgecolors='none')
            
            # 3. Death Effects
            if death_detected:
                # Red Border
                rect = plt.Rectangle(
                    (ax.get_xlim()[0], ax.get_ylim()[0]),
                    ax.get_xlim()[1] - ax.get_xlim()[0],
                    ax.get_ylim()[1] - ax.get_ylim()[0],
                    linewidth=3, edgecolor='red', facecolor='none'
                )
                ax.add_patch(rect)
                
                # Text on the middle plot
                if i == 1:
                     ax.text(0, 0, "STRUCTURE LOST", color='red', fontsize=18, 
                             ha='center', va='center', fontweight='bold', 
                             bbox=dict(facecolor='black', edgecolor='red', alpha=0.8))

        # 4. Global Overlays
        if show_too_late:
             # Show on the rightmost plot or center
             self.axes[2].text(0, 0, "HUMAN TOO LATE", color='red', fontsize=16, 
                               ha='center', va='center', fontweight='bold', 
                               bbox=dict(facecolor='black', edgecolor='red'))

        plt.pause(0.001)
