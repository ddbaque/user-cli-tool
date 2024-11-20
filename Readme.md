
# User CLI Tool

## Description

This is an interactive command-line tool for managing users and groups on Unix/Linux systems. The tool uses the `curses` library to provide a terminal-based UI that allows you to create, delete, and manage users and groups. It's designed for ease of use and efficient user management directly from the terminal.

![menu](./menu.gif)

## Features

- Create users and assign them to primary and secondary groups.
- Delete users and remove their associated directories.
- Interactive terminal interface using `curses`.
- Simple and intuitive controls for navigating through options.

## Prerequisites

- Python 3.x
- `curses` library (usually pre-installed in most Unix-like systems)

## How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/user-cli-tool.git
   cd user-cli-tool
   ```

2. **Make the script executable:**

   You need to give execute permissions to the script:

   ```bash
   chmod +x user-cli-tool.py
   ```

3. **Run the script:**

   Once the script is executable, you can run it with:

   ```bash
   ./user-cli-tool.py
   ```

   The application will open a terminal interface where you can navigate the menu using the following controls:
   - **Up Arrow** or `k`: Move up the menu.
   - **Down Arrow** or `j`: Move down the menu.
   - **Enter** or `l`: Select the current option.

## Menu Options

- **Create User**: Create a new user and assign them to a group (with optional secondary group).
- **Delete User**: Delete an existing user.
- **Exit**: Exit the application.

