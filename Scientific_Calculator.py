import streamlit as st
import math

st.set_page_config(page_title="Urwa's Sci Calc", page_icon="🔢", layout="centered")

# ---------- styling ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(160deg, #10121c 0%, #1a1d2e 100%);
    }

    /* hide the label row entirely, we use a placeholder inside the field instead */
    div[data-testid="stTextInput"] label {
        display: none;
    }

    /* Streamlit auto-shows a "Press Enter to apply" hint below the field
       whenever text is uncommitted - we already have our own placeholder
       text inside the box, so this one is redundant. Hide it. */
    div[data-testid="InputInstructions"] {
        display: none;
    }

    /* make the text input itself look like the calculator screen */
    div[data-testid="stTextInput"] input {
        background: #0d0f18;
        color: #eef0f7;
        font-size: 30px;
        font-weight: 600;
        text-align: right;
        border-radius: 14px;
        border: 1px solid #2a2e42;
        padding: 20px 22px;
        font-family: 'Courier New', monospace;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #565b78;
        font-size: 16px;
        font-weight: 400;
    }
    div[data-testid="stTextInput"] input:focus {
        border: 1px solid #6366f1;
        box-shadow: 0 0 0 1px #6366f1;
    }

    div.stButton > button {
        width: 100%;
        height: 62px;
        border-radius: 12px;
        border: 1px solid #2a2e42;
        font-size: 17px;
        font-weight: 500;
        background: #1c1f30;
        color: #dcdfec;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: 0.15s ease;
    }
    div.stButton > button:hover {
        background: #262a41;
        border-color: #3a3f5c;
        color: #fff;
        transform: translateY(-1px);
    }
    div.stButton > button:active {
        transform: translateY(1px);
    }
    /* the "=" button gets Streamlit's primary style, recolor it to stand out */
    div.stButton > button[kind="primary"] {
        background: #6366f1;
        border: 1px solid #6366f1;
        color: white;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #7577f3;
        border-color: #7577f3;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔢 Scientific Calculator")

# ---------- state ----------
if "expr" not in st.session_state:
    st.session_state.expr = ""
if "version" not in st.session_state:
    st.session_state.version = 0

# functions/constants exposed to eval, so users can't run arbitrary python
SAFE_NAMES = {
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "asin": lambda x: math.degrees(math.asin(x)),
    "acos": lambda x: math.degrees(math.acos(x)),
    "atan": lambda x: math.degrees(math.atan(x)),
    "log": math.log10,
    "ln": math.log,
    "sqrt": math.sqrt,
    "pow": math.pow,
    "pi": math.pi,
    "e": math.e,
    "abs": abs,
    "factorial": math.factorial,
    "exp": math.exp,
}


def format_result(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, float):
        return str(round(value, 10))
    return str(value)


def evaluate():
    """Evaluate the current expression and put the result straight back
    into st.session_state.expr, so the same field shows it - no second
    field needed."""
    expr = st.session_state.expr.replace("^", "**").replace("×", "*").replace("÷", "/")
    if not expr:
        return
    try:
        value = eval(expr, {"__builtins__": {}}, SAFE_NAMES)
        st.session_state.expr = format_result(value)
    except Exception:
        st.session_state.expr = "Error"
    st.session_state.version += 1  # forces the text_input to refresh with new text


def press(key):
    st.session_state.expr += key
    st.session_state.version += 1  # forces the text_input to refresh with new text


def clear_all():
    st.session_state.expr = ""
    st.session_state.version += 1


def backspace():
    st.session_state.expr = st.session_state.expr[:-1]
    st.session_state.version += 1


def on_type():
    # fires when you type into the box and press Enter (or click away)
    typed_key = f"typed_{st.session_state.version}"
    st.session_state.expr = st.session_state[typed_key]
    evaluate()


# ---------- the single input field (doubles as the result display) ----------
st.text_input(
    "expression",
    value=st.session_state.expr,
    key=f"typed_{st.session_state.version}",
    on_change=on_type,
    placeholder="Type here or press Enter to calculate...",
    label_visibility="collapsed",
)

# ---------- button grid ----------
rows = [
    [("sin(", "sin("), ("cos(", "cos("), ("tan(", "tan("), ("π", "π"), ("C", "C")],
    [("asin(", "asin("), ("acos(", "acos("), ("atan(", "atan("), ("e", "e"), ("⌫", "⌫")],
    [("log(", "log("), ("ln(", "ln("), ("sqrt(", "sqrt("), ("(", "("), (")", ")")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/"), ("^", "^")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("×", "*"), ("!", "!")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("−", "-"), ("abs(", "abs(")],
    [("0", "0"), (".", "."), ("%", "%"), ("＋", "+"), ("=", "=")],
]

for row in rows:
    ratios = [1.4 if value.isdigit() else 1 for _, value in row]
    cols = st.columns(ratios, gap="small")
    for col, (shown, value) in zip(cols, row):
        with col:
            is_equals = value == "="
            clicked = st.button(
                shown,
                key=f"btn_{shown}",
                type="primary" if is_equals else "secondary",
            )
            if clicked:
                if value == "C":
                    clear_all()
                elif value == "⌫":
                    backspace()
                elif value == "=":
                    evaluate()
                elif value == "π":
                    press("pi")
                elif value == "!":
                    press("factorial(")
                elif value == "%":
                    press("/100")
                else:
                    press(value)
                st.rerun()

st.caption("Click the buttons or type your expression directly — the result appears right in the same field.")
