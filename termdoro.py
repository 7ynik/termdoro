#!/usr/bin/env python3
"""
termdoro - Terminal Pomodoro Timer

A minimal terminal-based productivity timer that alternates between work and break sessions.

Usage examples:
  ./termdoro.py                 # 25/5 one round with prompts
  ./termdoro.py -w 50 -b 10 -r 4 --auto --no-bell
  ./termdoro.py --start-with break
"""
from __future__ import annotations
import argparse
import sys
import time
from typing import Literal


def fmt_mmss(seconds: int) -> str:
    m, s = divmod(max(0, seconds), 60)
    return f"{m:02d}:{s:02d}"


def bell(times: int = 2, enable: bool = True) -> None:
    if not enable:
        return
    for i in range(max(0, times)):
        # Terminal bell; may be silent depending on terminal settings.
        print("\a", end="", flush=True)
        # Small delay between bells without blocking too long
        time.sleep(0.05)


def countdown(total_seconds: int, label: str) -> None:
    """Render an inline countdown timer until zero."""
    start = time.monotonic()
    end = start + max(0, int(total_seconds))
    last_shown = None
    try:
        while True:
            now = time.monotonic()
            remaining = int(end - now)
            if remaining < 0:
                remaining = 0
            if remaining != last_shown:
                sys.stdout.write(f"\r{label}: {fmt_mmss(remaining)}")
                sys.stdout.flush()
                last_shown = remaining
            if remaining <= 0:
                break
            # Sleep a short amount so we update roughly once per second
            time.sleep(0.1)
    finally:
        # Ensure newline after finishing or on interruption
        print()


def prompt_to_continue(next_label: str, auto: bool) -> None:
    if auto:
        return
    try:
        input(f"Press Enter to start {next_label}...")
    except EOFError:
        # Non-interactive environment; just proceed.
        pass


def run_session(kind: Literal["WORK", "BREAK"], minutes: int, auto: bool, enable_bell: bool) -> None:
    seconds = max(0, int(minutes) * 60)
    countdown(seconds, f"{kind}")
    print(f"{kind} session complete.")
    bell(2, enable=enable_bell)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="termdoro - Terminal Pomodoro Timer")
    parser.add_argument("-w", "--work", type=int, default=25, help="work session duration in minutes (default: 25)")
    parser.add_argument("-b", "--break", dest="brk", type=int, default=5, help="break session duration in minutes (default: 5)")
    parser.add_argument("-r", "--rounds", type=int, default=1, help="number of work sessions to run (default: 1)")
    parser.add_argument("--auto", action="store_true", help="automatically start next session without prompting")
    parser.add_argument("--no-bell", action="store_true", help="disable terminal bell on session completion")
    parser.add_argument("--start-with", choices=["work", "break"], default="work", help="start with a break or work session (default: work)")
    args = parser.parse_args(argv)

    work_min = max(0, args.work)
    break_min = max(0, args.brk)
    rounds = max(0, args.rounds)
    auto = bool(args.auto)
    enable_bell = not bool(args.no_bell)

    try:
        if args.start_with == "break" and break_min > 0:
            print("Ready to begin: BREAK")
            prompt_to_continue("BREAK", auto)
            run_session("BREAK", break_min, auto, enable_bell)

        for i in range(rounds):
            # Work session
            print(f"Round {i + 1} of {rounds}: WORK")
            prompt_to_continue("WORK", auto)
            run_session("WORK", work_min, auto, enable_bell)

            # Break after work, unless it's the final round
            if i < rounds - 1 and break_min >= 0:
                print("Next up: BREAK")
                prompt_to_continue("BREAK", auto)
                run_session("BREAK", break_min, auto, enable_bell)

        print("All rounds complete. Great job!")
        return 0
    except KeyboardInterrupt:
        print("\nTimer interrupted. Exiting.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
