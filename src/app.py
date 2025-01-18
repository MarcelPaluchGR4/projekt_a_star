from tkinter import messagebox

import customtkinter as ctk

from a_star import Astar

MAP_HEIGHT = 20
MAP_WIDTH = 20

PASSABLE_COLOR = "#1F6AA5"
BLOCKED_COLOR = "red"
CRUSHABLE_COLOR = "yellow"
PATH_COLOR = "purple"
VISITED_COLOR = "gray"


class App(ctk.CTk):
    def __init__(self, fg_color=None, **kwargs) -> None:
        super().__init__(fg_color, **kwargs)
        ctk.set_appearance_mode("dark")
        self.create_frames()
        self.create_default_grid()
        self.create_buttons()
        self.a_star = Astar()
        self.color_buttons()

    def color_buttons(self) -> None:
        self.color_visited()
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if self.a_star.grid[i][j] == 5:
                    self.buttons[i][j].configure(fg_color=BLOCKED_COLOR)
                elif self.a_star.grid[i][j] == 4:
                    self.buttons[i][j].configure(fg_color=CRUSHABLE_COLOR)
                elif self.a_star.grid[i][j] == 3:
                    self.buttons[i][j].configure(fg_color=PATH_COLOR)
                else:
                    self.buttons[i][j].configure(fg_color=PASSABLE_COLOR)

    def create_frames(self) -> None:
        self.grid_frame = ctk.CTkFrame(self)
        self.buttons_frame = ctk.CTkFrame(self)
        self.grid_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
        self.buttons_frame.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

    def create_default_grid(self) -> None:
        self.buttons = []
        for i in range(MAP_WIDTH):
            row_buttons = []
            for j in range(MAP_HEIGHT):
                button = ctk.CTkButton(
                    master=self.grid_frame,
                    text="",
                    width=40,
                    height=40,
                    corner_radius=0,
                    command=lambda x=i, y=j: self.change_color(x, y),
                )
                button.grid(row=i, column=j, padx=1, pady=1)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        self.set_default_start_and_finish()

    def set_default_start_and_finish(self) -> None:
        self.buttons[-1][0].configure(text="S")
        self.buttons[0][-1].configure(text="F")

    def change_color(self, row: int, col: int) -> None:
        if (self.buttons[row][col].cget("fg_color")) == BLOCKED_COLOR:
            self.buttons[row][col].configure(fg_color=CRUSHABLE_COLOR)
            self.a_star.grid[row][col] = 4
        elif (self.buttons[row][col].cget("fg_color")) == CRUSHABLE_COLOR:
            self.buttons[row][col].configure(fg_color=PASSABLE_COLOR)
            self.a_star.grid[row][col] = 0
        else:
            self.buttons[row][col].configure(fg_color=BLOCKED_COLOR)
            self.a_star.grid[row][col] = 5

    def create_buttons(self) -> None:
        self.reset_button = ctk.CTkButton(
            self.buttons_frame,
            text="Reset",
            command=self.reset,
            corner_radius=0,
        )
        self.find_path_button = ctk.CTkButton(
            self.buttons_frame,
            text="Find Path",
            command=self.find_path,
            corner_radius=0,
        )

        self.reset_button.grid(row=98, column=0, padx=10, pady=10, sticky="NSEW")
        self.find_path_button.grid(row=99, column=0, padx=10, pady=10, sticky="NSEW")

    def find_path(self) -> None:
        self.a_star.get_path(self.buttons)

        self.color_buttons()
        if self.a_star.crushed_walls > 0:
            messagebox.showinfo(
                title="info",
                message=f"Crushed walls: {self.a_star.crushed_walls}, \n at: {self.a_star.crushed_walls_location}",
            )

    def color_visited(self) -> None:
        reversed_list = self.a_star.visited_list
        # reversed_list.reverse()
        for item in reversed_list:
            i, j = item
            self.buttons[i][j].configure(fg_color=VISITED_COLOR)
            self.update()
            self.after(25)

    def reset(self) -> None:
        self.a_star = Astar()
        self.color_buttons()


root = App()
root.mainloop()
