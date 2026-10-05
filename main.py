import curses
import sys
from functools import partial

from core.logger import setup_logging
from app import main


if __name__ == "__main__":
    setup_logging()
    # python3 main.py --messe  -> start directly in trade-fair idle mode
    start_idle = "messe" if "--messe" in sys.argv[1:] else None
    curses.wrapper(partial(main, start_idle=start_idle))
