from rest_framework.test import APITestCase

from nltk.tree import Tree

from ..views import ParaphraseListView


class TestParaphraseListView(APITestCase):
    """Checks that:
    - a view URL exists at desired location
    - an empty tree returns the error message
    - an invalid tree returns the error message
    - a tree without required labels returns an empty list
    - the result contains the correct amount of trees
    - the result contains the expected values
    - an invalid limit returns the error message
    - an invalid limit type returns the error message
    - a limit returns correct amount of trees
    """

    def setUp(self):
        self.location = '/paraphrase'
        self.status_code = 200

        self.param1 = '?tree='
        self.param2 = '&limit='

        self.valid_tree = '(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP(JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS restaurants) ) ) ) ) ) ) )'
        self.vt_length = 11
        self.tree_without_matches = '(S (DP (D the) (NP dog)) (VP (V chased) (DP (D the) (NP cat))))'
        self.twm_result = []
        self.invalid_tree = 'invalid tree'

        self.valid_limit = 5
        self.invalid_limit_type = 'limit'
        self.invalid_limit_number = 0

        self.errors = ParaphraseListView.errors

        self.example_output = (
            "(S (NP (NP (NNP Barri) (NNP Gòtic)) (, ,) (CC or) (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (NNS clubs)) (, ,) (NP (JJ trendy) (NNS bars)) (CC and) (NP (JJ Catalan) (NNS restaurants))))))))",
            "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (NNS clubs)) (, ,) (NP (JJ trendy) (NNS bars)) (CC and) (NP (JJ Catalan) (NNS restaurants))))))))",
            "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars)) (, ,) (NP (JJ Catalan) (NNS restaurants)) (CC and) (NP (NNS clubs))))))))",
            "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (JJ Catalan) (NNS restaurants)) (, ,) (NP (NNS clubs)) (CC and) (NP (JJ trendy) (NNS bars))))))))",
            "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (NNS clubs)) (, ,) (NP (JJ Catalan) (NNS restaurants)) (CC and) (NP (JJ trendy) (NNS bars))))))))",
            "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (JJ Catalan) (NNS restaurants)) (, ,) (NP (JJ trendy) (NNS bars)) (CC and) (NP (NNS clubs))))))))"
        )


    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(self.location)
        self.assertEqual(resp.status_code, self.status_code)


    def test_empty_tree_returns_error(self):
        resp = self.client.get(self.location)
        self.assertEqual(resp.data, {'error': self.errors['empty_tree']})


    def test_invalid_tree_returns_error(self):
        resp = self.client.get(
            f'{self.location}{self.param1}{self.invalid_tree}'
        )
        self.assertEqual(resp.data, {'error': self.errors['invalid_tree']})


    def test_tree_without_matches_returns_empty_list(self):
        resp = self.client.get(
            f'{self.location}{self.param1}{self.tree_without_matches}'
        )
        self.assertEqual(resp.data['paraphrases'], self.twm_result)


    def test_result_contains_correct_trees_amount(self):
        resp = self.client.get(
            f'{self.location}{self.param1}{self.valid_tree}'
        )
        self.assertEqual(len(resp.data['paraphrases']), self.vt_length)


    def test_result_contains_expected_values(self):
        resp = self.client.get(
            f'{self.location}{self.param1}{self.valid_tree}'
        )
        res = [Tree.fromstring(p['tree']) for p in resp.data['paraphrases']]
        for value in self.example_output:
            self.assertIn(Tree.fromstring(value), res)


    def test_invalid_limit_returns_error(self):
        resp = self.client.get(
            f'{self.location}{self.param1}{self.valid_tree}{self.param2} \
                {self.invalid_limit_number}'
        )
        self.assertEqual(resp.data, {'error': self.errors['invalid_limit']})


    def test_invalid_limit_type_returns_error(self):
        resp = self.client.get(
            f'{self.location}{self.param1}{self.valid_tree}{self.param2} \
                {self.invalid_limit_type}'
        )
        self.assertEqual(resp.data, {'error': self.errors['invalid_limit_type']})


    def test_limit_returns_correct_amount_of_trees(self):
        resp = self.client.get(
            f'{self.location}{self.param1}{self.valid_tree}{self.param2} \
                {self.valid_limit}'
        )
        self.assertEqual(len(resp.data['paraphrases']), self.valid_limit)
