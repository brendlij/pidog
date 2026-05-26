import curses
import logging
import math
from time import monotonic, sleep

from core.logger import setup_logging
from dog.controller import PiDogController

logger = logging.getLogger(__name__)

# Default thresholds (g)
DEFAULT_LOW = 0.75
DEFAULT_HIGH = 1.25
DEFAULT_HOLD = 0.35
DEFAULT_COOLDOWN = 5.0


def run_curses(stdscr):
    setup_logging()
    dog = PiDogController()

    low = DEFAULT_LOW
    high = DEFAULT_HIGH
    hold = DEFAULT_HOLD
    cooldown = DEFAULT_COOLDOWN

    lift_start = None
    last_bark = -cooldown

    curses.cbreak()
    curses.noecho()
    stdscr.nodelay(True)
    stdscr.keypad(True)

    try:
        curses.curs_set(0)
    except curses.error:
        pass

    try:
        while dog.running:
            stdscr.clear()

            ax, ay, az = dog.accel_g_data
            mag = math.sqrt(ax * ax + ay * ay + az * az)
            now = monotonic()

            triggered = False
            if mag < low or mag > high:
                if lift_start is None:
                    lift_start = now
                elif now - lift_start >= hold and now - last_bark >= cooldown:
                    triggered = True
                    dog.handle_key(ord("b"))
                    last_bark = now
                    lift_start = None
            else:
                lift_start = None

            # Display
            stdscr.addstr(0, 0, "PiDog IMU Lift Tester")
            stdscr.addstr(2, 0, f"Accel g:  ax={ax:6.3f}  ay={ay:6.3f}  az={az:6.3f}")
            stdscr.addstr(3, 0, f"Magnitude: {mag:6.3f} g")
            stdscr.addstr(5, 0, "Thresholds (use keys to adjust):")
            stdscr.addstr(6, 0, f"  Low  (a/z): {low:5.3f} g")
            stdscr.addstr(7, 0, f"  High (s/x): {high:5.3f} g")
            stdscr.addstr(8, 0, f"  Hold (d/c): {hold:5.3f} s")
            stdscr.addstr(9, 0, f"  Cool (f/v): {cooldown:5.1f} s")

            status = "TRIGGERED!" if triggered else "idle"
            stdscr.addstr(11, 0, f"Status: {status}")
            stdscr.addstr(13, 0, "Keys: q=quit  r=reset thresholds")

            stdscr.refresh()

            # Input
            key = stdscr.getch()
            if key != -1:
                if key in (ord("q"), 27):
                    dog.running = False
                    break
                if key == ord("a"):
                    low = max(0.0, low - 0.05)
                if key == ord("z"):
                    low = low + 0.05
                if key == ord("s"):
                    high = max(0.0, high - 0.05)
                if key == ord("x"):
                    high = high + 0.05
                if key == ord("d"):
                    hold = max(0.05, hold - 0.05)
                if key == ord("c"):
                    hold = hold + 0.05
                if key == ord("f"):
                    cooldown = max(0.0, cooldown - 0.5)
                if key == ord("v"):
                    cooldown = cooldown + 0.5
                if key == ord("r"):
                    low = DEFAULT_LOW
                    high = DEFAULT_HIGH
                    hold = DEFAULT_HOLD
                    cooldown = DEFAULT_COOLDOWN

            sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        dog.cleanup()


if __name__ == "__main__":
    curses.wrapper(run_curses)
