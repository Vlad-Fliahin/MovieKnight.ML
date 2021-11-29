import numpy as np
import pandas as pd
import os
import json
import requests

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from MovieKnight.settings import BASE_DIR
from io import StringIO


GENRES = 28
WEIGHTS = np.array([1, 0.01, 0.01, 0.01] + [1 for _ in range(GENRES)], dtype=np.float32)
IMPORTANT_FEATURES = ['isAdult', 'startYear', 'runtimeMinutes',
       'averageRating', 'Family', 'Biography', 'Film-Noir',
       'Crime', 'Music', 'Adult', 'Drama', 'Mystery', 'Adventure', 'History',
       'Fantasy', 'Documentary', 'News', 'Horror', 'Thriller', 'Game-Show',
       'Western', 'Comedy', 'Sport', 'Action', 'Sci-Fi', 'Talk-Show',
       'Animation', 'Romance', 'Reality-TV', 'War', 'Short', 'Musical']


def diff(a, b):
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    return np.sum(abs(b - a) * WEIGHTS)


class UserPrediction(APIView):
    def get(self, request, username):
        url = f"https://movieknightweb.azurewebsites.net/api/User/{username}"
        response = requests.request("GET", url)

        # print(response.content)

        # print(type(response.content))
        almost_json = response.content.decode('utf8').replace("'", '"')
        response_dict = json.loads(almost_json)
        print(response_dict)
        watch_history = response_dict['watchHistory']
        print(watch_history)
        movie_id = ""
        watched_movies = []
        for watch in watch_history:
            watched_movies.append(watch["movie"]["imDbId"])
            if not movie_id and watch["rating"] >= 8:
                movie_id = watch["movie"]["imDbId"]

        movies_data = pd.read_csv(f'{BASE_DIR}/static/movies_data.csv')
        movies_data.index = movies_data.tconst
        movies_data.drop(columns=['tconst'], inplace=True)
        # print(movies_data.columns)
        print(movie_id)
        if not movie_id:
            return JsonResponse({'movie_id': np.random.choice(movies_data.index, 1)[0]})

        random_movies = np.random.choice(movies_data.index, 2000)
        differences = dict()

        for film in random_movies:
            differences[film] = 100

        for film in movies_data.loc[random_movies].values:
            film_id = film[-1]
            if film_id in watched_movies:
                continue
            print(film)
            print(film_id in movies_data.index)
            differences[film_id] = diff(movies_data.loc[movie_id, IMPORTANT_FEATURES],
                                        movies_data.loc[film_id, IMPORTANT_FEATURES])

        mn = 1000
        id_mn = 0
        for key, value in differences.items():
            if value < mn:
                id_mn = key
                mn = value

        # create JSON object
        output = {'movie_id': id_mn}
        return JsonResponse(output)
