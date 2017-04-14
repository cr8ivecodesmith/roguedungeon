class Room:
    """A rectangle on the map used to characterize a room

    """
    def __init__(self, x, y, w, h):
        self.x1, self.y1 = x, y
        self.x2, self.y2 = (x + w), (y + h)
        self.room_objects = []

    def center(self):
        """Returns the center coordinate of the room
        Primarily used to connect the room with tunnels

        """
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def intersect(self, other):
        """Returns true when this room intersects with `other` room

        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
