import pygame


class Spritesheet(object):
    def __init__(self, filename, tile_width, tile_height, colorkey=None):
        self.filename = filename
        self.sheet = pygame.image.load(filename)
        self.colorkey = colorkey
        self.sheet = self.sheet.convert()

        self.tile_width = tile_width
        self.tile_height = tile_height

    def image_at(self, tile_col, tile_row):
        "Loads image from tile_col and tile_row tile"
        rect = pygame.Rect(
            tile_col * self.tile_width,
            tile_row * self.tile_height,
            self.tile_width,
            self.tile_height
        )
        image = pygame.Surface(rect.size)
        if self.colorkey != None:
            image.set_colorkey(self.colorkey)
        image.blit(self.sheet, (0, 0), rect)
        return image

    def blit_tile(self, surface, tile_col, tile_row, x, y):
        "Loads image from tile_col and tile_row tile"
        rect = pygame.Rect(
            tile_col * self.tile_width,
            tile_row * self.tile_height,
            self.tile_width,
            self.tile_height
        )
        if self.colorkey != None:
            self.sheet.set_colorkey(self.colorkey)
        surface.blit(self.sheet, (x, y), rect)

    def __getitem__(self, tile_coords):
        tile_col, tile_row = tile_coords
        return self.image_at(tile_col, tile_row)

    def __str__(self):
        return f"{self.tile_width} * {self.tile_height}"

    def __repr__(self):
        return f"Spritesheet({self.tile_width} * {self.tile_height}, {self.filename})"
