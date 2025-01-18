from random import randint

import customtkinter as ctk

from a_star import Astar

MAP_HEIGHT = 20
MAP_WIDTH = 20


class App(ctk.CTk):
    ratio = 0.2

    def __init__(self, fg_color=None, **kwargs) -> None:
        super().__init__(fg_color, **kwargs)
        ctk.set_appearance_mode("dark")
        self.create_frames()
        self.create_default_grid()
        self.create_buttons()

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

    def change_color(self, row, col):
        if (self.buttons[row][col].cget("fg_color")) == "red":
            self.buttons[row][col].configure(fg_color="#1F6AA5")
        else:
            self.buttons[row][col].configure(fg_color="red")

    def set_ratio(self, value: float) -> None:
        App.ratio = value

    def create_buttons(self) -> None:
        self.reset_button = ctk.CTkButton(
            self.buttons_frame,
            text="Reset",
            command=self.create_default_grid,
            corner_radius=0,
        )
        self.find_path_button = ctk.CTkButton(
            self.buttons_frame,
            text="Find Path",
            command=lambda x=self.buttons: Astar(x),
            corner_radius=0,
        )

        self.reset_button.grid(row=98, column=0, padx=10, pady=10, sticky="NSEW")
        self.find_path_button.grid(row=99, column=0, padx=10, pady=10, sticky="NSEW")

    def randomize_map(self) -> None:
        self.create_default_grid()
        total_elements = MAP_HEIGHT * MAP_WIDTH
        number_of_unpassable = int(total_elements * App.ratio)
        for _ in range(number_of_unpassable):
            self.buttons[randint(0, MAP_WIDTH - 1)][
                randint(0, MAP_HEIGHT - 1)
            ].configure(fg_color="red")


root = App()
root.mainloop()
