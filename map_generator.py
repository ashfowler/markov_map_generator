"""
Generates a map using a Markov model. Includes landmasses, bodies of water, forests, and mountains.
Author: Ash Fowler
"""

import numpy
from PIL import Image
from PIL import ImageDraw

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
IMAGE_WIDTH = 1400
""" The height of the image to be generated in pixels """
IMAGE_HEIGHT = 900
""" The length/height of each square of the grid in pixels """
GRID_SIZE = 4

class MapGenerator:
    def __init__(self, transition_matrix):
        self.transition_matrix = transition_matrix
        self.terrain_types = list(transition_matrix)
        self.current_terrain = self.get_first_terrain()
    
    def get_first_terrain(self):
        """Chooses a random terrain type to start with. Returns the name of the terrain type as a string."""
        first_terrain = numpy.random.choice(self.terrain_types)
        return first_terrain
    
    def get_next_terrain(self):
        """Chooses the next terrain type that will be drawn on the map based on the probablities provided by the transition matrix.
           Returns the name as a string.
           Args:
                current_terrain (str): the name of the terrain type to be transitioned from
        """
        next_terrain = numpy.random.choice(self.terrain_types, p=self.get_probabilities(self.current_terrain))

        self.current_terrain = next_terrain
    
    def get_probabilities(self, terrain):
        """Returns a list of the probabilities of choosing each terrain type in the order presented in terrain_types.
           Args:
                terrain_type (str): the terrain type to get the probabilities for
        """
        terrain_dict = self.transition_matrix.get(terrain)
        probs = []
        for terrain in self.terrain_types:
            probs.append(terrain_dict[terrain])
        return probs


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

def main():
    # TODO make background an old map. maybe add an image? add a border?
    print("Generating map ...")

    # set up image
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
    imgdraw = ImageDraw.Draw(img)

    map_generator = MapGenerator(TRANSITION_MATRIX)

    for x in range(0, IMAGE_WIDTH, 4):
        for y in range(0, IMAGE_HEIGHT, 4):
            next_terrain_color = MAP_COLORS[map_generator.current_terrain]
            imgdraw.rectangle([(x,y), (x+GRID_SIZE, y+GRID_SIZE)], fill=next_terrain_color)
            map_generator.get_next_terrain()

    img.save("test_images/image.png")

    print("Done!")

if __name__ == "__main__":
    main()
