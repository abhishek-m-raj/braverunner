import os
import sys

import pygame

from load_data import FONT_PATH, menu_folder
from utils.button import Button


class GameOverlay:
    """A modular overlay for Pause and Win screens"""

    def __init__(self, title, buttons_config):
        self.title = title
        self.buttons_config = buttons_config
        self.run_overlay = False
        self.status = None  # To return choice (e.g., 'resume', 'home')

    def draw(self, win):
        self.run_overlay = True
        self.status = None
        clock = pygame.time.Clock()

        sw, sh = win.get_size()

        # Capture current screen to maintain translucency
        bg_snapshot = win.copy()

        # Create translucent surface
        overlay_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay_surf.fill((0, 0, 0, 150))  # Black with transparency

        # UI constants

        BUTTON_WIDTH = 200
        BUTTON_HEIGHT = 60
        BUTTON_SPACING = 20

        # Load button backgrounds
        button_bg = pygame.image.load(os.path.join(menu_folder, "ButtonBg/Default.png"))
        button_bg_hover = pygame.image.load(
            os.path.join(menu_folder, "ButtonBg/Hover.png")
        )

        # Create buttons
        buttons = []
        total_height = (
            len(self.buttons_config) * (BUTTON_HEIGHT + BUTTON_SPACING) - BUTTON_SPACING
        )
        start_y = sh // 2 - total_height // 2 + 50

        for i, config in enumerate(self.buttons_config):
            # Closure to capture status
            def make_on_click(s):
                return lambda: self.set_status(s)

            btn = Button(
                x=sw // 2 - BUTTON_WIDTH // 2,
                y=start_y + i * (BUTTON_HEIGHT + BUTTON_SPACING),
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                text=config["text"],
                image=button_bg,
                hover_image=button_bg_hover,
                on_click=make_on_click(config["status"]),
            )
            # Style text
            btn.set_font(font_size=40, bold=True)
            buttons.append(btn)

        while self.run_overlay:
            clock.tick(60)

            # Draw captured game state
            win.blit(bg_snapshot, (0, 0))

            # Blit translucent background
            win.blit(overlay_surf, (0, 0))
            # Draw Title
            font = pygame.font.Font(FONT_PATH, 80)
            title_surf = font.render(self.title, True, (255, 255, 255))
            win.blit(title_surf, (sw // 2 - title_surf.get_width() // 2, sh // 2 - 200))

            for btn in buttons:
                btn.handle_event()
                btn.update()
                btn.draw(win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    sw, sh = event.size
                    win = pygame.display.set_mode((sw, sh), pygame.RESIZABLE)
                    overlay_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
                    overlay_surf.fill((0, 0, 0, 150))
                    # Re-center buttons
                    for j, b in enumerate(buttons):
                        b.set_location(
                            sw // 2 - BUTTON_WIDTH // 2,
                            start_y + j * (BUTTON_HEIGHT + BUTTON_SPACING),
                        )

            pygame.display.flip()

            if self.status:
                self.run_overlay = False

        return self.status

    def set_status(self, status):
        self.status = status
