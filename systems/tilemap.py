import pygame
import pytmx


class TiledMap:
    def __init__(self, filename):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight

    def render(self, surface):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                off_x = getattr(layer, "offsetx", 0)
                off_y = getattr(layer, "offsety", 0)
                for x, y, tile in layer.tiles():
                    if tile:
                        surface.blit(
                            tile,
                            (
                                x * self.tmxdata.tilewidth + off_x,
                                (y + 1) * self.tmxdata.tileheight
                                + off_y
                                - tile.get_height(),
                            ),
                        )

    def make_map(self):
        temp_surface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        ).convert_alpha()
        self.render(temp_surface)
        return temp_surface
