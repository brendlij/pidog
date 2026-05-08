import curses
import logging

logger = logging.getLogger(__name__)


def safe_addstr(stdscr, y, x, text):
    height, width = stdscr.getmaxyx()

    if y < 0 or x < 0:
        return

    if y >= height or x >= width:
        return

    max_len = width - x - 1

    if max_len <= 0:
        return

    try:
        stdscr.addstr(y, x, text[:max_len])
    except curses.error:
        logger.debug("Could not draw text at y=%s x=%s", y, x)


def draw_menu(stdscr, dog):
    stdscr.clear()

    lines_left = [
        "╔══════════════════════════════════════╗",
        "║           PiDog Controller           ║",
        "╚══════════════════════════════════════╝",
        "",
        "Movement",
        "  W / ↑      Forward",
        "  S / ↓      Backward",
        "  A / ←      Turn left",
        "  D / →      Turn right",
        "  T          Trot",
        "",
        "Basic Poses",
        "  E          Stand",
        "  X          Sit",
        "  F          Half sit",
        "  L          Lie down",
        "  O          Lie with hands out",
        "",
        "Actions",
        "  B          Bark",
        "  P          Push ups",
        "  G          Stretch",
        "  Z          Doze off",
        "  V          Nod lethargy",
        "  N          Shake head",
        "  U          Head up down",
        "  M          Wag tail",
        "  C          Act cute",
    ]

    lines_right = [
        "Head",
        "  J          Tilt head left",
        "  K          Tilt head right",
        "  I          Tilt head",
        "",
        "Custom Poses",
        "  R          Ready pose",
        "  Y          Chill pose",
        "",
        "Control",
        "  Space      Stop",
        "  Q / ESC    Quit",
        "",
        f"Status: {dog.status}",
    ]

    for y, line in enumerate(lines_left):
        safe_addstr(stdscr, y, 0, line)

    for y, line in enumerate(lines_right, start=4):
        safe_addstr(stdscr, y, 43, line)

    height, width = stdscr.getmaxyx()

    if height < 28 or width < 80:
        safe_addstr(
            stdscr,
            height - 1,
            0,
            "Terminal zu klein - bitte groesser machen"
        )

    stdscr.refresh()