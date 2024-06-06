import pygame
from settings import *
from os import walk

class SurfaceMaker:
    def __init__(self):
        # Iterate over the directory structure using os.walk
        for index, info in enumerate(walk('../licenta2/graphics/blocks')):
            # Check if it's the first iteration
            if index == 0:
                # Initialize a dictionary to store assets for each color
                self.assets = {color: {} for color in info[1]}
            else:
                # For subsequent iterations, load images into the assets dictionary
                for image_name in info[2]:
                    # Get the color type based on the current index
                    color_type = list(self.assets.keys())[index - 1]
                    
                    # Construct the full path for the image
                    full_path = '../licenta2/graphics/blocks' + f'/{color_type}/' + image_name
                    
                    # Load the image using Pygame and convert it to an alpha surface
                    surf = pygame.image.load(full_path).convert_alpha()
                    
                    # Add the loaded image to the assets dictionary
                    # Use the image name (without the extension) as the key
                    self.assets[color_type][image_name.split('.')[0]] = surf


    def get_surf(self, block_type,size):

        #create surface
        image = pygame.Surface(size)
        image.set_colorkey((0,0,0))
        sides = self.assets[block_type]

        # 4 corners
        # Blit the top-left corner onto the image at position (0, 0)
        image.blit(sides['topleft'], (0, 0))

        # The x-coordinate is calculated by subtracting the width of the top-right corner from the width of the image
        image.blit(sides['topright'], (size[0] - sides['topright'].get_width(), 0))

        # The y-coordinate is calculated by subtracting the height of the bottom-left corner from the height of the image
        image.blit(sides['bottomleft'], (0, size[1] - sides['bottomleft'].get_height()))

        # Both x and y coordinates are calculated similarly to the top-right corner
        image.blit(sides['bottomright'], (size[0] - sides['bottomright'].get_width(), size[1] - sides['bottomright'].get_height()))



        #top side
        top_width = size[0] - (sides['topleft'].get_width() + sides['topright'].get_width())
        scaled_top_surf = pygame.transform.scale(sides['top'],(top_width, sides['top'].get_height()))
        image.blit(scaled_top_surf, (sides['topleft'].get_width(),0))

        #left side
        left_height = size[1] - (sides['topleft'].get_height() + sides['bottomleft'].get_height())
        scaled_left_surf = pygame.transform.scale(sides['left'],((sides['left'].get_width(), left_height)))
        image.blit(scaled_left_surf, (0, sides['topleft'].get_height()))

        #right side
        right_height = size[1] - (sides['topright'].get_height() + sides['bottomright'].get_height())
        scaled_right_surf = pygame.transform.scale(sides['right'],(sides['right'].get_width(), right_height))
        image.blit(scaled_right_surf, (size[0] - sides['right'].get_width(), sides['topright'].get_height()))

        #bottom side
        bottom_width = size[0] - (sides['bottomleft'].get_width() + sides['bottomright'].get_width())
        scaled_bottom_surf = pygame.transform.scale(sides['bottom'],(bottom_width, sides['bottom'].get_height()))
        image.blit(scaled_bottom_surf, (sides['topleft'].get_width(),size[1] - sides['bottom'].get_height()))

        #center col
        center_height = size[1] - (sides['top'].get_height() + sides['bottom'].get_height())
        center_width = size[0] - (sides['right'].get_width() + sides['left'].get_width())
        scaled_center = pygame.transform.scale(sides['center'],(center_width, center_height))
        image.blit(scaled_center, sides['topleft'].get_size())
        return image
