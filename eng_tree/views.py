from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ParaphraseSerializer

from .synt_tree import TreePermutations


class ParaphraseListView(APIView):
    required_label = 'NP'
    inner_labels = {'NP', ',', 'CC'}

    def get(self, request):
        tree = request.query_params.get('tree')
        limit = request.query_params.get('limit', 20)

        if not tree:
            return Response({'error': 'Please, provide a tree parameter.'})

        try:
            limit = int(limit)
        except ValueError:
            return Response({'error': 'The limit should be an integer.'})

        paraphrases = TreePermutations(tree,
                                       self.required_label,
                                       self.inner_labels).paraphrases
        if paraphrases:
            paraphrases = paraphrases[:limit]

        serializer = ParaphraseSerializer(paraphrases, many=True)

        return Response({'paraphrases': serializer.data})
