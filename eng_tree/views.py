from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ParaphraseSerializer

from .synt_tree import TreePermutations


class ParaphraseListView(APIView):
    required_label = 'NP'
    inner_labels = {'NP', ',', 'CC'}

    errors = {
        'empty_tree': "Please, provide a tree parameter.",
        'invalid_tree': "Please, enter a valid syntax tree.",
        'invalid_limit_type': "The limit should be an integer.",
        'invalid_limit': "The limit should be higher than 0."
    }

    def get(self, request):
        tree = request.query_params.get('tree')
        limit = request.query_params.get('limit', 20)

        if not tree:
            return Response({'error': self.errors['empty_tree']})

        try:
            limit = int(limit)
            if limit < 1:
                return Response({'error': self.errors['invalid_limit']})
        except ValueError:
            return Response({'error': self.errors['invalid_limit_type']})

        syntax_tree = TreePermutations(tree,
                                     self.required_label,
                                     self.inner_labels)
        if syntax_tree.tree is None:
            return Response({'error': self.errors['invalid_tree']})

        paraphrases = syntax_tree.paraphrases[:limit]
        serializer = ParaphraseSerializer(paraphrases, many=True)

        return Response({'paraphrases': serializer.data})
