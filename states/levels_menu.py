import os
import sys

import pygame

from load_data import FONT_PATH, LEVELS, levels, menu_folder, menuBG
from save_manager import is_level_unlocked, load_save
from settings import FPS
from states.level import Level
from systems.tilemap import TiledMap
from utils.button import Button


class LevelsMenu:
    def __init__(self):
        self.run_levels = False

    def draw(self, win):
        self.run_levels = True
        clock = pygame.time.Clock()
        current_category = None

        # UI constants
        CAT_BUTTON_SIZE = 150
        LEVEL_BUTTON_SIZE = 120
        BUTTON_SPACING = 30

        # Load images
        classic_img = pygame.image.load(os.path.join(menu_folder, "classic bt.png"))
        desert_img = pygame.image.load(os.path.join(menu_folder, "desert bt.png"))
        graveyard_img = pygame.image.load(os.path.join(menu_folder, "graveyard bt.png"))
        level_unlocked_img = pygame.image.load(
            os.path.join(menu_folder, "Level/Unlocked.png")
        )
        level_locked_img = pygame.image.load(
            os.path.join(menu_folder, "Level/Locked.png")
        )
        button_bg_image = pygame.image.load(
            os.path.join(menu_folder, "ButtonBg/Default.png")
        )
        button_bg_image_hover = pygame.image.load(
            os.path.join(menu_folder, "ButtonBg/Hover.png")
        )
        back_button_icon = pygame.image.load(
            os.path.join(menu_folder, "Icons/ArrowLeft-Thin.png")
        )

        def on_back_click():
            nonlocal current_category, active_buttons
            if current_category is None:
                self.run_levels = False
            else:
                current_category = None
                active_buttons = create_category_buttons()

        back_btn = Button(
            x=50,
            y=50,
            width=60,
            height=60,
            image=button_bg_image,
            hover_image=button_bg_image_hover,
            icon=back_button_icon,
            icon_size=30,
            on_click=on_back_click,
        )

        completed_levels = load_save().get("completed_levels", [])

        def create_category_buttons():
            sw, sh = win.get_size()
            btns = []

            total_width = 3 * CAT_BUTTON_SIZE + 2 * BUTTON_SPACING
            start_x = (sw - total_width) // 2
            y = sh // 2 - CAT_BUTTON_SIZE // 2

            btns.append(
                Button(
                    x=start_x,
                    y=y,
                    width=CAT_BUTTON_SIZE,
                    height=CAT_BUTTON_SIZE,
                    image=classic_img,
                    on_click=lambda: set_category("classic"),
                )
            )

            btns.append(
                Button(
                    x=start_x + CAT_BUTTON_SIZE + BUTTON_SPACING,
                    y=y,
                    width=CAT_BUTTON_SIZE,
                    height=CAT_BUTTON_SIZE,
                    image=desert_img,
                    on_click=lambda: set_category("desert"),
                )
            )

            btns.append(
                Button(
                    x=start_x + 2 * (CAT_BUTTON_SIZE + BUTTON_SPACING),
                    y=y,
                    width=CAT_BUTTON_SIZE,
                    height=CAT_BUTTON_SIZE,
                    image=graveyard_img,
                    on_click=lambda: set_category("graveyard"),
                )
            )
            return btns

        def create_level_buttons(category):
            sw, sh = win.get_size()
            btns = []
            if category not in levels:
                return btns

            cat_levels = levels[category]

            cols = 4
            start_x = sw // 2 - (cols * (LEVEL_BUTTON_SIZE + BUTTON_SPACING)) // 2

            for i, level_info in enumerate(cat_levels):
                row = i // cols
                col = i % cols

                locked = not is_level_unlocked(
                    level_info["id"], LEVELS, completed_levels
                )
                btn_image = level_locked_img if locked else level_unlocked_img

                def make_on_click(info):
                    def on_click():
                        self.start_level(win, info)
                        nonlocal completed_levels, active_buttons
                        completed_levels = load_save().get("completed_levels", [])
                        active_buttons = create_level_buttons(current_category)
                    return on_click

                btn = Button(
                    x=start_x + col * (LEVEL_BUTTON_SIZE + BUTTON_SPACING),
                    y=200 + row * (LEVEL_BUTTON_SIZE + BUTTON_SPACING),
                    width=LEVEL_BUTTON_SIZE,
                    height=LEVEL_BUTTON_SIZE,
                    text=str(i + 1),
                    image=btn_image,
                    text_color=(55, 51, 49),
                    on_click=make_on_click(level_info) if not locked else lambda: None,
                )
                btn.set_font(font_size=50, bold=True)
                btns.append(btn)
            return btns

        def set_category(cat):
            nonlocal current_category, active_buttons
            current_category = cat
            active_buttons = create_level_buttons(cat)

        active_buttons = create_category_buttons()

        while self.run_levels:
            clock.tick(FPS)
            win.fill((52, 48, 46))

            sw, sh = win.get_size()

            # Draw Title
            title_text = (
                "Select Category"
                if current_category is None
                else f"{current_category.capitalize()} Levels"
            )
            font = pygame.font.Font(FONT_PATH, 50)
            title_surf = font.render(title_text, True, (255, 255, 255))
            win.blit(title_surf, (sw // 2 - title_surf.get_width() // 2, 50))

            back_btn.handle_event()
            back_btn.update()
            back_btn.draw(win)

            for btn in active_buttons:
                btn.handle_event()
                btn.update()

                # Draw rounded border for category buttons
                if current_category is None:
                    # Draw a white rounded border if hovered, otherwise light gray
                    border_color = (255, 255, 255) if btn.hovered else (200, 200, 200)
                    border_rect = pygame.Rect(
                        btn.x - 5, btn.y - 5, btn.width + 10, btn.height + 10
                    )
                    pygame.draw.rect(
                        win, border_color, border_rect, width=3, border_radius=15
                    )

                btn.draw(win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    sw, sh = event.size
                    win = pygame.display.set_mode((sw, sh), pygame.RESIZABLE)
                    if current_category is None:
                        active_buttons = create_category_buttons()
                    else:
                        active_buttons = create_level_buttons(current_category)

            pygame.display.flip()

    def start_level(self, win, level_info):
        menuBG.stop()
        maper = TiledMap(level_info["path"])
        Level(maper, level_id=level_info["id"]).draw()
        menuBG.play(-1)
