import pygame

from gui.text import Text

class InputText():
    """Class InputText

    Class to representation of text area in interface
    """

    def __init__(self, width, height, pos_x, pos_y, font_size):
        """Init method

        Args:
            width (int): width of text input
            height (int): height of text input
            pos_x (int): x position of text input
            pos_y (int): y position of text input
            font_size (int): font size of text
        """

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.active = False

        self.bg_color = (240, 240, 240)
        self.bg_color_active = (255, 255, 255)

        self.pos = (pos_x, pos_y)

        self.text = Text("", (0, 0, 0), font_size=font_size)
        self.set_text()
        self.update()

    def set_text(self):
        """Method to set text in text input
        """

        text_width, text_height = self.text.text_rendered.get_size()

        margin_x = self.rect.x + (self.rect.width - text_width) // 2
        margin_y = self.rect.y + (self.rect.height - text_height) // 2

        self.text.set_pos(margin_x, margin_y)

    def click(self):
        """Click method
        """

        if self.rect.collidepoint(self.mouse):
            self.active = not self.active
        else:
            self.active = False

    def update(self):
        """Update method
        """

        self.text.update()
        self.set_text()
        self.mouse = pygame.mouse.get_pos()

        if self.active:
            self.image.fill(self.bg_color_active)
        else:
            self.image.fill(self.bg_color)


    def handle_event(self, event):
        """Method to handle typing or mouse clicking

        Args:
            event (pygame.event): event
        """

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text.text = self.text.text[:-1]
                else:
                    self.text.text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click()

    def draw(self, screen):
        """Method to draw button on interface

        Args:
            screen (pygame.display): interface
        """
        screen.blit(self.image, self.rect)
        self.text.draw(screen)

    def get_text(self):
        """Text getter

        Returns:
            str: contents of text input
        """

        return self.text.text

    def set_background_color(self, color):
        """Background color setter

        Args:
            color (tuple): color
        """
        
        self.bg_color = color
