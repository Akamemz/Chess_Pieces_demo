import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


# --- Chess Piece Placement Logic (No changes here) ---

def get_rook_placements(n):
    """Calculates placements for n non-attacking rooks."""
    placements = [(i, i) for i in range(n)]
    count = n
    formula = "n"
    return placements, count, formula


def get_knight_placements(n):
    """Calculates placements for the maximum number of non-attacking knights."""
    placements = []
    for r in range(n):
        for c in range(n):
            if (r + c) % 2 == 0:
                placements.append((r, c))
    count = math.ceil((n ** 2) / 2)
    formula = "⌈n²/2⌉"
    return placements, count, formula


def get_bishop_placements(n):
    """Calculates placements for 2n-2 non-attacking bishops."""
    placements = []
    for i in range(n):
        placements.append((i, 0))  # First column
    for i in range(n):
        placements.append((i, n - 1))  # Last column
    count = 2 * n - 2 if n > 1 else 1
    formula = "2n - 2"
    return placements, count, formula


def get_king_placements(n):
    """Calculates placements for the maximum number of non-attacking kings."""
    placements = []
    for r in range(0, n, 2):
        for c in range(0, n, 2):
            placements.append((r, c))
    count = math.ceil(n / 2) * math.ceil(n / 2)
    formula = "⌈n/2⌉²"
    return placements, count, formula


def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    return True


def solve_n_queens_util(board, col, n):
    if col >= n:
        return True
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            if solve_n_queens_util(board, col + 1, n):
                return True
            board[i][col] = 0
    return False


def get_queen_placements(n):
    if n == 2 or n == 3:
        return [], 0, "n (no solution for n=2,3)"
    board = [[0 for _ in range(n)] for _ in range(n)]
    if not solve_n_queens_util(board, 0, n):
        return [], 0, "n"
    placements = []
    for r in range(n):
        for c in range(n):
            if board[r][c] == 1:
                placements.append((r, c))
    count = n
    formula = "n"
    return placements, count, formula


# --- Matplotlib Board Drawing (UPDATED) ---

def draw_board(n, placements, piece_symbol, piece_color, light_color, dark_color):
    """Uses Matplotlib to draw the chessboard and place the pieces with custom colors."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels([chr(65 + i) for i in range(n)])
    ax.set_yticklabels(range(1, n + 1))
    ax.tick_params(length=0)
    ax.grid(True, color='black', linewidth=1.5)
    ax.set_aspect('equal')

    # Draw squares with user-selected colors
    for r in range(n):
        for c in range(n):
            color = light_color if (r + c) % 2 == 0 else dark_color
            rect = patches.Rectangle((c, r), 1, 1, facecolor=color)
            ax.add_patch(rect)

    # Place pieces with user-selected color
    for r, c in placements:
        ax.text(c + 0.5, r + 0.5, piece_symbol,
                fontsize=30 / n * 4, ha='center', va='center', color=piece_color)

    ax.invert_yaxis()
    return fig


# --- Streamlit App UI (UPDATED) ---

st.set_page_config(layout="wide")
st.title("Interactive Demo: Armies of Peaceful Chess Pieces")
st.write(
    "This application demonstrates placing the maximum number of non-attacking "
    "chess pieces on a board of a given size."
)

st.sidebar.header("Controls")
board_size = st.sidebar.slider("Select Board Size (n x n)", min_value=1, max_value=20, value=8)
piece_type = st.sidebar.selectbox(
    "Select Chess Piece",
    ("Rook", "Knight", "Bishop", "King", "Queen")
)

# New color pickers in the sidebar
st.sidebar.header("Color Customization")
piece_color = st.sidebar.color_picker("Piece Color", "#000000")
light_square_color = st.sidebar.color_picker("Light Square Color", "#F0D9B5")
dark_square_color = st.sidebar.color_picker("Dark Square Color", "#B58863")

# --- Main Logic & Display ---

col1, col2 = st.columns([1, 2])
placements, count, formula, symbol = [], 0, "", ""

piece_map = {
    "Rook": (get_rook_placements, '♖'),
    "Knight": (get_knight_placements, '♘'),
    "Bishop": (get_bishop_placements, '♗'),
    "King": (get_king_placements, '♔'),
    "Queen": (get_queen_placements, '♕')
}

if piece_type in piece_map:
    placement_func, symbol = piece_map[piece_type]
    placements, count, formula = placement_func(board_size)
    if piece_type == "Bishop":
        placements = placements[:count]  # Ensure correct number for visualization

with col1:
    st.header(f"Results for the {piece_type}")
    st.metric(f"Maximum Pieces on {board_size}x{board_size} Board", len(placements))
    st.write("---")
    st.subheader("General Formula")
    st.latex(formula)
    st.write("---")
    st.subheader("Construction Logic")

    logic_text = {
        "Rook": "Place one rook in each row and column, often along the main diagonal.",
        "Knight": "Place knights on all squares of the same color. They can never attack each other this way.",
        "Bishop": "Place bishops along two edges of the board, like the first and last columns.",
        "King": "Place kings with a one-square buffer between them in all directions.",
        "Queen": "No simple formula exists. This solution is found using a backtracking algorithm to search for a valid placement."
    }
    st.write(logic_text.get(piece_type, ""))

with col2:
    st.header("Board Visualization")
    if not placements and board_size > 0 and piece_type == "Queen":
        st.warning(f"No solution exists for {board_size}x{board_size} queens.")

    # Pass the new color arguments to the drawing function
    fig = draw_board(board_size, placements, symbol, piece_color, light_square_color, dark_square_color)
    st.pyplot(fig)

