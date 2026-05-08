import curses
import logging
from time import sleep
import threading

from pidog import Pidog

from dog.actions import PiDogActions
from sensors.imu import IMUSensor

logger = logging.getLogger(__name__)


class PiDogController:
    """Keyboard controller for the PiDog."""

    def __init__(self, dog=None):
        self.dog = dog or Pidog(
            leg_init_angles=[30, 30, -30, -30, 80, -45, -80, 45],
            head_init_angles=[2, 2, -25],
            tail_init_angle=[0]
        )

        sleep(0.5)

        self.actions = PiDogActions(self.dog)
        self.imu = IMUSensor(self.dog)
        self.running = True

        self.setup_keybindings()

        logger.info("PiDog controller started")

    @property
    def status(self):
        return self.actions.status

    @property
    def accel_data(self):
        return self.imu.read_accel_raw()

    @property
    def accel_g_data(self):
        return self.imu.read_accel_g()

    @property
    def gyro_data(self):
        return self.imu.read_gyro_raw()

    def log_imu(self):
        ax, ay, az = self.accel_data
        gx, gy, gz = self.gyro_data
        agx, agy, agz = self.accel_g_data

        logger.info(
            "IMU accel_raw=(%d, %d, %d) accel_g=(%.3f, %.3f, %.3f) gyro_raw=(%d, %d, %d)",
            ax,
            ay,
            az,
            agx,
            agy,
            agz,
            gx,
            gy,
            gz,
        )

    def setup_keybindings(self):
        self.keybindings = {
            ord("w"): self.actions.walk_forward,
            curses.KEY_UP: self.actions.walk_forward,

            ord("s"): self.actions.walk_backward,
            curses.KEY_DOWN: self.actions.walk_backward,

            ord("a"): self.actions.turn_left,
            curses.KEY_LEFT: self.actions.turn_left,

            ord("d"): self.actions.turn_right,
            curses.KEY_RIGHT: self.actions.turn_right,

            ord("e"): self.actions.stand,
            ord("x"): self.actions.sit,
            ord("f"): self.actions.half_sit,
            ord("l"): self.actions.lie_down,
            ord("o"): self.actions.lie_with_hands_out,

            ord("b"): self.actions.bark,
            ord("p"): self.actions.pushups,
            ord("t"): self.actions.trot,
            ord("g"): self.actions.stretch,
            ord("z"): self.actions.doze_off,
            ord("v"): self.actions.nod_lethargy,
            ord("n"): self.actions.shake_head_action,

            ord("j"): self.actions.tilting_head_left,
            ord("k"): self.actions.tilting_head_right,
            ord("i"): self.actions.tilting_head,
            ord("u"): self.actions.head_up_down,
            ord("m"): self.actions.wag_tail,
            ord("c"): self.actions.act_cute,

            ord("r"): self.actions.ready_pose,
            ord("y"): self.actions.chill_pose,

            ord(" "): self.actions.stop,
        }

    def handle_key(self, key):
        if key in (ord("q"), 27):
            self.running = False
            self.actions.status = "Quit"
            self.actions.led_quit()
            logger.info("Quit requested")
            return

        action = self.keybindings.get(key)

        if action:
            logger.info("Key pressed: %s", key)

            try:
                action()
            except Exception:
                logger.exception("Action failed for key: %s", key)
                self.actions.status = "Fehler"
        else:
            logger.debug("Unknown key pressed: %s", key)

    def cleanup(self):
        logger.info("Cleanup started")

        try:
            self.actions.led_quit()
        except Exception:
            logger.exception("LED cleanup failed")

        try:
            self.dog.body_stop()
        except Exception:
            logger.exception("Body stop cleanup failed")

        try:
            self.dog.close()
        except Exception:
            logger.exception("Dog close cleanup failed")

        logger.info("Cleanup finished")