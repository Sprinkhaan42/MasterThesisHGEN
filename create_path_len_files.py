import numpy as np
import pickle


class RandomWalker:
    """
    Helper class to generate random walks on the input adjacency matrix.
    """

    def __init__(self, adj, rw_len, p=1, q=1, batch_size=128):
        self.adj = adj
        # if not "lil" in str(type(adj)):
        #    warnings.warn("Input adjacency matrix not in lil format. Converting it to lil.")
        #    self.adj = self.adj.tolil()

        self.rw_len = rw_len
        self.p = p
        self.q = q
        self.edges = np.array(self.adj.nonzero()).T
        self.node_ixs = np.unique(self.edges[:, 0], return_index=True)[1]
        self.batch_size = batch_size

    def walk(self):
        while True:
            yield random_walk(self.edges, self.node_ixs, self.rw_len, self.p, self.q, self.batch_size).reshape(
                [-1, self.rw_len])


def random_walk(edges, node_ixs, rwlen, p=1, q=1, n_walks=1):
    N = len(node_ixs)

    walk = []
    prev_nbs = None
    for w in range(n_walks):
        source_node = np.random.choice(N)
        walk.append(source_node)
        for it in range(rwlen - 1):

            if walk[-1] == N - 1:
                nbs = edges[node_ixs[walk[-1]]::, 1]
            else:
                nbs = edges[node_ixs[walk[-1]]:node_ixs[walk[-1] + 1], 1]

            if it == 0:
                walk.append(np.random.choice(nbs))
                prev_nbs = set(nbs)
                continue

            is_dist_1 = []
            for n in nbs:
                is_dist_1.append(int(n in set(prev_nbs)))

            is_dist_1_np = np.array(is_dist_1)
            is_dist_0 = nbs == walk[-2]
            is_dist_2 = 1 - is_dist_1_np - is_dist_0

            alpha_pq = is_dist_0 / p + is_dist_1_np + is_dist_2 / q
            alpha_pq_norm = alpha_pq / np.sum(alpha_pq)
            rdm_num = np.random.rand()
            cumsum = np.cumsum(alpha_pq_norm)
            nxt = nbs[np.sum(1 - (cumsum > rdm_num))]
            walk.append(nxt)
            prev_nbs = set(nbs)
    return np.array(walk)


with open('Youshu/adj_matrix.p', 'rb') as f:
    var = pickle.load(f)
walker = RandomWalker(var, 2)
walk = walker.walk()

print("start loop")
for i in walk:
    with open('Youshu/path_len_2.p', 'wb') as g:
        pickle.dump(i, g)
        print("Dump" + "\n")


print('succes')
