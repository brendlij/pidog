import curses
from core.logger import setup_logging
from app import main


if __name__ == "__main__":
    setup_logging()
    curses.wrapper(main)