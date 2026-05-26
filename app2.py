import curses
from math import sqrt
from time import monotonic, sleep
import logging

from core.logger import setup_logging
from dog.controller import PiDogController
from ui.terminal_ui import draw_menu

logger = logging.getLogger(__name__)

LIFT_ACCEL_LOW = 0.75
LIFT_ACCEL_HIGH = 1.25
LIFT_HOLD_SECONDS = 0.35
LIFT_BARK_COOLDOWN = 5.0


def main(stdscr):
    dog = PiDogController()
    last_imu_log_ts = 0.0
    lift_out_of_range_since = None
    last_lift_bark_ts = -LIFT_BARK_COOLDOWN

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

            ax, ay, az = dog.accel_g_data
            accel_magnitude = sqrt(ax * ax + ay * ay + az * az)

            if accel_magnitude < LIFT_ACCEL_LOW or accel_magnitude > LIFT_ACCEL_HIGH:
                if lift_out_of_range_since is None:
                    lift_out_of_range_since = now
                elif (
                    now - lift_out_of_range_since >= LIFT_HOLD_SECONDS
                    and now - last_lift_bark_ts >= LIFT_BARK_COOLDOWN
                ):
                    logger.info(
                        "Lift detected via accel magnitude %.3f, triggering bark",
                        accel_magnitude,
                    )
                    dog.handle_key(ord("b"))
                    last_lift_bark_ts = now
                    lift_out_of_range_since = None
            else:
                lift_out_of_range_since = None

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


if __name__ == "__main__":
    setup_logging()
    curses.wrapper(main)