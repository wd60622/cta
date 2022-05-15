from enum import Enum


class Route(Enum):
    """Enum of the different train lines.

    Codes found in the API documentation.

    """

    RED = "red"
    BLUE = "blue"
    BROWN = "brn"
    GREEN = "g"
    ORANGE = "org"
    PURPLE = "p"
    PINK = "pink"
    YELLOW = "y"
