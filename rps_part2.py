import streamlit as st
import random
from enum import Enum

# --- Constants and Enums ---
class Choice(Enum):
    ROCK = "🪨 Rock"
    PAPER = "📄 Paper"
    SCISSOR = "✂️ Scissor"

# --- Session State Initialization ---
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "user_score": 0,
        "computer_score": 0,
        "user_choice": "",
        "computer_choice": "",
        "match_result": "",
        "game_active": True,
        "max_score": 3,
        "history": []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --- Game Logic Functions ---
def get_computer_choice():
    """Randomly select computer's choice"""
    return random.choice(list(Choice))

def determine_winner(user, comp):
    """Determine round winner and return result string"""
    if user == comp:
        return "Match Draw! 🤝"
    elif (user == Choice.ROCK and comp == Choice.SCISSOR) or \
         (user == Choice.PAPER and comp == Choice.ROCK) or \
         (user == Choice.SCISSOR and comp == Choice.PAPER):
        st.session_state.user_score += 1
        return "You Win! 🎉"
    else:
        st.session_state.computer_score += 1
        return "Computer Wins! 💻"

def play_round(user_choice_val):
    """Execute one round of the game"""
    st.session_state.user_choice = user_choice_val
    st.session_state.computer_choice = get_computer_choice()
    
    user = st.session_state.user_choice
    comp = st.session_state.computer_choice
    
    st.session_state.match_result = determine_winner(user, comp)
    st.session_state.history.append(f"Round {len(st.session_state.history)+1}: {user.value} vs {comp.value} -> {st.session_state.match_result}")
    
    # Check for game winner
    if st.session_state.user_score >= st.session_state.max_score:
        st.session_state.match_result = f"🏆 You Won the Game! (Best of {st.session_state.max_score})"
        st.balloons()
        st.session_state.game_active = False
    elif st.session_state.computer_score >= st.session_state.max_score:
        st.session_state.match_result = f"😢 Computer Won the Game! (Best of {st.session_state.max_score})"
        st.session_state.game_active = False
    else:
        st.session_state.game_active = False  # Still need to click "Play Again"

def reset_game():
    """Reset all game state"""
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.user_choice = ""
    st.session_state.computer_choice = ""
    st.session_state.match_result = ""
    st.session_state.game_active = True
    st.session_state.history = []

def play_again():
    """Reset for next round"""
    st.session_state.user_choice = ""
    st.session_state.computer_choice = ""
    st.session_state.match_result = ""
    st.session_state.game_active = True

# --- Streamlit UI Configuration ---
st.set_page_config(
    page_title="Rock Paper Scissor Game",
    layout="centered",
    initial_sidebar_state="expanded"  # Now using sidebar for settings
)

# --- Sidebar (Settings and Info) ---
with st.sidebar:
    st.header("⚙️ Game Settings")
    st.session_state.max_score = st.selectbox(
        "Play Best of:",
        options=[3, 5, 7, 10],
        index=0
    )
    
    st.header("📊 Stats")
    st.metric("Your Wins", st.session_state.user_score)
    st.metric("Computer Wins", st.session_state.computer_score)
    
    with st.expander("📖 How to Play"):
        st.write(f"""
        - Choose **Rock**, **Paper**, or **Scissors**
        - First to win **{st.session_state.max_score} rounds** wins the game!
        - Click **Play Again** for a new round
        - Click **Reset** to start completely fresh
        """)

# --- Main Game Interface ---
st.title("🪨📄✂️ Rock Paper Scissors")

# Score Display
st.subheader("Current Scores")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Your Score", value=st.session_state.user_score)
with col2:
    st.metric(label="Computer Score", value=st.session_state.computer_score)

st.markdown("---")

# Round Display
st.subheader("Round Details")
col_user, col_vs, col_comp = st.columns([1, 0.5, 1])

with col_user:
    st.write("**Your choice:**")
    choice = st.session_state.user_choice
    st.markdown(f"<h2 style='text-align: center;'>{choice.value if choice else '?'}</h2>", 
                unsafe_allow_html=True)

with col_vs:
    st.markdown("<h2 style='text-align: center; color: red;'>VS</h2>", 
                unsafe_allow_html=True)

with col_comp:
    st.write("**Computer's choice:**")
    choice = st.session_state.computer_choice
    st.markdown(f"<h2 style='text-align: center;'>{choice.value if choice else '?'}</h2>", 
                unsafe_allow_html=True)

# Result Display
if st.session_state.match_result:
    st.markdown(f"<h2 style='text-align: center; color: {'green' if 'You' in st.session_state.match_result else 'red'};'>"
                f"{st.session_state.match_result}</h2>", 
                unsafe_allow_html=True)
else:
    st.info("Make your move to start the game!")

st.markdown("---")

# Action Buttons
if st.session_state.game_active:
    st.subheader("Make Your Move!")
    cols = st.columns(3)
    choices = [Choice.ROCK, Choice.PAPER, Choice.SCISSOR]
    for col, choice in zip(cols, choices):
        with col:
            st.button(choice.value, 
                     on_click=play_round, 
                     args=(choice,), 
                     use_container_width=True)
else:
    st.button("🔄 Play Another Round", 
             on_click=play_again, 
             type="primary", 
             use_container_width=True)

st.button("♻️ Reset All Scores", 
         on_click=reset_game, 
         type="secondary", 
         use_container_width=True)

# Game History
if st.session_state.history:
    st.markdown("---")
    with st.expander("📜 Game History"):
        for result in st.session_state.history[-5:][::-1]:  # Show last 5, newest first
            st.write(result)