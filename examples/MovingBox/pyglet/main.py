"""
    Simple example game where in you can move a box around by using the arrow keys and resize it using the mouse.

    Python: 3.6.3
    Author: hyarsan
    https://github.com/hyarsan
"""

import pyglet
from pyglet.window import key, mouse

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup variables for handling input.
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.mouse = [0, 0]

        # Setup main variables.
        self.boxX, self.boxY = (self.width / 2), (self.height / 2)
        self.boxSize = 25
        self.boxSizeMin = 5
        self.boxSizeMax = 100
        self.boxSpeed = 5

        # Check for arrows keys and update the cursor every frame.
        pyglet.clock.schedule(self.moveBox)
        pyglet.clock.schedule(self.updateCur)

    def drawRect(self, x, y, dx, dy):
        # Draws a rectangle from x, y to dx, dy.
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ("v2f", [x, y, dx, y, dx, dy, x, dy]))

    def drawLine(self, x, y, dx, dy):
        # Draws a blue line from x, y to dx, dy.
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2f", [x, y, dx, dy],), ("c3B", [0, 0, 255, 0, 0, 255]))

    def moveBox(self, dt):
        # Arrow keys move the box if it doesn't touch the edge.
        if self.keys[key.UP] and self.boxY < self.height - self.boxSize:
            self.boxY += self.boxSpeed

        if self.keys[key.DOWN] and self.boxY > 0 + self.boxSize:
            self.boxY -= self.boxSpeed

        if self.keys[key.LEFT] and self.boxX > 0 + self.boxSize:
            self.boxX -= self.boxSpeed

        if self.keys[key.RIGHT] and self.boxX < self.width - self.boxSize:
            self.boxX += self.boxSpeed

    def updateCur(self, dt):
        # Changes mouse cursor to hand if hovering the box, shows stop cursor if it can't get bigger or smaller.
        if self.mouse[0] >= self.boxX - self.boxSize and self.mouse[0] <= self.boxX + self.boxSize:
            if self.mouse[1] >= self.boxY - self.boxSize and self.mouse[1] <= self.boxY + self.boxSize:
                if self.boxSize != self.boxSizeMin and self.boxSize != self.boxSizeMax:
                    self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_HAND))
                else:
                    self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_NO))
            else:
                self.set_mouse_cursor()
        else:
            self.set_mouse_cursor()

    def on_mouse_motion(self, x, y, dx, dy):
        # Update mouse cursor location variable if the mouse is being moved.
        self.mouse[0] += dx
        self.mouse[1] += dy

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # Update mouse cursor location variable if the mouse is dragging.
        self.mouse[0] += dx
        self.mouse[1] += dy

    def on_mouse_press(self, x, y, button, modifiers):
        # Left click makes the box bigger, right click makes it smaller.
        if self.mouse[0] >= self.boxX - self.boxSize and self.mouse[0] <= self.boxX + self.boxSize:
            if self.mouse[1] >= self.boxY - self.boxSize and self.mouse[1] <= self.boxY + self.boxSize:
                if button == mouse.RIGHT:
                    if self.boxSize != self.boxSizeMin:
                        self.boxSize -= 5
                elif button == mouse.LEFT:
                    if self.boxSize != self.boxSizeMax:
                        self.boxSize += 5

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # Scrolling up makes the box bigger, scrolling down makes it smaller.
        if self.mouse[0] >= self.boxX - self.boxSize and self.mouse[0] <= self.boxX + self.boxSize:
            if self.mouse[1] >= self.boxY - self.boxSize and self.mouse[1] <= self.boxY + self.boxSize:
                if scroll_y <= -1:
                    if self.boxSize != self.boxSizeMin:
                        self.boxSize -= 5
                elif scroll_y >= 1:
                    if self.boxSize != self.boxSizeMax:
                        self.boxSize += 5

    def on_draw(self):
        self.clear()
        # Draws rectangle around x and y.
        self.drawRect(self.boxX - self.boxSize, self.boxY - self.boxSize, self.boxX + self.boxSize, self.boxY + self.boxSize)

        # Set line width to 3.
        pyglet.gl.glLineWidth(3)
        # Draws a line from the top left corner of the rectangle, to the bottom right corner.
        self.drawLine(self.boxX + self.boxSize, self.boxY - self.boxSize, self.boxX - self.boxSize, self.boxY + self.boxSize)
        # Same but with top right to bottom left.
        self.drawLine(self.boxX - self.boxSize, self.boxY - self.boxSize, self.boxX + self.boxSize, self.boxY + self.boxSize)

if __name__ == "__main__":
    window = Window(caption = "Moving Box")
    pyglet.app.run()
