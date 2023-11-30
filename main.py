from flask import Flask, render_template, url_for
import requests
import math
app = Flask(__name__)

API = "45dbe079194b85f3c980907d6c1cb76e"
image_pre = "https://image.tmdb.org/t/p/w300"

dict_genre = {'genres': [{'id': 28, 'name': 'Action'}, {'id': 12, 'name': 'Adventure'}, {'id': 16, 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 80, 'name': 'Crime'}, {'id': 99, 'name': 'Documentary'}, {'id': 18, 'name': 'Drama'}, {'id': 10751, 'name': 'Family'}, {'id': 14, 'name': 'Fantasy'}, {'id': 36, 'name': 'History'}, {'id': 27, 'name': 'Horror'}, {'id': 10402, 'name': 'Music'}, {'id': 9648, 'name': 'Mystery'}, {'id': 10749, 'name': 'Romance'}, {'id': 878, 'name': 'Science Fiction'}, {'id': 10770, 'name': 'TV Movie'}, {'id': 53, 'name': 'Thriller'}, {'id': 10752, 'name': 'War'}, {'id': 37, 'name': 'Western'}]}


def funcForBackdropPath(image_data, image_pre=image_pre):
    if image_data['poster_path'] is None:
        if image_data['backdrop_path'] is None:
            static_image_url = url_for('static', filename='images/no_image.png')
            return (static_image_url, image_data['original_title'], image_data['id'])
        else:
            return (image_pre + image_data['backdrop_path'], image_data['original_title'], image_data['id'])
    else:
        return (image_pre + image_data['poster_path'], image_data['original_title'], image_data['id'], image_data['vote_average'], image_data['release_date'])





# for top rated - requesting only once so that server doesnt load
def funcForTopRated():
    top_rated_url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"

    headers_top_rated = {"accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWRiZTA3OTE5NGI4NWYzYzk4MDkwN2Q2YzFjYjc2ZSIsInN1YiI6IjY1NjYyYTcyODlkOTdmMDBhYjE1ZWUzZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.HkrlRy6Ny7G9uwCzFuYrSW7V7GGEslMEL6W0TA6dyjE"
    }

    response_top_rated = requests.get(top_rated_url, headers=headers_top_rated)

    data_top_rated = response_top_rated.json()
    # print(data_top_rated)
    image_data = data_top_rated["results"]



    images = []

    for i in range(10):

        images.append(funcForBackdropPath(image_data[i]))

    return images


images_for_top_rated = funcForTopRated()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404



@app.route('/')
def index():
    return render_template('index.html', message='Hello, World!',  genres=dict_genre['genres'])

@app.route('/trending/<timeperiod>/<page_no>')
def trending(timeperiod, page_no):
    page_no = int(page_no)
    trending_url = f"https://api.themoviedb.org/3/trending/movie/{timeperiod}?language=en-US&page={page_no}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWRiZTA3OTE5NGI4NWYzYzk4MDkwN2Q2YzFjYjc2ZSIsInN1YiI6IjY1NjYyYTcyODlkOTdmMDBhYjE1ZWUzZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.HkrlRy6Ny7G9uwCzFuYrSW7V7GGEslMEL6W0TA6dyjE"
    }

    response = requests.get(trending_url, headers=headers)
    data = response.json()


    total_results = data.get('total_results', 0)
    image_data = data["results"]
    # total_pages = math.ceil(total_results/20)
    # print(data)
    total_pages = 500
    if len(image_data)==0:
        print("length 0")


    images = []

    for i in range(len(image_data)):
        # print(image_data[i]['poster_path'], image_data[i]['backdrop_path'])

        images.append(funcForBackdropPath(image_data[i]))

    # print(page_no)
    # images = []
    search_input = ""
    # total_pages = 10
    # page_no = 1
    # timeperiod = "day"
    return render_template('trending.html',timeperiod=timeperiod, images=images, total_pages=total_pages, page_no=page_no, top_rated_images=images_for_top_rated,  genres=dict_genre['genres'])

@app.route('/search/<search_input>/<page_no>')
def search(search_input, page_no):
    page_no = int(page_no)
    # print(f"{search_input}")
    tmdbQueryString =  f"https://api.themoviedb.org/3/search/movie?query={search_input}&api_key={API}&page={page_no}"
    response = requests.get(tmdbQueryString)
    data = response.json()
    # print(data["results"])
    total_results = data.get('total_results', 0)
    image_data = data["results"]
    total_pages = math.ceil(total_results/20)

    if len(image_data)==0:
        print("length 0")


    images = []

    for i in range(len(image_data)):
        # print(image_data[i]['poster_path'], image_data[i]['backdrop_path'])

        images.append(funcForBackdropPath(image_data[i]))




    return render_template('search.html', images=images, search_input=search_input, total_pages=total_pages, page_no=page_no, top_rated_images=images_for_top_rated,  genres=dict_genre['genres'])

    # return tmdbQueryString
    # return render_template('search.html', message='Hello, World!')

@app.route('/movie_page/<idm>')
def movie_page(idm):
    # print("hehe",idm)
    image_pre = "https://image.tmdb.org/t/p/original"
    tmdbQueryString = f"https://api.themoviedb.org/3/movie/{int(idm)}?api_key={API}"
    response = requests.get(tmdbQueryString)
    data = response.json()
    # print(data)
    if "success" in data.keys():
        if data['success'] == False:
            return render_template('404.html')
    else:
        images_data = funcForBackdropPath(data)
        # print(images_data, image_pre)
        return render_template('movie_page.html', images_data=data, genres=dict_genre['genres'])


if __name__ == '__main__':
    app.run(debug=True)
#  192.168.144.1
# waitress-serve --host=192.168.144.1 --port=8080 main:app
