from dash_extensions import EventListener
from dash_extensions.enrich import DashProxy, html, Input, Output, State, dcc
from dash.exceptions import PreventUpdate
import time

''' import random
def gamewin(comp, you):
    if comp == you:
        return None
    elif comp=="st":
        if you=="sc":
            return False
        elif you=="p":
            return True
        elif comp =="sc":
            if you=="p":
                return False
            elif you =="st":
                return True
        elif comp =="p":
            if you=="st":
                return False
            elif you =="sc":
                return True
print("Comp Turn: stone(st) scissor(sc)or paper(p)?")
randNo=random.randint(1,3)
if randNo ==1:
    comp="st"
elif randNo==2:
    comp="sc"
elif randNo==3:
    comp="p"
you = input("Your Turn: stone(st) scissor(sc) or paper(p)?")
a = gamewin(comp,you)
print(f"Computer Choose  {comp}")
print(f"You Choose  {you}")
if a==None:
    print("The game is a tie!")
elif a :
    print("You win!")
else:
    print("You lose!") '''


app = DashProxy(__name__)


def generate_card(src: str, borderColor: str, rotation: str):
    return html.Div(style={'width': '125px', 'height': '207px', 'border': '1px', 'border-style': 'solid',
                           'border-color': borderColor, 'border-radius': '11px', 'display': 'flex', 'justify-content': 'center', 'backgroundColor': 'white',
                           'rotate': rotation,

                           },
                    children=html.Img(
                        src=src, style={'width': '60%', 'height': 'auto'})
                    )


# a&4 is rock, s&5 is paper, d&6 is scissor.
rps_values = {
    'a': 1,
    's': 2,
    'd': 3,
    '4': 1,
    '5': 2,
    '6': 3
}

rps_assets = {
    1: 'assets/rock.svg',
    2: 'assets/paper.svg',
    3: 'assets/scissor.svg',
}


@app.callback(
    Output("player_state", "data"),
    Input("main_elem", "event"),
    Input("main_elem", "n_events"),
    State("player_state", "data")
)
def update_datastore(e, ne,  player_state):
    if e is None:
        raise PreventUpdate()
    key = str(e['key']).lower()

    player_state = player_state or {
        'p1_input': None, 'p2_input': None, 'p1_timestamp': None, 'p2_timestamp': None, }

    now = time.time_ns() / 1000000  # Time in milliseconds
    if key == 'a' or key == 's' or key == 'd':
        print(e)
        player_state['p1_input'] = rps_values[key]
        player_state['p1_timestamp'] = now

    if key == '4' or key == '5' or key == '6':
        print(e)
        player_state['p2_input'] = rps_values[key]
        player_state['p2_timestamp'] = now

    return player_state


@app.callback(Output("score_store", "data"),
              Output("result-p1", "children"),
              Output("result-p2", "children"),
              Input("player_state", "modified_timestamp"),
              State("player_state", "data"),
              State("score_store", "data")
              )
def on_player_states(ts, player_state, data):

    if ts is None:
        raise PreventUpdate
    data = data or {'score_p1': 0, 'score_p2': 0}
    player_state = player_state or {
        'p1_input': None, 'p2_input': None, 'p1_timestamp': None, 'p2_timestamp': None, }

    winner = None
    # 300ms max diff. between both player inputs
    if (player_state['p1_input'] != None and player_state['p2_input'] != None and player_state['p1_timestamp'] != None and player_state['p2_timestamp'] != None):
        if (abs(player_state['p1_timestamp']-player_state['p2_timestamp']) <= 300):
            print("Calculating winner")
            winner = calc_winner(
                player_state['p1_input'], player_state['p2_input'])

            print("{} won!".format(winner if winner != "draw" else "Nobody"))

            if (winner == "p1"):
                data['score_p1'] = data['score_p1'] + 1
            elif (winner == "p2"):
                data['score_p2'] = data['score_p2'] + 1
            # else draw, no one won
    cardp1 = html.Div()
    cardp2 = html.Div()
    
    if (winner == "p1"):
        cardp1 = generate_card(rps_assets[player_state['p1_input']], "#63F31D",
                               "0deg") if player_state['p1_input'] != None else html.Div()
        cardp2 = generate_card(rps_assets[player_state['p2_input']], "#707070",
                               "0deg") if player_state['p2_input'] != None else html.Div()
    elif (winner == "p2"):
        cardp1 = generate_card(rps_assets[player_state['p1_input']], "#707070",
                               "0deg") if player_state['p1_input'] != None else html.Div()
        cardp2 = generate_card(rps_assets[player_state['p2_input']], "#63F31D",
                               "0deg") if player_state['p2_input'] != None else html.Div()
    else:
        cardp1 = generate_card(rps_assets[player_state['p1_input']], "#707070",
                               "0deg") if player_state['p1_input'] != None else html.Div()
        cardp2 = generate_card(rps_assets[player_state['p2_input']], "#707070",
                               "0deg") if player_state['p2_input'] != None else html.Div()

    return data, cardp1, cardp2


@app.callback(Output(component_id='p1_score', component_property='children'),
              Output(component_id='p2_score', component_property='children'),
              Input("score_store", "modified_timestamp"),
              State("score_store", "data")
              )
def on_data(ts, data):

    if ts is None:
        raise PreventUpdate
    data = data or {'score_p1': 0, 'score_p2': 0}

    return data.get('score_p1', 0), data.get('score_p2', 0)


# logic from https://eduherminio.github.io/blog/rock-paper-scissors/
def calc_winner(p1: int, p2: int):

    inps = {p1, p2}

    winner = abs(p2-p1)
    if winner == 0:
        return "draw"
    elif winner == 1:
        inpsInv = {p1: "p1", p2: "p2"}
        return inpsInv[max(inps)]
    else:
        inpsInv = {p1: "p1", p2: "p2"}
        return inpsInv[min(inps)]


app.layout = EventListener(html.Div(tabIndex="-1", children=[
    html.Div(style={'width': '100%', 'display': 'flex', 'position': 'fixed', 'justify-content': 'center', 'z-index': '2'},
             children=[html.Img(style={'transform': 'scaleX(-1)', 'margin': '0px'},
                                src='assets/page_sep.svg'),
                       html.Img(src='assets/page_sep.svg',
                                style={'margin-left': '-2px'}),

                       ],
             ),
    html.Div(style={'z-index': '3', 'display': 'flex', 'position': 'fixed', 'justify-content': 'center', 'width': '100%', 'height': '100%', 'align-items': 'center'},
             children=[html.Div(style={'margin-right': '-30px', 'position': 'relative', 'top': '20px'},
                                children=generate_card('assets/rock.svg', '#F31D1D', '-30deg')),
             html.Div(style={'z-index': '4'}, children=generate_card(
                 'assets/paper.svg', '#1DD6F3', '0deg')),
        html.Div(style={'margin-left': '-30px', 'position': 'relative', 'top': '20px'}, children=generate_card(
            'assets/scissor.svg', '#5C10F8', '30deg')),
    ],),
    html.Div(style={'z-index': '3', 'display': 'flex', 'position': 'fixed', 'justify-content': 'center', 'width': '100%', 'height': '100%', 'align-items': 'center'},
             children=[
        html.Div(id="result-p1",
                 style={'position': 'fixed', 'left': '80px'}, ),
             html.Div(id="result-p2",
                      style={'position': 'fixed', 'right': '80px'},),
             ],),
    dcc.Store('score_store'),
    dcc.Store('player_state'),
    html.Div('0', id='p1_score', className='score_text',
             style={'bottom': '20px', 'left': '30px'},),
    html.Div('0', id='p2_score', className='score_text',
             style={'bottom': '20px', 'right': '30px'}),
    html.Div(style={'width': '100%', 'display': 'flex', 'position': 'fixed', 'justify-content': 'center', 'z-index': '3', 'bottom': '0px'},
             children=[html.Img(src='assets/keyboard.svg',
                                style={'width': '20%', 'height': 'auto'}), ],
             ),
]),
    events=[{"event": "keyup", "props": ["key", "repeat"]}],

    id="main_elem",
    logging=False,

)

if __name__ == '__main__':
    app.run_server(debug=False)
