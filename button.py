import pygame

class Button():
    def __init__(self, width, height, pos_x, pos_y, text, action, color=(80, 80, 80), hover_color=(35, 35, 35)):
        self.color = color
        self.hover_color = hover_color

        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.action = action

        self.set_text(text)
        self.update()

    def set_text(self, text):
        self.text = text
        text_width, text_height = text.text_rendered.get_size()

        margin_x = self.rect.x + (self.rect.width - text_width) // 2
        margin_y = self.rect.y + (self.rect.height - text_height) // 2

        text.set_pos(margin_x, margin_y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click()

    def update(self):
        self.mouse = pygame.mouse.get_pos()

        if self.rect.left <= self.mouse[0] <= self.rect.right and self.rect.top <= self.mouse[1] <= self.rect.bottom:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.image.fill(self.hover_color)

        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.image.fill(self.color)

    def click(self):
        if self.rect.collidepoint(self.mouse):
            self.action()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.text.draw(screen)
