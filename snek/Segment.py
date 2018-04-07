class Segment:
    x: int = None
    y: int = None
    next = None
    prev = None

    def __init__(self, x: int, y: int, next, prev) -> None:
        self.x = x
        self.y = y
        self.next = next
        self.prev = prev
