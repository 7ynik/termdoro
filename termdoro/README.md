# termdoro

A minimal terminal-based Pomodoro timer. It guides you through alternating work and break sessions with clear countdowns and alerts. No accounts, no data tracking—just a timer and session switching.

## Features
- Work sessions: default 25 minutes, visible countdown in your terminal
- Break sessions: default 5 minutes
- Cycles: alternate between work and break
- Clear feedback: text alert when a session ends (optional terminal bell)
- Customizable durations: set your own work/break lengths
- Minimal configuration: no setup beyond Python 3

## Requirements
- Python 3.8+

## Usage
Run directly:

```bash
./termdoro.py
```

Or with Python:

```bash
python3 termdoro.py
```

Options:
- `-w, --work` minutes for work sessions (default: 25)
- `-b, --break` minutes for break sessions (default: 5)
- `-r, --rounds` number of work sessions to run (default: 1)
- `--auto` automatically start the next session without prompting
- `--no-bell` disable terminal bell on session end
- `--start-with {work,break}` start with a break or a work session (default: work)

Examples:
- One 25/5 round with prompts:
  ```bash
  ./termdoro.py
  ```
- Four 50/10 rounds, auto-advance, no bell:
  ```bash
  ./termdoro.py -w 50 -b 10 -r 4 --auto --no-bell
  ```
- Start with a break:
  ```bash
  ./termdoro.py --start-with break
  ```

## Notes
- Press Ctrl+C to stop at any time.
- The bell character may not produce sound on all terminals; the text alert always appears.
