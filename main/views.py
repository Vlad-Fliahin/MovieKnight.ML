import numpy as np
import requests
from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework.views import APIView


class UserPrediction(APIView):
    def get(self, request, user_id):
        index = np.random.randint(250)

        url = "https://imdb-api.com/en/API/Top250Movies/k_4ae2fkk3"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        movies = response.json()
        movie = movies['items'][index]
        # create JSON object
        output = {'movie_id': movie['id']}

        return JsonResponse(output)
