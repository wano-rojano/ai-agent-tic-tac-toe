import flet as ft
import asyncio
import math, copy, random

# Constants of the game
X = "X"
O = "O"
T = "Tie"
EMPTY = None
N = 3
BOARD_BG = "#282a36"

class TicTacToe(ft.Column):
    """
    Main TicTacToe game class. Handles UI, game logic, and user/AI interactions.
    """
    def __init__(self, page):
        """
        Initialize the game state, UI components, and dialogs.
        """
        super().__init__()
        self.page = page
        self.ai_marker = ""
        self.ai_icon_name = ""
        self.ai_icon_color = ""
        self.ai_score = 0
        self.ai_tally = ft.Text("0", size=25)
        self.ai_icon = ft.Icon()
        self.ai_turn = ft.Container(height=10, width=100, border_radius=3, visible=False)
        self.player_marker = ""
        self.player_icon_name = ""
        self.player_icon_color = ""
        self.player_score = 0
        self.player_tally = ft.Text("0", size=25)
        self.player_icon = ft.Icon()
        self.player_turn = ft.Container(height=10, width=100, border_radius=3, visible=False)
        self.ties_score = 0
        self.ties_tally = ft.Text("0", size=25)
        self.board_state = [[EMPTY for _ in range(N)] for _ in range(N)]
        self.winning_marker_combinations = (
            ((0, 0), (0, 1), (0, 2)),
            ((1, 0), (1, 1), (1, 2)),
            ((2, 0), (2, 1), (2, 2)),
            ((0, 0), (1, 0), (2, 0)),
            ((0, 1), (1, 1), (2, 1)),
            ((0, 2), (1, 2), (2, 2)),
            ((0, 0), (1, 1), (2, 2)),
            ((0, 2), (1, 1), (2, 0))
        )
        self.marker_combination = tuple()
        self.player_first = True
        self.previous_winner = None
        self.initial_move_ai = False

        # UI elements and dialogs
        self.start = ft.AlertDialog(
            bgcolor="#21222c",
            title=ft.Text(
                value="",
                color="#f8f8f2",
                text_align=ft.TextAlign.CENTER
            )
        )

        self.game_ends = ft.AlertDialog(
            bgcolor="#21222c",
            modal=True,
            title=ft.Text(
                value="",
                color="#f8f8f2",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton("New Game", on_click=self.new_game),
                ft.TextButton("Exit Game", on_click=self.confirm_exit_game),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.exit_dialog = ft.AlertDialog(
            bgcolor="#21222c",
            modal=True,
            title=ft.Text(
                value="Are you sure you want to exit?",
                color="#f8f8f2",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.close_exit_dialog()),
                ft.TextButton("Exit", on_click=self.exit_game),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.title = ft.Text(
            value="Tic Tac Toe",
            size=40,
            color="#f8f8f2",
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD
        )

        self.board = ft.GridView(
            width=300,
            height=300,
            runs_count=N,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
            controls=[
                ft.Container(bgcolor=BOARD_BG, border_radius=2.5, on_click=self.player_marks, data=i)
                for i in range(N * N)
            ]
        )

        self.score_board = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self.ai_tally,
                        ft.Row(
                            [
                                self.ai_icon,
                                ft.Text("AI")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER),
                        self.ai_turn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        self.ties_tally,
                        ft.Text("TIES"),
                        ft.Container(height=10, width=100)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        self.player_tally,
                        ft.Row(
                            [
                                self.player_icon,
                                ft.Text("PLAYER")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        self.player_turn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            spacing=0,
            width=300,
            height=100,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = [
            self.title,
            self.board,
            self.score_board
        ]
        self.ask_player_first()

    def ask_player_first(self):
        """
        Prompts the user if they want to play first.
        """
        async def set_player_first(e):
            """
            Handler for when the user chooses to play first.
            """
            game_starts.open = False
            self.page.update()
            self.player_first = True
            self.initial_move_ai = False
            await self.start_game()

        async def set_ai_first(e):
            """
            Handler for when the user chooses the AI to play first.
            """
            game_starts.open = False
            self.page.update()
            self.player_first = False
            self.initial_move_ai = True
            await self.start_game()

        game_starts = ft.AlertDialog(
            bgcolor="#21222c",
            modal=True,
            title=ft.Text(
                value="Do you want to play first?",
                color="#f8f8f2",
                text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton("No", on_click=set_ai_first),
                ft.TextButton("Yes", on_click=set_player_first)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(game_starts)
        game_starts.open = True
        self.page.update()

    async def start_game(self):
        """
        Set up the game state and UI for a new game, depending on who plays first.
        """
        await asyncio.sleep(0.5)
        if self.player_first:
            self.player_marker = X
            self.player_icon_name = ft.Icons.CLOSE
            self.player_icon.name = self.player_icon_name
            self.player_icon_color = "#ff79c6"
            self.player_icon.color = self.player_icon_color
            self.player_turn.bgcolor = self.player_icon_color
            self.ai_marker = O
            self.ai_icon_name = ft.Icons.CIRCLE_OUTLINED
            self.ai_icon.name = self.ai_icon_name
            self.ai_icon_color = "#8be9fd"
            self.ai_icon.color = self.ai_icon_color
            self.ai_turn.bgcolor = self.ai_icon_color
            self.page.overlay.append(self.start)
            self.start.title.value = "Player plays first"
            self.start.open = True
            self.page.update()
            await asyncio.sleep(1)
            self.start.open = False
            self.title.color = "#f8f8f2"
            self.page.update()
        else:
            self.player_marker = O
            self.player_icon_name = ft.Icons.CIRCLE_OUTLINED
            self.player_icon.name = self.player_icon_name
            self.player_icon_color = "#8be9fd"
            self.player_icon.color = self.player_icon_color
            self.player_turn.bgcolor = self.player_icon_color
            self.ai_marker = X
            self.ai_icon_name = ft.Icons.CLOSE
            self.ai_icon.name = self.ai_icon_name
            self.ai_icon_color = "#ff79c6"
            self.ai_icon.color = self.ai_icon_color
            self.ai_turn.bgcolor = self.ai_icon_color
            self.page.overlay.append(self.start)
            self.start.title.value = "AI plays first"
            self.start.open = True
            self.page.update()
            await asyncio.sleep(1)
            self.start.open = False
            self.title.color = "#f8f8f2"
            self.page.update()
            await self.ai_marks()

    def terminal(self, board):
        """
        Check if the game is over (win or tie).
        """
        return self.check_winner(board) is not None

    def utility(self, board, depth):
        """
        Return the utility value of the board for minimax.
        """
        winner = self.check_winner(board)
        if winner == self.ai_marker:
            return 10 - depth
        elif winner == self.player_marker:
            return depth - 10
        else:
            return 0

    def check_winner(self, board):
        """
        Check for a winner or tie on the board.
        """
        for marker_combination in self.winning_marker_combinations:
            x, y, z = marker_combination
            if board[x[0]][x[1]] == board[y[0]][y[1]] == board[z[0]][z[1]] != None:
                self.marker_combination = marker_combination
                return board[x[0]][x[1]]
        if all(cell is not None for row in board for cell in row):
            return T
        return None

    def minimax(self, board, depth, maximizing_ai, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning for AI move selection.
        """
        if self.terminal(board):
            return self.utility(board, depth), None

        optimal_move = None
        if maximizing_ai:
            max_eval = -math.inf
            for row in range(N):
                for col in range(N):
                    if board[row][col] == EMPTY:
                        board[row][col] = self.ai_marker
                        eval_score, _ = self.minimax(board, depth + 1, False, alpha, beta)
                        board[row][col] = EMPTY
                        if eval_score > max_eval:
                            max_eval = eval_score
                            optimal_move = (row, col)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break
            return max_eval, optimal_move
        else:
            min_eval = math.inf
            for row in range(N):
                for col in range(N):
                    if board[row][col] == EMPTY:
                        board[row][col] = self.player_marker
                        eval_score, _ = self.minimax(board, depth + 1, True, alpha, beta)
                        board[row][col] = EMPTY
                        if eval_score < min_eval:
                            min_eval = eval_score
                            optimal_move = (row, col)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
            return min_eval, optimal_move

    def update_win_draw_ui(self, winner):
        """
        Update the UI and scores when the game ends (win or draw).
        """
        if winner == self.ai_marker:
            for marker in self.marker_combination:
                index = marker[0] * N + marker[1]
                self.board.controls[index].bgcolor = "#f1fa8c"
            self.page.overlay.append(self.game_ends)
            self.game_ends.title.value = "AI Wins!"
            self.game_ends.open = True
            self.ai_score += 1
            self.ai_tally.value = self.ai_score
            self.title.color = self.ai_icon_color
            self.previous_winner = "AI"
            self.page.update()
        elif winner == self.player_marker:
            for marker in self.marker_combination:
                index = marker[0] * N + marker[1]
                self.board.controls[index].bgcolor = "#f1fa8c"
            self.page.overlay.append(self.game_ends)
            self.game_ends.title.value = "Player Wins!"
            self.game_ends.open = True
            self.player_score += 1
            self.player_tally.value = self.player_score
            self.previous_winner = "Player"
            self.title.color = self.player_icon_color
            self.page.update()
        elif winner == T:
            self.page.overlay.append(self.game_ends)
            self.game_ends.title.value = "Draw!"
            self.game_ends.open = True
            self.ties_score += 1
            self.ties_tally.value = self.ties_score
            self.previous_winner = "Draw"
            self.page.update()

    async def ai_marks(self):
        """
        Handle the AI's move, update the board, and check for game end.
        """
        board = copy.deepcopy(self.board_state)
        if self.initial_move_ai:
            row = random.randint(0, N - 1)
            col = random.randint(0, N - 1)
            optimal_move = (row, col)
            self.initial_move_ai = False
        else:
            _, optimal_move = self.minimax(board, 0, True, -math.inf, math.inf)

        if optimal_move:
            index = optimal_move[0] * N + optimal_move[1]
            self.board_state[optimal_move[0]][optimal_move[1]] = self.ai_marker
            self.player_turn.visible = False
            self.ai_turn.visible = True
            self.board.controls[index].content = ft.Icon(
                name=self.ai_icon_name, color=self.ai_icon_color, size=70
            )
            self.board.controls[index].bgcolor = BOARD_BG
            self.board.controls[index].disabled = True
            self.page.update()

            board = copy.deepcopy(self.board_state)
            winner = self.check_winner(board)
            if winner in (self.ai_marker, self.player_marker, T):
                self.update_win_draw_ui(winner)
                return

            await asyncio.sleep(0.5)
            self.ai_turn.visible = False
            self.player_turn.visible = True
            self.page.update()

    async def player_marks(self, e):
        """
        Handle the player's move, update the board, and check for game end.
        """
        index = e.control.data
        row = index // N
        col = index % N
        if self.board_state[row][col] is not None:
            return

        self.board_state[row][col] = self.player_marker
        self.player_turn.visible = True
        self.ai_turn.visible = False
        self.board.controls[index].content = ft.Icon(
            name=self.player_icon_name, color=self.player_icon_color, size=70
        )
        self.board.controls[index].bgcolor = BOARD_BG
        self.board.controls[index].disabled = True
        self.page.update()

        board = copy.deepcopy(self.board_state)
        winner = self.check_winner(board)
        if winner in (self.player_marker, self.ai_marker, T):
            self.update_win_draw_ui(winner)
            return

        await asyncio.sleep(0.5)
        await self.ai_marks()

    async def new_game(self, e):
        """
        Reset the board and start a new game.
        """
        self.game_ends.open = False
        self.title.color = "#f8f8f2"
        self.page.update()
        await asyncio.sleep(0.5)
        self.board_state = [[EMPTY for _ in range(N)] for _ in range(N)]
        for i in range(N * N):
            self.board.controls[i].disabled = False
            self.board.controls[i].content = ft.Icon()
            self.board.controls[i].bgcolor = BOARD_BG
        self.page.update()
        self.ask_player_first()

    async def confirm_exit_game(self, e):
        """
        Show the exit confirmation dialog.
        """
        self.exit_dialog.open = True
        self.page.overlay.append(self.exit_dialog)
        self.page.update()

    async def exit_game(self, e):
        """
        Handle the exit game action.
        """
        self.exit_dialog.open = False
        self.page.update()
        await asyncio.sleep(0.5) 
        self.page.window.destroy()

def main(page: ft.Page):
    """
    Main entry point for the app. Sets up the page and adds the TicTacToe game.
    """
    page.title = "Tic Tac Toe"
    page.window.height = 600
    page.window.width = 500
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 50
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#21222c"

    ttt = TicTacToe(page)
    for cell in ttt.board.controls:
        cell.on_click = ttt.player_marks
        cell.async_callback = True
    page.add(ttt)

ft.app(main)
