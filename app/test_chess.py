import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# --- Chess Piece Placement & Info Logic (UPDATED) ---

def get_rook_placements(n):
    """Calculates placements and arrangement info for n non-attacking rooks."""
    placements = [(i, i) for i in range(n)]
    count = n
    formula = "n"
    # ENHANCEMENT: Add the number of arrangements.
    try:
        arrangements_text = f"{n}! = {math.factorial(n):,}"
    except ValueError:
        arrangements_text = f"{n}! (a very large number)"
    return placements, count, formula, arrangements_text

def get_knight_placements(n):
    """Calculates placements and arrangement info for non-attacking knights."""
    placements = []
    for r in range(n):
        for c in range(n):
            if (r + c) % 2 == 0:  # All light squares
                placements.append((r, c))
    count = math.ceil((n ** 2) / 2)
    formula = r"\lceil n^2/2 \rceil"
    # ENHANCEMENT: Add the number of arrangements.
    arrangements_text = "2 (all on light squares or all on dark squares)."
    return placements, count, formula, arrangements_text

def get_bishop_placements(n):
    """Calculates a correct placement for 2n-2 non-attacking bishops."""
    # ENHANCEMENT: Corrected the placement logic.
    # This construction places n on the top row and n-2 on the bottom, skipping corners.
    placements = []
    if n > 0:
        for i in range(n):
            placements.append((0, i))  # Top row
    if n > 2:
        for i in range(1, n - 1):
            placements.append((n-1, i)) # Bottom row, skipping corners
            
    count = 2 * n - 2 if n > 1 else n
    formula = "2n - 2"
    # ENHANCEMENT: Add the number of arrangements.
    try:
        arrangements_text = f"2^{n} = {2**n:,}"
    except OverflowError:
        arrangements_text = f"2^{n} (a very large number)"
    return placements, count, formula, arrangements_text

def get_king_placements(n):
    """Calculates placements and arrangement info for non-attacking kings."""
    placements = []
    for r in range(0, n, 2):
        for c in range(0, n, 2):
            placements.append((r, c))
    count = math.ceil(n / 2) * math.ceil(n / 2)
    formula = r"\lceil n/2 \rceil^2"
    # ENHANCEMENT: Add arrangement info based on board parity.
    if n % 2 != 0:
        arrangements_text = "1 (a unique arrangement for odd-sized boards)."
    else:
        arrangements_text = "An unsolved problem with many solutions for even-sized boards."
    return placements, count, formula, arrangements_text

# --- Queen Solver (no changes here, but added arrangement info) ---
def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i] == 1: return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1: return False
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == 1: return False
    return True

def solve_n_queens_util(board, col, n):
    if col >= n: return True
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            if solve_n_queens_util(board, col + 1, n): return True
            board[i][col] = 0
    return False

def get_queen_placements(n):
    """Calculates one solution and provides arrangement info."""
    if n == 2 or n == 3:
        return [], 0, "n (no solution for n=2,3)", "0"
    board = [[0] * n for _ in range(n)]
    placements = []
    if solve_n_queens_util(board, 0, n):
        for r in range(n):
            for c in range(n):
                if board[r][c] == 1:
                    placements.append((r, c))
    count = len(placements)
    formula = "n"
    # ENHANCEMENT: Add detailed arrangement info for the 8x8 case and general case.
    if n == 8:
        arrangements_text = "92 distinct solutions (12 fundamental solutions if rotations/reflections are considered the same)."
    else:
        arrangements_text = "An unsolved problem for large n."
    return placements, count, formula, arrangements_text

# --- Matplotlib Board Drawing (no changes here) ---
def draw_board(n, placements, piece_symbol, piece_color, light_color, dark_color):
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
    for r in range(n):
        for c in range(n):
            color = light_color if (r + c) % 2 == 0 else dark_color
            rect = patches.Rectangle((c, r), 1, 1, facecolor=color)
            ax.add_patch(rect)
    for r, c in placements:
        ax.text(c + 0.5, r + 0.5, piece_symbol,
                fontsize=30 / (n or 1) * 4, ha='center', va='center', color=piece_color)
    ax.invert_yaxis()
    return fig

# --- Streamlit App UI (UPDATED) ---
st.set_page_config(layout="wide")
st.title("Interactive Demo: Maximum Non-Attacking Chess Pieces")
st.write(
    "This application visualizes the solution to the classic independence problem in chess: "
    "placing the maximum number of non-attacking pieces of a single type on a board of size 'n'."
)

st.sidebar.header("Controls")
board_size = st.sidebar.slider("Select Board Size (n x n)", min_value=1, max_value=20, value=8)
piece_type = st.sidebar.selectbox(
    "Select Chess Piece",
    ("Rook", "Knight", "Bishop", "King", "Queen",)
)
st.sidebar.header("Color Customization")
piece_color = st.sidebar.color_picker("Piece Color", "#000000")
light_square_color = st.sidebar.color_picker("Light Square Color", "#F0D9B5")
dark_square_color = st.sidebar.color_picker("Dark Square Color", "#B58863")

# --- Main Logic & Display (UPDATED) ---
col1, col2 = st.columns([1, 2])
placements, count, formula, symbol, arrangements_text = [], 0, "", "", ""

piece_map = {
    "Rook": (get_rook_placements, '♖'),
    "Knight": (get_knight_placements, '♘'),
    "Bishop": (get_bishop_placements, '♗'),
    "King": (get_king_placements, '♔'),
    "Queen": (get_queen_placements, '♕')
}

if piece_type in piece_map:
    placement_func, symbol = piece_map[piece_type]
    placements, count, formula, arrangements_text = placement_func(board_size)

with col1:
    st.header(f"Results for the {piece_type}")
    st.metric(f"Maximum Pieces on {board_size}x{board_size} Board", count)
    st.write("---")
    st.subheader("General Formula")
    st.latex(formula)
    st.write("---")
    
    # ENHANCEMENT: New section for Number of Arrangements
    st.subheader("Number of Arrangements")
    st.info(arrangements_text)
    
    st.write("---")
    st.subheader("Construction Logic")
    logic_text = {
        "Rook": "Place one rook in each row and column. The visualized solution places them along the main diagonal.",
        "Knight": "Place knights on all squares of the same color. A knight always moves between light and dark squares, so they can never attack each other.",
        "Bishop": "A common construction is to place bishops along the edges. The solution shown places bishops on all squares of the top row and all but the two corner squares of the bottom row.",
        "King": "Place kings with a one-square buffer between them in all directions. This is achieved by placing them on alternating files and ranks.",
        "Queen": "No simple construction formula exists. The solution shown is found using a backtracking algorithm to search for one of the many possible valid placements."
    }
    st.write(logic_text.get(piece_type, ""))

with col2:
    st.header("Board Visualization")
    if not placements and board_size > 0 and piece_type == "Queen":
        st.warning(f"No solution exists for {board_size}x{board_size} queens.")
    else:
        fig = draw_board(board_size, placements, symbol, piece_color, light_square_color, dark_square_color)
        st.pyplot(fig)