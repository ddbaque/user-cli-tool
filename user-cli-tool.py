#!/usr/bin/env python3
import curses
import os
import subprocess


class MenuDisplay:
    def __init__(self, menu):
        # set menu parameter as class property
        self.menu = menu
        self.current_y = 1
        # run curses application
        curses.wrapper(self.mainloop)

    def mainloop(self, stdscr):
        # turn off cursor blinking
        curses.curs_set(0)

        # color scheme for selected row
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        # set screen object as class property
        self.stdscr = stdscr

        # get screen height and width
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()

        # specify the current selected row
        current_row = 0

        # print the menu
        self.print_menu(current_row)

        while 1:
            key = self.stdscr.getch()

            if (key == curses.KEY_UP or key == ord("k")) and current_row > 0:
                current_row -= 1
            elif (key == curses.KEY_DOWN or key == ord("j")) and current_row < len(
                self.menu
            ) - 1:
                current_row += 1
            elif (
                key == curses.KEY_ENTER or key == curses.KEY_RIGHT or key == ord("l")
            ) or key in [10, 13]:
                self.print_center("You selected '{}'".format(self.menu[current_row]))

                # If user selected "Create User"
                if current_row == 0:
                    self.handle_create_user()
                    # if user selected last row (Exit), confirm before exit the program
                elif current_row == 1:
                    self.handle_delete_user()
                elif current_row == len(self.menu) - 1:
                    if self.confirm("Are you sure you want to exit?"):
                        break

                self.stdscr.getch()

            self.print_menu(current_row)

    def print_incremental(self, text):
        if self.current_y == 1:
            self.stdscr.clear()
        x = 2  # Fixed x position
        # Print at the current position
        self.stdscr.addstr(self.current_y, x, text)
        self.current_y += 1  # Move to the next line for subsequent calls
        self.stdscr.refresh()

    def print_menu(self, selected_row_idx):
        self.current_y = 1
        self.stdscr.clear()

        # Calculate starting point for vertical alignment
        self.current_y = 1
        start_y = 1

        for idx, row in enumerate(self.menu):
            # Align all options to the left (column 0)
            x = 2  # Start at the leftmost position
            y = start_y + idx  # Vertically centered

            if idx == selected_row_idx:
                row = "> " + row  # Add ">" before the selected option
                self.color_print(y, x, row, 1)
            else:
                self.stdscr.addstr(y, x, row)

        self.stdscr.refresh()

    def color_print(self, y, x, text, pair_num):
        self.stdscr.attron(curses.color_pair(pair_num))
        self.stdscr.addstr(y, x, text)
        self.stdscr.attroff(curses.color_pair(pair_num))

    def print_confirm(self, selected="yes"):
        # clear yes/no line
        curses.setsyx(self.screen_height // 2 + 1, 0)
        self.stdscr.clrtoeol()

        y = self.screen_height // 2 + 1
        options_width = 10

        # print yes
        option = "yes"
        x = self.screen_width // 2 - options_width // 2 + len(option)
        if selected == option:
            self.color_print(y, x, option, 1)
        else:
            self.stdscr.addstr(y, x, option)

        # print no
        option = "no"
        x = self.screen_width // 2 + options_width // 2 - len(option)
        if selected == option:
            self.color_print(y, x, option, 1)
        else:
            self.stdscr.addstr(y, x, option)

        self.stdscr.refresh()

    def confirm(self, confirmation_text):
        self.print_center(confirmation_text)

        current_option = "yes"
        self.print_confirm(current_option)

        while 1:
            key = self.stdscr.getch()

            if (key == curses.KEY_RIGHT or key == ord("l")) and current_option == "yes":
                current_option = "no"
            elif (key == curses.KEY_LEFT or key == ord("h")) and current_option == "no":
                current_option = "yes"
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return True if current_option == "yes" else False

            self.print_confirm(current_option)

    def print_center(self, text):
        self.stdscr.clear()
        x = 2
        y = 1
        self.stdscr.addstr(y, x, text)
        self.stdscr.refresh()

    def get_user_input(self, prompt):
        # Clear screen and print prompt
        self.stdscr.clear()
        self.print_center(prompt)

        # Define input box
        curses.curs_set(1)  # Enable cursor for input
        self.stdscr.refresh()

        # Get user input (allowing up to 30 characters)
        input_str = ""
        while True:
            key = self.stdscr.getch()

            if key == curses.KEY_BACKSPACE or key == 127:
                # Remove the last character
                input_str = input_str[:-1]
                self.stdscr.clear()
                self.print_center(prompt + input_str)
            elif key == 10 or key == 13:  # Enter key
                break
            elif 32 <= key <= 126:  # Printable characters
                input_str += chr(key)
                self.stdscr.clear()
                self.print_center(prompt + input_str)

            self.stdscr.refresh()

        curses.curs_set(0)  # Disable cursor after input
        return input_str

    def handle_create_user(self):
        username = self.get_user_input("Enter username: ")
        group = self.get_user_input("Enter group: ")
        self.print_center(f"Username: {username} | Group:{group}")
        if self.confirm("You want to add a secondary group?"):
            second_group = self.get_user_input("Enter secondary group: ")
            self.create_user(username, group, second_group)

        else:
            self.create_user(username, group)

    def create_user(self, username, primary_group, secondary_group=None):
        try:
            # Check if the primary group exists, and create it if it doesn't
            subprocess.run(
                ["getent", "group", primary_group],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            self.print_incremental(f"The group '{primary_group}' already exists.")
        except subprocess.CalledProcessError:
            self.print_incremental(f"Creating the group '{primary_group}'...")
            subprocess.run(["groupadd", primary_group], check=True)
            self.print_incremental(f"Group '{primary_group}' created.")

        # Ensure the folder /home/<primary_group> exists
        primary_group_directory = f"/home/{primary_group}"
        if not os.path.exists(primary_group_directory):
            self.print_incremental(
                f"Creating the group directory: {primary_group_directory}..."
            )
            os.makedirs(primary_group_directory, exist_ok=True)
            subprocess.run(
                ["chown", f"{primary_group}:{primary_group}", primary_group_directory],
                check=True,
            )
            self.print_incremental(
                f"Directory {primary_group_directory} created and assigned to group '{primary_group}'."
            )

        if secondary_group:
            try:
                # Check if the secondary group exists, and create it if it doesn't
                subprocess.run(
                    ["getent", "group", secondary_group],
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
                self.print_incremental(
                    f"The secondary group '{secondary_group}' already exists."
                )
            except subprocess.CalledProcessError:
                self.print_incremental(
                    f"Creating the secondary group '{secondary_group}'..."
                )
                subprocess.run(["groupadd", secondary_group], check=True)
                self.print_incremental(f"Secondary group '{secondary_group}' created.")

        try:
            # Create the user and assign their home directory under /home/<primary_group>
            user_home = f"{primary_group_directory}/{username}"
            self.print_incremental(
                f"Creating the user '{username}' with home directory '{user_home}'..."
            )

            # Build the useradd command
            command = [
                "useradd",
                "-m",  # Create the user's home directory
                "-d",
                user_home,  # Specify the home directory
                "-g",
                primary_group,  # Assign the primary group
                "-s",
                "/bin/bash",  # Set the shell to bash
            ]

            # Add the secondary group if provided
            if secondary_group:
                command.extend(["-G", secondary_group])

            command.append(username)
            subprocess.run(command, check=True)

            self.print_incremental(
                f"User '{username}' successfully created with home directory '{user_home}'."
            )
            if secondary_group:
                self.print_incremental(
                    f"User '{username}' added to secondary group '{secondary_group}'."
                )
        except subprocess.CalledProcessError as e:
            self.print_incremental(f"Error creating the user '{username}': {e}")

    def handle_delete_user(self):
        username = self.get_user_input("Enter username to delete: ")
        if self.confirm(f"Are you looking to delete the user {username}?"):
            self.delete_user(username)

    def delete_user(self, username):
        try:
            # Check if the user exists
            subprocess.run(
                ["id", username],
                check=True,
                stdout=subprocess.DEVNULL,
            )

            # Run the userdel -r command without sudo
            subprocess.run(
                ["userdel", "-r", username],
                check=True,
                stdout=subprocess.DEVNULL,
            )

            self.print_incremental(f"User '{username}' deleted successfully.")

        except Exception as e:
            self.print_incremental(f"Exception while trying to delete user: {str(e)}")


if __name__ == "__main__":
    menu = ["Create User", "Delete User", "Exit"]
    MenuDisplay(menu)
