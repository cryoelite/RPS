from dash_extensions import EventListener
from dash_extensions.enrich import DashProxy, html, Input, Output, State, dcc
from dash.exceptions import PreventUpdate
import time

# Create the main Dash app instance
app = DashProxy(__name__)

# --- Constants ---
# Map keyboard inputs to game values (1: Rock, 2: Paper, 3: Scissors)
# Player 1: 'a', 's', 'd'
# Player 2: '4', '5', '6'
RPS_VALUES = {
    'a': 1, 's': 2, 'd': 3,  # Player 1
    '4': 1, '5': 2, '6': 3   # Player 2
}

# Map game values to their corresponding image assets
RPS_ASSETS = {
    1: 'assets/rock.svg',
    2: 'assets/paper.svg',
    3: 'assets/scissor.svg',
}

# --- Reusable UI Components ---

def generate_card(src: str, border_color: str, rotation: str):
    """Creates a UI card element to display a rock, paper, or scissors image."""
    return html.Div(style={'width': '125px', 'height': '207px', 'border': '1px', 'border-style': 'solid',
                           'border-color': border_color, 'border-radius': '11px', 'display': 'flex',
                           'justify-content': 'center', 'backgroundColor': 'white', 'rotate': rotation},
                    children=html.Img(src=src, style={'width': '60%', 'height': 'auto'}))

# --- Game Logic ---

def calc_winner(p1_choice: int, p2_choice: int):
    """
    Determines the winner of a Rock-Paper-Scissors round.
    - 1: Rock, 2: Paper, 3: Scissors
    Returns 'p1', 'p2', or 'draw'.
    """
    if p1_choice == p2_choice:
        return "draw"

    winning_combinations = {
        (1, 3),  # Rock (1) beats Scissors (3)
        (2, 1),  # Paper (2) beats Rock (1)
        (3, 2),  # Scissors (3) beats Paper (2)
    }

    if (p1_choice, p2_choice) in winning_combinations:
        return "p1"
    else:
        return "p2"

# --- Callbacks ---

@app.callback(
    Output("player_state", "data"),
    Input("main_elem", "event"),
    State("player_state", "data")
)
def update_player_state_on_keypress(event, player_state):
    """
    Listens for keyboard events and updates the shared player state.
    This callback captures key presses for both players, records their choice
    and the timestamp of the input.
    """
    if event is None:
        raise PreventUpdate

    key = str(event['key']).lower()

    # Initialize state if it's the first run
    player_state = player_state or {
        'p1_input': None, 'p2_input': None,
        'p1_timestamp': None, 'p2_timestamp': None,
    }

    # Ignore keys that are not part of the game controls
    if key not in RPS_VALUES:
        raise PreventUpdate

    now_ms = time.time_ns() / 1_000_000  # Time in milliseconds

    # Update state for the corresponding player
    if key in ['a', 's', 'd']:
        player_state['p1_input'] = RPS_VALUES[key]
        player_state['p1_timestamp'] = now_ms
    elif key in ['4', '5', '6']:
        player_state['p2_input'] = RPS_VALUES[key]
        player_state['p2_timestamp'] = now_ms

    return player_state


@app.callback(
    Output("score_store", "data"),
    Output("result-p1", "children"),
    Output("result-p2", "children"),
    Input("player_state", "modified_timestamp"),
    State("player_state", "data"),
    State("score_store", "data")
)
def handle_game_round(ts, player_state, score_data):
    """
    This is the core game logic callback. It triggers whenever the player state changes.
    It checks if both players have made a move within the time limit,
    calculates the winner, updates scores, and displays the results.
    """
    if ts is None:
        raise PreventUpdate

    # Initialize data stores on first run
    score_data = score_data or {'score_p1': 0, 'score_p2': 0}
    player_state = player_state or {
        'p1_input': None, 'p2_input': None,
        'p1_timestamp': None, 'p2_timestamp': None,
    }

    p1_input = player_state.get('p1_input')
    p2_input = player_state.get('p2_input')
    p1_time = player_state.get('p1_timestamp')
    p2_time = player_state.get('p2_timestamp')

    winner = None
    # A round can only be decided if both players have made an input
    if all([p1_input, p2_input, p1_time, p2_time]):
        # Check if inputs were made within the 300ms time window
        if abs(p1_time - p2_time) <= 300:
            winner = calc_winner(p1_input, p2_input)

            # Update scores based on the winner
            if winner == "p1":
                score_data['score_p1'] += 1
            elif winner == "p2":
                score_data['score_p2'] += 1
            # On draw, scores do not change

    # --- UI Updates ---
    # Default border color for cards
    p1_border_color = "#707070"
    p2_border_color = "#707070"

    # Highlight winner's card in green
    if winner == "p1":
        p1_border_color = "#63F31D"  # Green
    elif winner == "p2":
        p2_border_color = "#63F31D"  # Green

    # Generate the cards to display the players' choices
    card_p1 = html.Div()
    card_p2 = html.Div()
    if p1_input:
        card_p1 = generate_card(RPS_ASSETS[p1_input], p1_border_color, "0deg")
    if p2_input:
        card_p2 = generate_card(RPS_ASSETS[p2_input], p2_border_color, "0deg")

    return score_data, card_p1, card_p2


@app.callback(
    Output('p1_score', 'children'),
    Output('p2_score', 'children'),
    Input("score_store", "modified_timestamp"),
    State("score_store", "data")
)
def update_score_display(ts, score_data):
    """Updates the score displays on the screen when the score data changes."""
    if ts is None:
        raise PreventUpdate
    score_data = score_data or {'score_p1': 0, 'score_p2': 0}
    return score_data.get('score_p1', 0), score_data.get('score_p2', 0)


# --- App Layout ---

app.layout = EventListener(
    html.Div(tabIndex="-1", children=[
        # Data stores for game state and scores
        dcc.Store('player_state'),
        dcc.Store('score_store'),

        # Top decorative separator
        html.Div(
            style={'width': '100%', 'display': 'flex', 'position': 'fixed', 'justify-content': 'center', 'z-index': '2'},
            children=[
                html.Img(src='assets/page_sep.svg', style={'transform': 'scaleX(-1)', 'margin': '0px'}),
                html.Img(src='assets/page_sep.svg', style={'margin-left': '-2px'}),
            ]
        ),

        # Center static background cards
        html.Div(
            style={'z-index': '3', 'display': 'flex', 'position': 'fixed', 'justify-content': 'center', 'width': '100%', 'height': '100%', 'align-items': 'center'},
            children=[
                html.Div(style={'margin-right': '-30px', 'position': 'relative', 'top': '20px'}, children=generate_card('assets/rock.svg', '#F31D1D', '-30deg')),
                html.Div(style={'z-index': '4'}, children=generate_card('assets/paper.svg', '#1DD6F3', '0deg')),
                html.Div(style={'margin-left': '-30px', 'position': 'relative', 'top': '20px'}, children=generate_card('assets/scissor.svg', '#5C10F8', '30deg')),
            ]
        ),

        # Area where player choices are displayed after a round
        html.Div(
            style={'z-index': '3', 'display': 'flex', 'position': 'fixed', 'justify-content': 'center', 'width': '100%', 'height': '100%', 'align-items': 'center'},
            children=[
                html.Div(id="result-p1", style={'position': 'fixed', 'left': '80px'}),
                html.Div(id="result-p2", style={'position': 'fixed', 'right': '80px'}),
            ]
        ),

        # Score displays
        html.Div('0', id='p1_score', className='score_text', style={'bottom': '20px', 'left': '30px'}),
        html.Div('0', id='p2_score', className='score_text', style={'bottom': '20px', 'right': '30px'}),

        # Bottom keyboard controls image
        html.Div(
            style={'width': '100%', 'display': 'flex', 'position': 'fixed', 'justify-content': 'center', 'z-index': '3', 'bottom': '0px'},
            children=[html.Img(src='assets/keyboard.svg', style={'width': '20%', 'height': 'auto'})]
        ),
    ]),
    # Listen for 'keyup' events on the main div
    id="main_elem",
    events=[{"event": "keyup", "props": ["key", "repeat"]}],
    logging=False
)

if __name__ == '__main__':
    app.run_server(debug=False)
