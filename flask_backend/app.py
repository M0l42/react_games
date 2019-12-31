from flask import Flask, render_template, request, jsonify
from path_algorithm import DijkstraAlgorithm, AStar
from game_object import Apple, Snake
import json

app = Flask(__name__)


@app.route('/')
def home():
    title = "Home"
    return render_template("home.html", title=title)


@app.route('/game-of-life/')
def game_of_life():
    context = {
        "title": "Game of Life",
        "description": "A two dimensional universe in which patterns evolve through time."
    }
    return render_template("game_of_life.html", context=context)


@app.route('/snake/')
def snake():
    title = "Snake"
    description = "Snake using path finding algorithm to find the apple"
    return render_template("snake.html",
                           title=title,
                           description=description,)


@app.route('/update/', methods=['POST'])
def update():
    app.logger.warning("HERE !")
    data_byte = request.data

    my_json = data_byte.decode('utf8').replace("'", '"')
    app.logger.warning(my_json)
    data = json.loads(my_json)

    snake = Snake(data['snake'])
    apple = Apple(data['apple'])
    algorithm = data['algorithm']
    app.logger.warning(snake.body)
    app.logger.warning(apple.y)
    app.logger.warning(apple.x)
    app.logger.warning(algorithm)

    if algorithm == 'dijkstra':
        path_algorithm = DijkstraAlgorithm(snake, apple)
    elif algorithm == 'a_star':
        path_algorithm = AStar(snake, apple)
    path = path_algorithm.test()
    # app.logger.warning(path)

    # if algorithm == 'DijkstraAlgorithm':
    #     path_algorithm = DijkstraAlgorithm(snake, apple)
    # else:
    #     path_algorithm = AStar(snake, apple)
    # path = path_algorithm.test()
    #
    return jsonify({'result': 'sucess', 'path': path})


if __name__ == '__main__':
    app.run(debug=True)
