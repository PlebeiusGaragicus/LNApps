import pygame
import numpy as np
from scipy.ndimage import gaussian_filter

def extract_bright_parts(surface, threshold=200):
    """Extract the bright parts of a surface."""
    array = pygame.surfarray.array3d(surface)
    brightness = np.average(array, axis=2)
    mask = brightness < threshold
    for channel in range(3):
        array[:,:,channel][mask] = 0
    return pygame.surfarray.make_surface(array)

def blur_surface(surface, radius=2):
    """Apply Gaussian blur to a surface."""
    array = pygame.surfarray.array3d(surface)
    for channel in range(3):
        array[:,:,channel] = gaussian_filter(array[:,:,channel], sigma=radius)
    return pygame.surfarray.make_surface(array)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bloom Effect with pygame")

# Assume 'image' is your loaded image that you want to apply the bloom effect to
image = pygame.image.load('path_to_your_image.png')

# Extract the bright parts of the image
bright_parts = extract_bright_parts(image)

# Blur the bright parts
blurred_bright_parts = blur_surface(bright_parts, radius=5)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(blurred_bright_parts, (0, 0))
    screen.blit(image, (0, 0))
    pygame.display.flip()

pygame.quit()
