import curses
from time import monotonic, sleep
import logging

from dog.controller import PiDogController
from ui.terminal_ui import draw_menu

logger = logging.getLogger(__name__)


def main(stdscr):
    dog = PiDogController()
    last_imu_log_ts = 0.0

    curses.cbreak()
    curses.noecho()

    try:
        curses.curs_set(0)
    except curses.error:
        logger.warning("Could not hide cursor")

    stdscr.nodelay(True)
    stdscr.keypad(True)

    try:
        while dog.running:
            draw_menu(stdscr, dog)

            now = monotonic()

            if now - last_imu_log_ts >= 1.0:
                dog.log_imu()
                last_imu_log_ts = now

            key = stdscr.getch()

            if key != -1:
                dog.handle_key(key)

            sleep(0.05)

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received")

    except Exception:
        logger.exception("Main loop crashed")

    finally:
        dog.cleanup()