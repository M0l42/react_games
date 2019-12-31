class Apple:
    def __init__(self, data):
        self.x = data['x']
        self.y = data['y']


class Snake:
    def __init__(self, data):
        self.body = list()
        for coordinate in data:
            self.body.append((coordinate['x'], coordinate['y']))

