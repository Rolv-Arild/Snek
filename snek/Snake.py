import numpy

from snek.Segment import Segment

# Directions
NONE: int = 0
UP: int = 1
DOWN: int = -1
LEFT: int = -2
RIGHT: int = 2

# Pixel types
EMPTY = 0
FOOD = 1
HEAD = 2
SNAKE = 3


class Snek:
    """
    A class for representing a snake game
    """
    width: int = None
    height: int = None
    length: int = None
    __head__: Segment = None
    __tail__: Segment = None
    __heading__: int = None
    food_x: int = None
    food_y: int = None
    move_count: int = None

    def __init__(self, width: int, height: int, length: int, heading: int) -> None:
        """
        Initializer for snake object

        :param width: the width of the board
        :param height: the height of the board
        :param length: the length of the snake
        :param heading: the direction of the snake
        """
        self.width = width
        self.height = height
        self.length = length
        self.__heading__ = heading
        self.__head__ = Segment(length, 0, None, None)
        n = self.__head__
        for i in range(1, length):
            n.next = Segment(length - i, 0, None, n)
            n = n.next
        self.__tail__ = n
        self.move_count = 0
        self.__place_food___()

    def __place_food___(self) -> None:
        """
        Places food at a random location on the board

        :return: None
        """
        f = numpy.random.randint(0, self.width * self.height - self.length)

        f = self.__adjusted_f__(f)

        self.food_x = f % self.width
        self.food_y = f // self.width

    def __adjusted_f__(self, f: int) -> int:
        """
        Adjusts the initially selected value of f to an appropriate location
        on the board that ensures equal distribution outside of the snake

        :param f: the initial value of f
        :return: a new and improved value of f
        """
        c = 0
        n = self.__head__
        while n is not None:
            if n.y * self.width + n.x <= f:
                c += 1
            n = n.next

        for i in range(f + 1, f + c + 1):
            x = i % self.width
            y = i // self.width
            if self.__is_snake__(x, y):
                c += 1
        return f + c

    def __is_snake__(self, x: int, y: int) -> bool:
        """
        Finds out if a given coordinate is part of the snake or not

        :param x: the x value
        :param y: the y value
        :return: true if the coordinate (x, y) is a part of the snake
        """
        n = self.__head__
        while n is not None:
            if x == n.x and y == n.y:
                return True
            n = n.next
        return False

    def move(self) -> bool:
        """
        Moves the snake

        :return: false if this move kills the snake
        """
        if self.__heading__ == NONE:
            self._debug_()
            return True

        dx: int = {RIGHT: 1, LEFT: -1}.get(self.__heading__, 0)
        dy: int = {UP: 1, DOWN: -1}.get(self.__heading__, 0)

        is_kill: bool = False
        if self.__head__.x + dx < 0 \
                or self.__head__.x + dx >= self.width \
                or self.__head__.y + dy < 0 \
                or self.__head__.y + dy >= self.height:
            is_kill = True  # the snake hits the border

        n: Segment = self.__tail__
        while n != self.__head__:
            n.x = n.prev.x
            n.y = n.prev.y
            if n.x == self.__head__.x + dx and n.y == self.__head__.y + dy:
                is_kill = True  # the snake hits itself
            n = n.prev

        self.__head__.x += dx
        self.__head__.y += dy
        if self.__head__.x == self.food_x and self.__head__.y == self.food_y:
            self.length += 1
            self.__tail__.next = Segment(self.__tail__.x, self.__tail__.y, None, self.__tail__)
            self.__place_food___()
            self.__tail__ = self.__tail__.next

        if not is_kill:
            self.move_count += 1

        return not is_kill

    def _debug_(self):
        out: list = [[0] * self.width] * self.height
        i: int = 0
        while i < 1000000:
            self.__place_food___()
            out[self.food_y][self.food_x] += 1
            i += 1
        print(out)

    def set_direction(self, direction: int) -> None:
        """Sets the direction of the snake"""
        if direction != -self.__heading__:
            self.__heading__ = direction

    def pixels(self) -> [[int]]:
        out = [[EMPTY for _ in range(0, self.width + 1)] for _ in range(0, self.height + 1)]
        out[self.food_y][self.food_x] = FOOD
        n: Segment = self.__head__
        out[n.y][n.x] = HEAD
        n = n.next
        while n is not None:
            out[n.y][n.x] = SNAKE
            n = n.next
        return out

    def snake_coordinates(self):
        n: Segment = self.__head__
        out = []
        while n is not None:
            out.append((n.x, n.y))
            n = n.next
        return out
