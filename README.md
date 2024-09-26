# mg-soundboard - 100% Free

Welcome to the **mg-soundboard** project! This application is a free and customizable soundboard that allows you to manage and play audio files via keyboard shortcuts. It is designed to be easy to use and highly configurable.

## Features

- **Sound Management**: Easily add, remove, and edit sounds.
- **Keyboard Shortcuts**: Assign and modify keyboard shortcuts for each sound.
- **Customizable Settings**:
  - **Loop**: Set whether the sound should be repeated in a loop.
  - **Stop Other Sounds**: Choose whether to stop other sounds when this sound plays (default is True).
  - **Volume**: Adjust the volume of the sound (default is 100%).
  - **Active**: Enable or disable the sound.
- **Global Shortcuts**: Activate or deactivate global shortcut functionality.
- **Configuration Saving**: Settings and sounds are automatically saved and restored when the application is reopened.

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/Axel00x/mg-soundboard.git
    cd mg-soundboard
    ```

2. **Install Dependencies**:

    Ensure you have Python 3.x installed, then run:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file includes all necessary libraries:
    - `pygame`
    - `tkinter`
    - `keyboard`

## Usage

1. **Run the Application**:

    ("\dist\mg-soundboard_main.exe")[https://github.com/Axel00x/mg-soundboard/blob/main/dist/mg-soundboard_main.exe]

2. **User Interface**:

    - **Add Sound**: Click the "Add Sound" button to load a `.wav` audio file and assign a shortcut.
    - **Remove Sound**: Select a sound from the list and click "Remove Sound".
    - **Edit Sound**: Double-click a sound in the list to open an edit window.
    - **Settings**: Modify settings such as name, shortcut, loop, stop other sounds, volume, and active status of the sound.

3. **Keyboard Shortcuts**:

    - **Play Sound**: Press the key associated with the sound to play it.
    - **Stop All Sounds**: Press the `e` key to stop all currently playing sounds.

4. **Global Settings**:

    - **Shortcut**: Enable or disable global shortcut functionality via a checkbox in the main window.

## Configuration

Settings are automatically saved to a file named `config.json` in the same directory as the project. Changes made during use are applied and saved in real-time.

## Contributing

If you wish to contribute to the project, feel free to open a pull request or report issues through the [GitHub issue tracker](https://github.com/Axel00x/mg-soundboard/issues).

## License

This project is distributed under the [MIT License](LICENSE). It is completely free and open for community improvements.

---

Thank you for using **mg-soundboard**! I hope this application proves useful and that you enjoy the customization and features it offers.
