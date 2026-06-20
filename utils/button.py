import pygame

from load_data import FONT_PATH


class Button:
    """Enhanced button class with image support and press animations"""

    def __init__(
        self,
        x,
        y,
        width,
        height,
        on_click,
        text=None,
        image=None,
        idle_image=None,
        hover_image=None,
        pressed_image=None,
        icon=None,
        icon_size=None,
        press_animation=None,
        text_color=(255, 255, 255),
        idle_color=(200, 200, 200),
        hover_color=(255, 255, 255),
        pressed_color=(150, 150, 150),
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Text properties
        self.text = text
        self.text_color = text_color
        self.font_size = 36
        self.bold = False
        self.font = pygame.font.Font(FONT_PATH, self.font_size)
        self.text_surface = None
        if text:
            self.text_surface = self.font.render(self.text, True, self.text_color)

        # Background Image properties (state-based)
        # Support both single image (backward compatible) and state-specific images
        self.idle_image = idle_image
        self.hover_image = hover_image
        self.pressed_image = pressed_image
        self.image = image  # Fallback for backward compatibility

        # Scale all images to button size
        if self.idle_image:
            self.idle_image = pygame.transform.scale(self.idle_image, (width, height))
        if self.hover_image:
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        if self.pressed_image:
            self.pressed_image = pygame.transform.scale(
                self.pressed_image, (width, height)
            )
        if self.image:
            self.image = pygame.transform.scale(self.image, (width, height))

        # Icon properties (overlay on image)
        self.icon = icon
        self.icon_size = icon_size
        if self.icon and self.icon_size:
            self.icon = pygame.transform.scale(
                self.icon, (self.icon_size, self.icon_size)
            )
        elif self.icon:
            # Default icon size to 50% of button size
            default_size = int(min(width, height) * 0.5)
            self.icon = pygame.transform.scale(self.icon, (default_size, default_size))

        # State properties
        self.hovered = False
        self.pressed = False
        self.on_click = on_click

        # Color properties
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color

        # Animation properties
        self.press_animation = press_animation
        self.is_animating = False

    def set_font(self, font_size, bold=False):
        """Update font size and weight"""
        self.font_size = font_size
        self.bold = bold
        self.font = pygame.font.Font(FONT_PATH, self.font_size)
        self.font.set_bold(self.bold)
        if self.text:
            self.text_surface = self.font.render(self.text, True, self.text_color)

    def update(self):
        """Update button state and animations"""
        if self.press_animation and self.is_animating:
            self.press_animation.update()
            if self.press_animation.finished:
                self.is_animating = False

    def draw(self, screen):
        """Draw button with current state"""
        # Determine which background image to use based on state
        current_image = None
        if self.pressed and self.pressed_image:
            current_image = self.pressed_image
        elif self.hovered and self.hover_image:
            current_image = self.hover_image
        elif self.idle_image:
            current_image = self.idle_image
        elif self.image:
            current_image = self.image

        # Only draw background color if NO image is present
        # This makes colors transparent when images exist
        if not current_image:
            if self.pressed:
                color = self.pressed_color
            elif self.hovered:
                color = self.hover_color
            else:
                color = self.idle_color

            pygame.draw.rect(screen, color, self.rect)

        # Draw background image if available
        if current_image:
            screen.blit(current_image, (self.x, self.y))

        # Draw icon in the middle if available
        if self.icon:
            icon_x = self.x + self.width // 2 - self.icon.get_width() // 2
            icon_y = self.y + self.height // 2 - self.icon.get_height() // 2
            screen.blit(self.icon, (icon_x, icon_y))

        # Draw text if available (only if no icon, or on top)
        if self.text_surface and not self.icon:
            screen.blit(
                self.text_surface,
                (
                    self.x + self.width // 2 - self.text_surface.get_width() // 2,
                    self.y + self.height // 2 - self.text_surface.get_height() // 2,
                ),
            )

        # Draw press animation if active
        if self.press_animation and self.is_animating:
            self.press_animation.draw(
                screen,
                self.x
                + self.width // 2
                - self.press_animation.imageList[0].get_width() // 2,
                self.y
                + self.height // 2
                - self.press_animation.imageList[0].get_height() // 2,
            )

    def handle_event(self):
        """Handle mouse events"""
        mx, my = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        clicked = mouse_buttons[0]

        # Update hover state
        self.hovered = self.rect.collidepoint(mx, my)

        # Handle click
        if self.hovered and clicked:
            if not self.pressed:
                self.pressed = True
                self.on_click()

                # Start press animation if available
                if self.press_animation:
                    self.press_animation.reset()
                    self.is_animating = True
        else:
            self.pressed = False

    def set_text(self, text):
        """Update button text"""
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.text_color)

    def set_image(self, image):
        """Update button background image (all states)"""
        self.image = pygame.transform.scale(image, (self.width, self.height))

    def set_location(self, x, y):
        """Update button position"""
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def set_idle_image(self, image):
        """Update idle state background image"""
        self.idle_image = pygame.transform.scale(image, (self.width, self.height))

    def set_hover_image(self, image):
        """Update hover state background image"""
        self.hover_image = pygame.transform.scale(image, (self.width, self.height))

    def set_pressed_image(self, image):
        """Update pressed state background image"""
        self.pressed_image = pygame.transform.scale(image, (self.width, self.height))

    def set_state_images(self, idle_image, hover_image, pressed_image):
        """Update all state-specific images at once"""
        if idle_image:
            self.idle_image = pygame.transform.scale(
                idle_image, (self.width, self.height)
            )
        if hover_image:
            self.hover_image = pygame.transform.scale(
                hover_image, (self.width, self.height)
            )
        if pressed_image:
            self.pressed_image = pygame.transform.scale(
                pressed_image, (self.width, self.height)
            )

    def set_icon(self, icon, icon_size=None):
        """Update button icon (overlay on image/background)"""
        self.icon = icon
        if icon_size:
            self.icon = pygame.transform.scale(self.icon, (icon_size, icon_size))
        elif icon:
            # Default icon size to 50% of button size
            default_size = int(min(self.width, self.height) * 0.5)
            self.icon = pygame.transform.scale(self.icon, (default_size, default_size))


class IconButton(Button):
    """Button that displays an icon image centered"""

    def __init__(self, x, y, width, height, icon_image, on_click, scale_factor=0.7):
        super().__init__(x, y, width, height, on_click)
        self.scale_factor = scale_factor
        self.icon_image = icon_image
        if self.icon_image:
            icon_size = int(width * scale_factor)
            self.icon_image = pygame.transform.scale(
                self.icon_image, (icon_size, icon_size)
            )

    def draw(self, screen):
        """Draw icon button"""
        # Draw background
        if self.pressed:
            color = self.pressed_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.idle_color

        pygame.draw.rect(screen, color, self.rect)

        # Draw icon centered
        if self.icon_image:
            icon_rect = self.icon_image.get_rect(center=self.rect.center)
            screen.blit(self.icon_image, icon_rect)


class TextButton(Button):
    """Button optimized for text display"""

    def __init__(self, x, y, width, height, text, on_click, font_size=36, **kwargs):
        super().__init__(x, y, width, height, on_click, text=text, **kwargs)
        self.font = pygame.font.Font(FONT_PATH, font_size)
        self.text_surface = self.font.render(self.text, True, self.text_color)


class AnimatedButton(Button):
    """Button with animated background/state changes"""

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        on_click,
        idle_animation=None,
        hover_animation=None,
        **kwargs,
    ):
        super().__init__(x, y, width, height, on_click, text=text, **kwargs)
        self.idle_animation = idle_animation
        self.hover_animation = hover_animation
        self.current_animation = idle_animation

    def update(self):
        """Update animations"""
        super().update()

        # Switch animation based on state
        if self.hovered and self.hover_animation:
            if self.current_animation != self.hover_animation:
                self.current_animation = self.hover_animation
                self.hover_animation.reset()
        elif self.idle_animation:
            if self.current_animation != self.idle_animation:
                self.current_animation = self.idle_animation
                self.idle_animation.reset()

        if self.current_animation:
            self.current_animation.update()

    def draw(self, screen):
        """Draw animated button"""
        # Draw current animation frame as background
        if self.current_animation:
            self.current_animation.draw(screen, self.x, self.y)
        else:
            # Fallback to color
            if self.pressed:
                color = self.pressed_color
            elif self.hovered:
                color = self.hover_color
            else:
                color = self.idle_color
            pygame.draw.rect(screen, color, self.rect)

        # Draw text if available
        if self.text_surface:
            screen.blit(
                self.text_surface,
                (
                    self.x + self.width // 2 - self.text_surface.get_width() // 2,
                    self.y + self.height // 2 - self.text_surface.get_height() // 2,
                ),
            )
