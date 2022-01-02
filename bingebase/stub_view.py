from django.http import JsonResponse

from rest_framework.views import APIView


class StubView(APIView):
    """
    Just a stub endpoint for testing
    """

    def get(self, request):
        stub_data = [{"name": "stub data 1"}, {"name": "stub data 2"}]
        return JsonResponse(stub_data, safe=False)