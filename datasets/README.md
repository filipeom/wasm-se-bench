# Datasets

To compare symbolic execution tools, we use a custom-made Wasm implementation
of a B-tree data structure inspired by that of [cite].
This data structure allows us to effectively test the scalability of engines
with respect to code size ($\approx$ 4000 LoC) and the complexity of the
generated formulas.

## B-tree Implementation

B-trees are $n$-ary self-balancing trees typically used in the implementation
of storage systems. B-trees have a fixed branching factor $d$, denoting the
maximum number of children that internal nodes may have.
B-tree nodes store at most $d{-}1$ keys; internal nodes additionally store
the pointers to their respective children. Intuitively, it is as if each
internal node stores one key in between each two consecutive child pointers.
The keys stored inside a B-tree are arranged so that: **(1)** the keys of
every node are ordered; and **(2)** each key $k_i$ stored in between the
pointers $p_i$ and $p_{i+1}$ of an internal node is greater than all the
keys stored in the node pointed to by $p_i$ and less than those stored in
the one pointed to by $p_{i+1}$. B-trees must additionally satisfy various
other invariants. Figure [missing ref] shows a B-tree with branching factor $d = 4$.
The tree contains one internal node (Node $1$) and four leaf nodes (Nodes $2$
to $5$), with the internal node storing three keys. Observe that, for instance,
the second key stored in Node 1 (key $3$) is greater than the single key
stored in Node 3 (key $2$) and less than both keys stored in Node 4 (keys $4$
and $5$).

Our B-tree implementation in Wasm follows the one described by [cite], only
holding 32-bit integer keys. Each B-tree node is kept in a separate memory
page according to the memory layout given in Figure [missing ref].
Each memory page stores:

1. a flag $b$, indicating if it represents a leaf node;
2. an integer $n$, denoting the number of keys that the node holds; and
3. $n$ keys,  $k_1, \dotsc, k_n$.

Additionally, each internal node stores $n{+}1$ child pointers, $p_1, \dotsc, p_{n{+}1}$.
We use an extra memory page for keeping metadata information about the B-tree,
namely: its branching factor $d$, number of nodes $n_\mathit{nodes}$, and
address of the root node $a_\mathit{root}$.

Figure [missing ref] shows the memory layout of the first three nodes of the
B-tree presented in Figure [missing ref] together with the extra memory page
used to store its meta-information.

Our B-tree implementation comes with four main functions:

1. `$createBTree(d)` for creating an empty B-tree with the specified degree;
2. `$insertBTree(t, k)` for inserting the key $k$ into the tree $t$;
3. `$searchBTree(t, k)` for checking if the tree $t$ holds the key $k$; and
4. `$deleteBTree(t, k)` for deleting the key $k$ from the tree $t$.

## Experimental Setup

In order to compare the performance of the tools, we created a
symbolic test suite. All symbolic tests follow  the same code
template but use a varying number of symbolic values, of which
some are constrained to be ordered. In the following, we use $n_o$
and $n_u$ to denote respectively the number of ordered and unordered
symbolic values used in each test.

| Number of ordered ($n_o$) | Number of paths for $n_u = 1$ | Number of paths for $n_u = 2$ | Number of paths for $n_u = 3$ |
|--------------------------:|------------------------------:|------------------------------:|------------------------------:|
| 2 |  3 |  12 |  60 |
| 3 |  4 |  20 | 120 |
| 4 |  5 |  30 | 210 |
| 5 |  6 |  42 | 336 |
| 6 |  7 |  56 | 506 |
| 7 |  8 |  72 | 720 |
| 8 |  9 |  91 |  -- |
| 9 | 10 | 110 |  -- |
