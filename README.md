# Topology Death Visualizer

This project visualizes the concept of "Topological Death" — the moment when the underlying structure of high-dimensional data is lost during projection or transformation. It is designed as an experiment to compare human cognitive prediction of structural collapse against algorithmic detection.

<img src="https://github.com/otmojo/topology-death-visualizer/blob/main/Figure_1.png" alt="Image 1" width="900" />

<img src="https://github.com/otmojo/topology-death-visualizer/blob/main/Figure_2.png" alt="Image 2" width="900" />


## Experiment Design

The experiment simulates a high-dimensional ring structure undergoing deformation and projection.
1.  **Observe**: The user watches the structure deform in real-time.
2.  **Predict**: At a random time (`t=0.3s`), the screen freezes. The user must predict *when* the structure will "break" (lose its topological integrity) based on the observed trend.
3.  **Result**: The system resumes (in the background) to find the actual "death time" (`t_real`) and compares it with the user's prediction (`t_human`).

### Topological Metrics

*   **Score (KNN Overlap)**: Measures how many local neighbors in the original high-dimensional space remain neighbors in the 2D projection. A sharp drop indicates "Topological Death".
*   **Stress (Edge Compression)**: Measures the ratio of projected edge lengths to their original lengths. High stress variance indicates structural distortion.

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main experiment:

```bash
python main.py
```

### Controls
*   **Spacebar**: Press during `PREDICT` mode to lock in your prediction of the death time.

## Project Structure

*   `main.py`: The entry point and experiment controller (State Machine).
*   `topology.py`: Core logic for topological metrics (KNN Overlap, Stress).
*   `render.py`: Visualization engine (Matplotlib) drawing the projections and topological edges.
*   `death.py`: The algorithmic death detector.
*   `geometry.py`: High-dimensional geometric transformations (Rotation, Interpolation).
*   `experiment.py`: Data logging.

## License
MIT
