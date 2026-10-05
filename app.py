import curses
from time import monotonic, sleep
import logging

from dog.controller import PiDogController
from ui.terminal_ui import draw_menu

logger = logging.getLogger(__name__)


def main(stdscr, start_idle=None):
    dog = PiDogController()
    if start_idle:
        dog.set_idle_mode(start_idle)
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
            dog.tick_idle_mode()

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