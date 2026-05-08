import curses
import logging
from time import monotonic, sleep
from threading import Lock, Thread

from pidog import Pidog

from dog.actions import PiDogActions
from dog.idle_modes import IdleModeManager
from sensors.imu import IMUSensor
from sensors.sdd import SDDSensor
from sensors.dual_touch import DualTouchSensor

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
        self.idle_modes = IdleModeManager(self.actions)
        self.imu = IMUSensor(self.dog)
        self.sdd = SDDSensor(self.dog)
        self.dual_touch = DualTouchSensor(self.dog)
        self.running = True
        self._action_thread = None
        self._action_lock = Lock()

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

    @property
    def sound_direction(self):
        return self.sdd.read_direction()

    @property
    def sound_detected(self):
        return self.sdd.is_detected()

    @property
    def idle_mode_name(self):
        return self.idle_modes.active_name

    def log_imu(self):
        ax, ay, az = self.accel_data
        gx, gy, gz = self.gyro_data
        agx, agy, agz = self.accel_g_data
        detected = self.sound_detected
        direction = self.sound_direction

        logger.info(
            "IMU accel_raw=(%d, %d, %d) accel_g=(%.3f, %.3f, %.3f) gyro_raw=(%d, %d, %d) sdd_detected=%s sdd_dir=%d",
            ax,
            ay,
            az,
            agx,
            agy,
            agz,
            gx,
            gy,
            gz,
            detected,
            direction,
        )

    def set_idle_mode(self, mode_name):
        if self.idle_modes.enable(mode_name):
            self.actions.status = f"Idle mode: {mode_name}"

    def disable_idle_mode(self):
        self.idle_modes.disable()
        self.actions.status = "Idle mode: off"

    def tick_idle_mode(self):
        self.idle_modes.tick(monotonic())

    def _is_action_running(self):
        with self._action_lock:
            return self._action_thread is not None and self._action_thread.is_alive()

    def _run_action_async(self, action_name, action_callable):
        if self._is_action_running():
            logger.info("Action ignored because another action is still running: %s", action_name)
            return False

        def worker():
            try:
                action_callable()
            except Exception:
                logger.exception("Action failed: %s", action_name)
                self.actions.status = f"Error during {action_name}"
            finally:
                with self._action_lock:
                    self._action_thread = None

        thread = Thread(target=worker, daemon=True)

        with self._action_lock:
            self._action_thread = thread

        thread.start()
        return True

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
            ord(","): self.actions.head_backward,
            ord("."): self.actions.head_forward,
            ord("m"): self.actions.wag_tail,
            ord("c"): self.actions.act_cute,

            ord("r"): self.actions.ready_pose,
            ord("y"): self.actions.chill_pose,

            ord("1"): lambda: self.set_idle_mode("calm"),
            ord("2"): lambda: self.set_idle_mode("curious"),
            ord("3"): lambda: self.set_idle_mode("sleepy"),
            ord("0"): self.disable_idle_mode,

            ord(" "): self.actions.stop,
        }

    def handle_key(self, key):
        if key in (ord("q"), 27):
            self.running = False
            self.actions.status = "Quit"
            self.actions.led_quit()
            logger.info("Quit requested")
            return

        if key == ord(" "):
            self.actions.stop()
            return

        action = self.keybindings.get(key)

        if action:
            logger.info("Key pressed: %s", key)

            try:
                if key != ord(" "):
                    # if action is a controller method (toggle), call directly
                    if getattr(action, "__self__", None) is self:
                        try:
                            action()
                        except Exception:
                            logger.exception("Controller action failed for key: %s", key)
                    else:
                        self._run_action_async(str(key), action)
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

        with self._action_lock:
            action_thread = self._action_thread

        if action_thread and action_thread.is_alive():
            action_thread.join(timeout=1.0)

        try:
            self.dog.close()
        except Exception:
            logger.exception("Dog close cleanup failed")

        pass

        logger.info("Cleanup finished")

    pass