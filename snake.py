import customtkinter as ctk
from settings import *
from random import randint
from sys import exit


class Game(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__()
        self.title("Snake")
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")

        # layout
        self.columnconfigure(list(range(FIELDS[0])), weight=1, uniform="a")
        self.rowconfigure(list(range(FIELDS[1])), weight=1, uniform="a")

        # snake
        # A list of tuples with the initial body positions of the snake. These will be drawn on the fram with the draw() method we created below
        self.snake = [
            START_POS,
            (START_POS[0] - 1, START_POS[1]),
            (START_POS[0] - 2, START_POS[1]),
        ]
        self.direction = DIRECTIONS["right"]
        self.bind("<Key>", self.get_input)

        # Apple
        self.place_apple()

        # Score
        # Create a frame for score
        score_label = ctk.CTkLabel(
            self, text="Score:", anchor="ne", font=("Helvetica", 28)
        )
        score_label.place(relx=0.4, rely=0.05)
        self.score_int = ctk.IntVar(self, 0)
        score_int_label = ctk.CTkLabel(
            self, textvariable=self.score_int, anchor="ne", font=("Helvetica", 28)
        )
        score_int_label.place(relx=0.6, rely=0.05)

        # Draw Logic
        self.draw_frames = []
        self.animate()

        # run
        self.mainloop()

    def animate(self):
        # SNAKE UPDATE
        # Create new head: new_head = old_head +  direction
        new_head = (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1],
        )
        # We insert in the position we want the new head (at index 0)
        self.snake.insert(0, new_head)
        # Remove Tail

        # APPLE COLLISION
        if self.snake[0] == self.apple_pos:
            self.place_apple()
            self.score_int.set(self.score_int.get() + 1)
        else:
            # We just use the pop method to get the last item of the list ( this is a queue)
            # We only want to pop if we do not eat the apple
            self.snake.pop()

        # GAME OVER
        self.check_game_over()

        # DRAWING
        # Draw is here because it now needs to rerun and udpate every 250 ms
        self.draw()
        # Rerun method
        self.after(250, self.animate)

    def check_game_over(self):
        snake_head = self.snake[0]
        if (
            snake_head[0] >= RIGHT_LIMIT
            or snake_head[0] < LEFT_LIMIT
            or snake_head[1] < TOP_LIMIT
            or snake_head[1] >= BOTTOM_LIMIT
            or snake_head in self.snake[1:]
        ):
            self.destroy()
            exit()

    def get_input(self, event):
        # Keycode we get from the keycode properties of the pressed key
        match event.keycode:
            case 37:
                self.direction = (
                    DIRECTIONS["left"]
                    if self.direction != DIRECTIONS["right"]
                    else self.direction
                )
            case 38:
                self.direction = (
                    DIRECTIONS["up"]
                    if self.direction != DIRECTIONS["down"]
                    else self.direction
                )
            case 39:
                self.direction = (
                    DIRECTIONS["right"]
                    if self.direction != DIRECTIONS["left"]
                    else self.direction
                )
            case 40:
                self.direction = (
                    DIRECTIONS["down"]
                    if self.direction != DIRECTIONS["up"]
                    else self.direction
                )

    def place_apple(self):
        self.apple_pos = (randint(0, FIELDS[0] - 1), randint(0, FIELDS[1] - 1))

    def draw(self):
        # Forget all frames we need this because if not the snake will keep on growing
        if self.draw_frames:
            for frame, pos in self.draw_frames:
                frame.grid_forget()

            # Empty draw_frames
            self.draw_frames.clear()

        # Create a frame for the apple and append to the draw_frames list
        apple_frame = ctk.CTkFrame(
            self,
            fg_color=APPLE_COLOR,
            corner_radius=50,
        )
        self.draw_frames.append((apple_frame, self.apple_pos))

        # Create a frame for each swuare body part of snake, use enumerate to assign an index and a position tuple (col, row)
        for index, pos in enumerate(self.snake):
            # Assign color based on the index position of body part,
            color = SNAKE_BODY_COLOR if index != 0 else SNAKE_HEAD_COLOR
            # Create Frame for each part body of snake
            snake_frame = ctk.CTkFrame(self, fg_color=color, corner_radius=0)
            # Append Snake frame to draw_Frames list
            self.draw_frames.append((snake_frame, pos))

        # For each frame assign position to corresponding column
        for frame, pos in self.draw_frames:
            frame.grid(column=pos[0], row=pos[1])


# Good Practice to add this so it doesnt run any other code from other files
if __name__ == "__main__":
    Game()


############################################# NOTES #############################################

# 1- apple_pos is an instance variable of the Game class. It is initialized in the __init__ method when
#    an instance of the Game class is created. Since draw is a method of the Game class, it has access
#    to all the instance variables of that class, including apple_pos.

# 2- The purpose of this block:
#
# 		if self.draw_frames:
# 			for frame, pos in self.draw_frames:
# 				frame.grid_forget()
#
#  	  is to clear the previous visualization of the snake and apple on the game grid. When the snake moves,
#     the frames representing its body and the apple need to be repositioned on the grid. Before doing so,
#     the existing frames from the previous iteration need to be forgotten to avoid visual artifacts and
#     to ensure that the new frames are placed correctly.
#
#     The grid_forget() method removes the widget from the grid but does not destroy the widget itself.
#     This allows you to update the visualization by creating new frames for the snake and apple without
#     having to destroy and recreate the entire grid.
#
# 		self.draw_frames.clear()
#
#    This line clears the draw_frames list after using its contents. The draw_frames list is a list of tuples,
#    where each tuple contains a frame and its position. After the frames are forgotten with grid_forget(),
#    there's no need to keep these tuples in the list. Clearing the list ensures that it is ready to be populated
#    with new tuples in the next iteration of the draw method.
