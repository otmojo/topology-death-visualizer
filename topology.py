import numpy as np
from sklearn.neighbors import NearestNeighbors

class TopologyMetric:
    def __init__(self, X0, k=10):
        self.k = k
        self.X0 = X0
        nbrs = NearestNeighbors(n_neighbors=k + 1).fit(X0)
        _, self.ref_knn = nbrs.kneighbors(X0)
        self.ref_knn = self.ref_knn[:, 1:]
        
        # Build Reference Edge List (for visualization and stress)
        # Undirected graph: store (min(i,j), max(i,j)) to avoid dupes
        edges = set()
        for i, neighbors in enumerate(self.ref_knn):
            for n in neighbors:
                if i < n:
                    edges.add((i, n))
                else:
                    edges.add((n, i))
        self.edges = np.array(list(edges))

    def score(self, Z):
        nbrs = NearestNeighbors(n_neighbors=self.k + 1).fit(Z)
        _, knn = nbrs.kneighbors(Z)
        knn = knn[:, 1:]

        overlap = [
            len(set(a) & set(b)) / self.k
            for a, b in zip(self.ref_knn, knn)
        ]
        return np.mean(overlap), np.array(overlap)
    
    def get_edges(self):
        return self.edges

    def calculate_stress(self, Z):
        """
        Calculate topological stress (expansion/compression of edges).
        Returns the mean ratio of current edge lengths (2D) to original edge lengths (High-Dim).
        """
        # Current lengths in 2D
        p1_2d = Z[self.edges[:, 0]]
        p2_2d = Z[self.edges[:, 1]]
        d_2d = np.linalg.norm(p1_2d - p2_2d, axis=1)
        
        # Original lengths in High-Dim (computed once and cached would be better, but this is fast enough)
        p1_nd = self.X0[self.edges[:, 0]]
        p2_nd = self.X0[self.edges[:, 1]]
        d_nd = np.linalg.norm(p1_nd - p2_nd, axis=1)
        
        # Avoid division by zero
        d_nd[d_nd == 0] = 1e-9
        
        stress = d_2d / d_nd
        return np.mean(stress)


def predict_human_death_time(self, times, S_values,
                                 sensitivity=0.02,
                                 reaction_delay=3):
        """
        Humans perceive structural death through the rate of change of S(t).
        """
        for i in range(reaction_delay, len(times)):
            delta = abs(S_values[i] - S_values[i - reaction_delay])
            if delta > sensitivity:
                return times[i]
        return None
