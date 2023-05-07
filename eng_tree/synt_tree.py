from itertools import permutations, product

from nltk.tree import Tree


allowed_labels = {'NP', ',', 'CC'}
inp = '(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP(JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS restaurants) ) ) ) ) ) ) )'

class TreePermutations:
    """This class allows to:
    - Make a `Tree` object from string. Available by `tree` attribute.
    - Find all the subtree positions for a required label. Available by
    `ids` attribute.
    - Make permutations for all subtrees. Available by `sub_paraphrases`
    attribute.
    - Make a list of all possible paraphrases by inputed parameters.
    Available by `paraphrases` attribute.
    """

    ids = None
    sub_paraphrases = None
    paraphrases = None

    def __init__(
            self, in_tree: str, parented_label: str,
            allowed_nested_labels: set[str]) -> None:
        self.tree = self.make_tree(in_tree)
        self.parented_label = parented_label
        self.allowed_labels = allowed_nested_labels

        if self.tree:
            self.ids = self.get_positions()
            self.sub_paraphrases = [
                self.permute_values(self.tree[match]) for match in self.ids
            ]
            self.paraphrases = self.generate_trees(self.sub_paraphrases,
                                                   self.ids)


    def make_tree(self, in_tree: str) -> Tree|None:
        """Make a `Tree` object from an input string.
        Return a `Tree` object or `None`.
        """

        try:
            main_tree = Tree.fromstring(in_tree)
        except ValueError:
            main_tree = None

        return main_tree


    def get_positions(
            self, main_tree: Tree = None, sample: set[str] = None,
            req_label: str = None) -> list[tuple[int]]:
        """Find all the subtrees with the required label that match a
        sample.
        Return a list of positions for the subtrees needed.
        """

        if not main_tree:
            main_tree = self.tree
        if not sample:
            sample = self.allowed_labels
        if not req_label:
            req_label = self.parented_label

        req_positions = []
        for pos in main_tree.treepositions():
            subtree = main_tree[pos]
            if isinstance(subtree, Tree) and subtree.label() == req_label:
                labels = set(node.label() for node in subtree if isinstance(node, Tree))
                if len(labels) > 1 and not labels - sample:
                    req_positions.append(pos)

        return req_positions


    def permute_values(
            self, nodes: Tree, req_label: str = None) -> list[Tree]:
        """Get all the required labels and their indices.
        Return a list of subtree permutations.
        """

        if not req_label:
            req_label = self.parented_label

        required, idxs = [], []
        for node in nodes:
            if node.label() == req_label:
                required.append(node)
                idxs.append(nodes.index(node))

        # make permutations and create tuples with indices for each variant
        perms = [zip(idxs, perm) for perm in permutations(required)]

        # get a list of complete subtrees using the permutations results
        tree_perms = []
        for perm in perms:
            var = nodes.copy()
            for idx, value in perm:
                var[idx] = value
            tree_perms.append(var)

        return tree_perms


    def generate_trees(
            self, subtrees: list[list[Tree]], positions: list[tuple[int]],
            main_tree: Tree = None) -> list[Tree]:
        """Make a list of all possible complete trees using permuted
        subtrees and their positions in the main tree.
        Return the list of `Tree` objects.
        """

        if not main_tree:
            main_tree = self.tree

        # combine all the subtrees
        perm_combinations = product(*subtrees)

        whole_trees = []
        # fill a list with copies of the main tree and replace the subtrees
        # that should be permuted with their combined versions
        for perm in perm_combinations:
            result = main_tree.copy(deep=True)
            for i, index in enumerate(positions):
                result[index] = perm[i]
            whole_trees.append({'tree': result})

        return whole_trees[1:]
