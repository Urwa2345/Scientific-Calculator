# 🔢 Scientific Calculator

A dark-themed scientific calculator built with Python and Streamlit. Works with both keyboard typing and mouse clicks, and the two always stay in sync.

## Features

- Type an expression and press **Enter**, or click the on-screen buttons — either way, the display stays consistent
- Scientific functions: `sin`, `cos`, `tan`, `asin`, `acos`, `atan` (degrees), `log`, `ln`, `sqrt`, `abs`, `factorial`, `exp`, plus `π` and `e`
- Safe evaluation — expressions run in a locked-down sandbox with no access to Python's built-in functions
- Clean number formatting (no trailing `.0` on whole results)
- Custom dark UI with hover/press effects on buttons

## Requirements

- Python 3.8+
- Streamlit

## Setup

```bash
pip install streamlit
```

## Run

```bash
streamlit run Scientific_Calculator.py
```

Opens in your browser at `http://localhost:8501`.

## Usage

| Action | How |
|---|---|
| Calculate | Type expression + Enter, or click `=` |
| Power | `^` (e.g. `2^10`) |
| Factorial | `!` (e.g. `factorial(5)`) |
| Clear | `C` |
| Backspace | `⌫` |

## How it works

- `st.session_state` tracks the current expression and result across every click and keystroke, since Streamlit reruns the script each time.
- The input field's key changes on every button click, forcing it to refresh with the latest expression instead of keeping stale typed text — this is what keeps keyboard and mouse input in sync.
- `eval()` is restricted to a fixed set of safe math functions only, so no unsafe code can run through it.

## Possible additions

- Calculation history
- Memory buttons (M+, M-, MR, MC)
- Degrees/radians toggle

## License

Free to use and modify.

