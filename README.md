# AI Agent for Tic-Tac-Toe Game

A modern Tic Tac Toe game built with [Flet](https://flet.dev/) in Python features an unbeatable AI opponent that uses the Minimax algorithm with alpha-beta pruning. You can play against the AI in your browser or as a desktop application!

## Features

- **Unbeatable AI:** Uses Minimax algorithm with alpha-beta pruning.
- **Modern UI:** Built with Flet for a clean, responsive interface.
- **Scoreboard:** Tracks wins, ties, and losses.
- **Play as X or O:** Choose who goes first.
- **Cross-platform:** Runs as a desktop app or in the browser.

## How to Play

- Choose whether you want to play first or let the AI start.
- Click on a cell to make your move.
- The AI will respond instantly.
- The scoreboard will update after each game.
- Click "New Game" to play again, or "Exit Game" to close the app (in web mode, you will be prompted to close the browser tab).

## Getting Started

### Prerequisites

- Python 3.9 or newer

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/ai-agent-tic-tac-toe.git
    cd ai-agent-tic-tac-toe
    ```

2. **Install dependencies:**
    ```sh
    pip install flet==0.27.6
    ```

## Run the app

### uv

Run as a desktop app:

```
uv run flet run
```

Run as a web app:

```
uv run flet run --web
```

### Poetry

Install dependencies from `pyproject.toml`:

```
poetry install
```

Run as a desktop app:

```
poetry run flet run
```

Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).

## References

- [Minimax Algorithm Blog](https://www.neverstopbuilding.com/blog/minimax)
- [Tic-Tac-Toe Agent using Alpha-Beta Pruning](https://medium.com/@amadi8/tic-tac-toe-agent-using-alpha-beta-pruning-18e8691b61d4)
- [Tic-Tac-Toe (UI Inspiration) on GitHub](https://github.com/soris2000/Tic-Tac-Toe)

**Made with ❤️ using [Flet](https://flet.dev/)**