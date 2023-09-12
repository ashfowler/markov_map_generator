"""
Generates a map using a Markov model. Includes landmasses, bodies of water, forests, and mountains.
Author: Ash Fowler
"""

import numpy
from PIL import Image
from PIL import ImageDraw

""" The types of terrain in the map """
TERRAIN_TYPES = [
    "grass",
    "sand",
    "water",
    "forest",
    "low mountain",
    "high mountain"
]
""" The RGB values of the colors for each terrain type """
MAP_COLORS = {
    "grass": (115, 189, 63),
    "sand": (240, 226, 189),
    "water": (92, 116, 209),
    "forest": (68, 117, 45),
    "low mountain": (132, 126, 135),
    "high mountain": (103, 94, 107)
}
""" Contains the probablilities for "moving" from one terrain type to another """
TRANSITION_MATRIX = {
    "grass": {
        "grass": 0.9,
        "sand": 0.05,
        "water": 0.0,
        "forest": 0.025,
        "low mountain": 0.025,
        "high mountain": 0.0
        },
    "sand": {
        "grass": 0.1,
        "sand": 0.8,
        "water": 0.08,
        "forest": 0.0,
        "low mountain": 0.02,
        "high mountain": 0.0
        },
    "water": {
        "grass": 0.0,
        "sand": 0.2,
        "water": 0.8,
        "forest": 0.0,
        "low mountain": 0.0,
        "high mountain": 0.0
        },
    "forest": {
        "grass": 0.1,
        "sand": 0.0,
        "water": 0.0,
        "forest": 0.9,
        "low mountain": 0.0,
        "high mountain": 0.0
        },
    "low mountain": {
        "grass": 0.075,
        "sand": 0.02,
        "water": 0.005,
        "forest": 0.0,
        "low mountain": 0.8,
        "high mountain": 0.1
        },
    "high mountain": {
        "grass": 0.0,
        "sand": 0.0,
        "water": 0.0,
        "forest": 0.0,
        "low mountain": 0.4,
        "high mountain": 0.6
        }
}
""" The width of the image to be generated in pixels """
IMAGE_WIDTH = 1000
""" The height of the image to be generated in pixels """
IMAGE_HEIGHT = 700
""" The length/height of each square of the grid in pixels """
GRID_SIZE = 4

def check_probabilities():
    """A testing function which prints out the values of the sums of the transition matrix's probabilities.
    Each sum should end up being equal to 1.0.
    """
    # TODO delete this function later
    dicts = TRANSITION_MATRIX.values()
    for d in dicts:
        d_keys = d.values()
        sum = 0
        for k in d_keys:
            sum += k
        print(sum)

def get_probabilities(terrain_type):
    """Returns a list of the probabilities of choosing each terrain type in the order presented in the TERRAIN_TYPES object.
       Args:
            terrain_type (str): the terrain type to get the probabilities for
    """
    terrain_dict = TRANSITION_MATRIX.get(terrain_type)
    print(terrain_type)
    probs = []
    for terrain in TERRAIN_TYPES:
        print(terrain_dict[terrain])
        probs.append(terrain_dict[terrain])
    return probs

def get_first_point(): # TODO rename to terrain, not point?
    """Chooses a random terrain type to start with. Returns the name of the terrain type as a string."""
    first_point = numpy.random.choice(TERRAIN_TYPES)
    return first_point

def get_next_point(current_point):
    """Chooses the next terrain type that will be drawn on the map based on the probablities provided by the transition matrix.
       Returns the name as a string.
       Args:
            current_point (str): the name of the terrain type to be transitioned from
    """
    next_point = numpy.random.choice(TERRAIN_TYPES, p=get_probabilities(current_point))
    print(next_point)
    return next_point

def main():
    # TODO make background an old map. maybe add an image? add a border?
    
    # set up window
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
    imgdraw = ImageDraw.Draw(img)
    
    current_point = get_first_point()

    for x in range(IMAGE_WIDTH+1):
        for y in range(IMAGE_HEIGHT+1):
            next_point = get_next_point(current_point)
            next_point_color = MAP_COLORS[next_point]
            imgdraw.point([(x,y)], fill=next_point_color)
            current_point = next_point

    img.save("images/image.png")

if __name__ == "__main__":
    main()
