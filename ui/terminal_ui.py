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

    ax, ay, az = dog.accel_data
    gx, gy, gz = dog.gyro_data
    agx, agy, agz = dog.accel_g_data

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
        "  ,          Head backward",
        "  .          Head forward",
        "  J          Tilt head left",
        "  K          Tilt head right",
        "  I          Tilt head",
        "",
        "Custom Poses",
        "  R          Ready pose",
        "  Y          Chill pose",
        "",
        "Idle Modes (skeleton)",
        "  1          Calm",
        "  2          Curious",
        "  3          Sleepy",
        "  0          Off",
        f"  Active     {dog.idle_mode_name}",
        "",
        "Control",
        "  Space      Stop",
        "  Q / ESC    Quit",
        "",
        "IMU",
        f"  Accel raw  X:{ax:6d} Y:{ay:6d} Z:{az:6d}",
        f"  Gyro  raw  X:{gx:6d} Y:{gy:6d} Z:{gz:6d}",
        f"  Accel g    X:{agx:6.2f} Y:{agy:6.2f} Z:{agz:6.2f}",
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