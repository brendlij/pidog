import curses
from time import sleep
import logging

from dog.controller import PiDogController
from ui.terminal_ui import draw_menu

logger = logging.getLogger(__name__)


def main(stdscr):
    dog = PiDogController()

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