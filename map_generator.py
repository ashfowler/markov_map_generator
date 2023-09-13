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
        self.current_x = 0 # in pixels
        self.current_y = 0 # in pixels

        # set up image
        self.img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
        self.imgdraw = ImageDraw.Draw(self.img)
    
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
        if self.current_x == 0:
            # we can just use the base probabilities for the first column, since there are no filled in pixels to the left
            next_terrain = numpy.random.choice(self.terrain_types, p=self.get_probabilities(self.current_terrain))
        else:
            # past the first column, we want to average the probabilities from the current pixel (below) and the pixel to the left
            new_probabilities = self.get_new_probabilities()
            next_terrain = numpy.random.choice(self.terrain_types, p=new_probabilities)

        self.current_terrain = next_terrain
    
    def get_probabilities(self, terrain):
        """Returns a list of the probabilities of choosing each terrain type in the order presented in terrain_types.
           Args:
                terrain_type (str): the terrain type to get the probabilities for
        """
        terrain_dict = self.transition_matrix.get(terrain)
        probs = []
        for t in self.terrain_types:
            probs.append(terrain_dict[t])
        return probs
    
    def get_new_probabilities(self):
        coords_left = (self.current_x-4, self.current_y)
        terrain_left_color = self.img.getpixel(coords_left)
        terrain_left = self.get_terrain_from_color(terrain_left_color)
        probs_left = self.get_probabilities(terrain_left)
        probs_below = self.get_probabilities(self.current_terrain)

        new_probs = []
        for i in range( len(self.terrain_types) ):
            sum = probs_left[i] + probs_below[i]
            new_probs.append(sum/2)

        return new_probs
    
    def get_terrain_from_color(self, color):
        for t in self.terrain_types:
            if MAP_COLORS.get(t) == color:
                return t
        return None
    
    def generate_map(self, image_name): # TODO let it take image size as param - have to make sure edges ok if not divisible by 4
        

        for x in range(0, IMAGE_WIDTH, 4):
            self.current_x = x
            for y in range(0, IMAGE_HEIGHT, 4):
                self.current_y = y
                next_terrain_color = MAP_COLORS[self.current_terrain]
                self.imgdraw.rectangle([(x,y), (x+GRID_SIZE, y+GRID_SIZE)], fill=next_terrain_color)
                self.get_next_terrain()

        self.img.save(image_name)


def check_probabilities(probs):
    """A testing function which prints out the value of the sum a list of probabilities.
       Each sum should end up being equal to 1.0.
    """
    # TODO delete this later
    sum = 0
    for i in probs:
        sum += i
    print(sum)

def main():
    # TODO make background an old map. maybe add an image? add a border?
    print("Generating map...")
    map_generator = MapGenerator(TRANSITION_MATRIX)
    map_generator.generate_map("test_images/image.png") # TODO change default destination
    print("Done!")

if __name__ == "__main__":
    main()
