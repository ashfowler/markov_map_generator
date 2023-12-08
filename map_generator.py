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
        "grass": 0.94,
        "sand": 0.02,
        "water": 0.01,
        "forest": 0.015,
        "low mountain": 0.015,
        "high mountain": 0.0
        },
    "sand": {
        "grass": 0.06,
        "sand": 0.91,
        "water": 0.03,
        "forest": 0.0,
        "low mountain": 0.0,
        "high mountain": 0.0
        },
    "water": {
        "grass": 0.02,
        "sand": 0.02,
        "water": 0.96,
        "forest": 0.0,
        "low mountain": 0.0,
        "high mountain": 0.0
        },
    "forest": {
        "grass": 0.08,
        "sand": 0.0,
        "water": 0.0,
        "forest": 0.92,
        "low mountain": 0.0,
        "high mountain": 0.0
        },
    "low mountain": {
        "grass": 0.035,
        "sand": 0.01,
        "water": 0.0,
        "forest": 0.0,
        "low mountain": 0.83,
        "high mountain": 0.125
        },
    "high mountain": {
        "grass": 0.0,
        "sand": 0.0,
        "water": 0.0,
        "forest": 0.0,
        "low mountain": 0.25,
        "high mountain": 0.75
        }
}
""" The width of the image to be generated in pixels """
IMAGE_WIDTH = 1400
""" The height of the image to be generated in pixels """
IMAGE_HEIGHT = 904
""" The length/height of each square of the grid in pixels """
GRID_SIZE = 8

class MapGenerator:
    def __init__(self, transition_matrix):
        self.transition_matrix = transition_matrix
        self.terrain_types = list(transition_matrix)
        self.current_terrain = self.get_first_terrain()
        self.current_x = 0 # in pixels, not referencing the grid
        self.current_y = 0 # in pixels, not referencing the grid

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
            # WHEN STARTING A NEW COLUMN, DON'T RELY ON CURRENT_TERRAIN TO DECIDE NEW TERRAIN TODO
        else:
            # past the first column, we want to average the probabilities from the current pixel (before) and the pixel to the left
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
        coords_left = (self.current_x-GRID_SIZE, self.current_y)
        terrain_left_color = self.img.getpixel(coords_left)
        terrain_left = self.get_terrain_from_color(terrain_left_color)
        probs_left = self.get_probabilities(terrain_left)
        probs_before = self.get_probabilities(self.current_terrain)

        new_probs = []
        num_zeroes = 0
        leftover = 0
        for i in range(len(self.terrain_types)):
            if probs_left[i] == 0 or probs_before[i] == 0:
                new_probs.append(0)
                num_zeroes += 1
                leftover = leftover + (probs_left[i] + probs_before[i])/2
            else:
                sum = probs_left[i] + probs_before[i]
                new_probs.append(sum/2)
        
        if num_zeroes > 0 and leftover > 0:
            num_non_zeroes = len(self.terrain_types) - num_zeroes
            if num_non_zeroes == 0:
                # # no overlap between the two terrain types. Average them like normal.
                # for i in range(len(new_probs)):
                #     sum = probs_left[i] + probs_before[i]
                #     new_probs[i] = (sum/2)

                # no overlap between the two terrain types. prioritize current_terrain
                new_probs = probs_before
                # TODO make it randomly choose one
            else:
                # anything that is a 0% chance for one of the terrains but not for the other will be a 0% chance in the new probabilities TODO word this better
                for i in range(len(new_probs)):
                    if new_probs[i] != 0:
                        new_probs[i] += leftover/num_non_zeroes # sand and hm have no overlap: probs will be all 0s
        
        return new_probs
    
    def get_terrain_from_color(self, color):
        for t in self.terrain_types:
            if MAP_COLORS.get(t) == color:
                return t
        return None
    
    def generate_map(self, image_name): # TODO let it take image size as param - have to make sure edges ok if not divisible by GRID_SIZE
        
        for x in range(0, IMAGE_WIDTH, GRID_SIZE):
            self.current_x = x
            for y in range(0, IMAGE_HEIGHT, GRID_SIZE):
                self.current_y = y
                current_pixel_color = self.img.getpixel((x+1,y+1))
                if current_pixel_color[0] == current_pixel_color[1] == current_pixel_color[2] == 0: # if the current pixel hasn't been filled yet
                    next_terrain_color = MAP_COLORS[self.current_terrain]
                    rand_int_x = numpy.random.randint(1, 2)
                    rand_int_y = numpy.random.randint(1, 2) # TODO currently, these two variables do nothing. They roll a 1 every time. Just here for testing purposes.
                    self.imgdraw.rectangle([(x,y), (x+(GRID_SIZE*rand_int_x), y+(GRID_SIZE*rand_int_y))], fill=next_terrain_color)
                    self.get_next_terrain()
                
                self.img.save(image_name) # TODO take this out. just here for testing purposes

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
