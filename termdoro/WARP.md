# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Common commands

- Run with defaults (25 min work, 5 min break, 1 round):
  - `./termdoro.py`
  - `python3 termdoro.py`
- Run with custom durations and behavior (examples):
  - Four 50/10 rounds, auto-advance, no bell: `./termdoro.py -w 50 -b 10 -r 4 --auto --no-bell`
  - Start with a break: `./termdoro.py --start-with break`
- Requirements: Python 3.8+; no external dependencies; no build step.
- Tests/Lint: No test or lint setup is included in this repo.

## Architecture overview

This is a single-file Python CLI timer (`termdoro.py`) with no external dependencies. It alternates WORK and BREAK sessions with an in-terminal countdown and optional bell.

- Entrypoint: `main()` parses CLI flags via `argparse`:
  - `--work/-w <int>` minutes per work session (default 25)
  - `--break/-b <int>` minutes per break session (default 5)
  - `--rounds/-r <int>` number of work sessions (default 1)
  - `--auto` auto-start next session without prompt
  - `--no-bell` disable bell at session end
  - `--start-with {work,break}` optional initial break before first work
- Control flow:
  - Optionally runs an initial BREAK if `--start-with break` and break duration > 0
  - For each round: run WORK, then (unless final round) run BREAK
  - Prints status lines like "Round i of N: WORK" and "Next up: BREAK"
  - KeyboardInterrupt is handled, exiting with code 130 and a friendly message
- Session execution (`run_session`):
  - Calls `countdown(total_seconds, label)` to render an inline MM:SS countdown using carriage returns and `time.monotonic()` for stable timing; updates roughly once per second; ensures a newline on finish or interruption
  - Emits a completion message and optional terminal bell via `bell(times=2)` (prints "\a" with small delays); bell audibility depends on terminal settings
- Utilities:
  - `fmt_mmss(seconds)` formats remaining time as `MM:SS`
  - `prompt_to_continue(next_label, auto)` gates session starts unless `--auto` is set; tolerates non-interactive stdin via `EOFError`
- Exit behavior:
  - Normal completion returns 0; Ctrl+C returns 130

Notes:
- Press Ctrl+C to stop at any time
- The bell may be silent depending on terminal configuration; textual completion messages always appear
