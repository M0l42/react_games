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
    data_byte = request.data

    my_json = data_byte.decode('utf8').replace("'", '"')
    data = json.loads(my_json)

    snake = Snake(data['snake'])
    apple = Apple(data['apple'])
    algorithm = data['algorithm']

    if algorithm == 'dijkstra':
        path_algorithm = DijkstraAlgorithm(snake, apple)
        path = []
        for i in range(10):
            path.extend([0, 0, 2, 2, 1, 1, 3, 3])
    elif algorithm == 'a_star':
        path_algorithm = AStar(snake, apple)
        path = path_algorithm.test()
    result = path_algorithm.error
    if result is None:
        result = 'success'

    return jsonify({'result': result, 'path': path})


if __name__ == '__main__':
    app.run(debug=True)
