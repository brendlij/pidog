from pidog import Pidog
import curses
from time import sleep
import logging


# ---------- Logging ----------

logging.basicConfig(
    filename="pidog_controller.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("PiDogController")


class PiDogActions:
    """All actions the dog can do."""

    def __init__(self, dog):
        self.dog = dog
        self.status = "Bereit"

        self.stand_angles = [25, 25, -25, -25, 70, -45, -70, 45]
        self.sit_angles = [30, 30, -30, -30, 80, -45, -80, 45]

        self.led_idle()

    # ---------- LEDs ----------

    def set_led(self, style="breath", color="white", bps=1, brightness=0.5):
        try:
            self.dog.rgb_strip.set_mode(
                style=style,
                color=color,
                bps=bps,
                brightness=brightness
            )
        except Exception:
            logger.exception("Could not set LED")

    def led_idle(self):
        self.set_led(style="breath", color="blue", bps=0.8, brightness=0.3)

    def led_move(self):
        self.set_led(style="boom", color="cyan", bps=2, brightness=0.6)

    def led_action(self):
        self.set_led(style="breath", color="magenta", bps=1.5, brightness=0.5)

    def led_cute(self):
        self.set_led(style="breath", color="pink", bps=1.2, brightness=0.7)

    def led_bark(self):
        self.set_led(style="bark", color="red", bps=2.5, brightness=0.8)

    def led_stop(self):
        self.set_led(style="boom", color="yellow", bps=1.5, brightness=0.6)

    def led_quit(self):
        try:
            self.dog.rgb_strip.close()
        except Exception:
            logger.exception("Could not close LED strip")

    # ---------- Helpers ----------

    def do_action(self, action_name, step_count=1, speed=50):
        self.dog.do_action(action_name, step_count=step_count, speed=speed)
        self.dog.wait_all_done()

    def go_home(self, pose="stand"):
        if pose == "stand":
            self.stand()
        elif pose == "sit":
            self.sit()

    def run_action(
        self,
        status,
        action_name,
        led_func=None,
        step_count=1,
        speed=50,
        home_pose=None
    ):
        self.status = status
        logger.info("Action started: %s", status)

        if led_func:
            led_func()

        try:
            self.do_action(action_name, step_count=step_count, speed=speed)

            if home_pose:
                self.go_home(home_pose)

            logger.info("Action finished: %s", status)

        except Exception:
            logger.exception("Action failed: %s", status)
            self.status = f"Fehler bei {status}"

    # ---------- Basic Movement ----------

    def stand(self):
        self.run_action(
            status="Stand",
            action_name="stand",
            led_func=self.led_idle,
            speed=70
        )

    def sit(self):
        self.run_action(
            status="Sit",
            action_name="sit",
            led_func=self.led_idle,
            speed=70
        )

    def half_sit(self):
        self.run_action(
            status="Half sit",
            action_name="half_sit",
            led_func=self.led_action,
            speed=60
        )

    def lie_down(self):
        self.run_action(
            status="Lie down",
            action_name="lie",
            led_func=self.led_action,
            speed=80
        )

    def lie_with_hands_out(self):
        self.run_action(
            status="Lie with hands out",
            action_name="lie_with_hands_out",
            led_func=self.led_cute,
            speed=70
        )

    def walk_forward(self):
        self.run_action(
            status="Forward",
            action_name="forward",
            led_func=self.led_move,
            step_count=3,
            speed=98,
            home_pose="stand"
        )

    def walk_backward(self):
        self.run_action(
            status="Backward",
            action_name="backward",
            led_func=self.led_move,
            step_count=3,
            speed=98,
            home_pose="stand"
        )

    def turn_left(self):
        self.run_action(
            status="Turn left",
            action_name="turn_left",
            led_func=self.led_move,
            step_count=1,
            speed=120,
            home_pose="stand"
        )

    def turn_right(self):
        self.run_action(
            status="Turn right",
            action_name="turn_right",
            led_func=self.led_move,
            step_count=1,
            speed=120,
            home_pose="stand"
        )

    def trot(self):
        self.run_action(
            status="Trot",
            action_name="trot",
            led_func=self.led_move,
            step_count=4,
            speed=90,
            home_pose="stand"
        )

    # ---------- Tricks ----------

    def bark(self):
        self.status = "Bark"
        logger.info("Action started: Bark")

        try:
            self.led_bark()

            self.dog.do_action("head_bark", step_count=1, speed=100)
            self.dog.speak("single_bark_1", volume=50)

            sleep(1)

            self.dog.wait_all_done()
            self.go_home("sit")

            logger.info("Action finished: Bark")

        except Exception:
            logger.exception("Action failed: Bark")
            self.status = "Fehler bei Bark"

    def pushups(self):
        self.status = "Push ups"
        logger.info("Action started: Push ups")

        try:
            self.led_action()

            self.do_action("half_sit", speed=60)
            self.do_action("push_up", step_count=4, speed=60)

            self.go_home("stand")

            logger.info("Action finished: Push ups")

        except Exception:
            logger.exception("Action failed: Push ups")
            self.status = "Fehler bei Push ups"

    def stretch(self):
        self.run_action(
            status="Stretch",
            action_name="stretch",
            led_func=self.led_action,
            step_count=1,
            speed=60
        )

    def doze_off(self):
        self.status = "Doze off"
        logger.info("Action started: Doze off")

        try:
            self.set_led(style="breath", color="white", bps=0.4, brightness=0.25)
            self.do_action("doze_off", step_count=1, speed=40)

            logger.info("Action finished: Doze off")

        except Exception:
            logger.exception("Action failed: Doze off")
            self.status = "Fehler bei Doze off"

    def nod_lethargy(self):
        self.status = "Nod lethargy"
        logger.info("Action started: Nod lethargy")

        try:
            self.set_led(style="breath", color="cyan", bps=0.5, brightness=0.3)
            self.do_action("nod_lethargy", step_count=3, speed=40)

            logger.info("Action finished: Nod lethargy")

        except Exception:
            logger.exception("Action failed: Nod lethargy")
            self.status = "Fehler bei Nod lethargy"

    def shake_head_action(self):
        self.run_action(
            status="Shake head",
            action_name="shake_head",
            led_func=self.led_action,
            step_count=3,
            speed=80
        )

        self.led_idle()

    def tilting_head_left(self):
        self.run_action(
            status="Tilting head left",
            action_name="tilting_head_left",
            led_func=self.led_cute,
            step_count=1,
            speed=40
        )

    def tilting_head_right(self):
        self.run_action(
            status="Tilting head right",
            action_name="tilting_head_right",
            led_func=self.led_cute,
            step_count=1,
            speed=40
        )

    def tilting_head(self):
        self.run_action(
            status="Tilting head",
            action_name="tilting_head",
            led_func=self.led_cute,
            step_count=5,
            speed=30
        )

    def head_up_down(self):
        self.run_action(
            status="Head up down",
            action_name="head_up_down",
            led_func=self.led_action,
            step_count=4,
            speed=60
        )

    def wag_tail(self):
        self.run_action(
            status="Wag tail",
            action_name="wag_tail",
            led_func=self.led_cute,
            step_count=20,
            speed=90
        )

    def act_cute(self):
        self.status = "Act cute"
        logger.info("Action started: Act cute")

        try:
            self.led_cute()

            self.dog.do_action("sit", speed=60)
            self.dog.do_action("wag_tail", step_count=30, speed=90)
            self.dog.do_action("tilting_head", step_count=5, speed=25)

            self.dog.wait_all_done()
            self.dog.wait_head_done()

            logger.info("Action finished: Act cute")

        except Exception:
            logger.exception("Action failed: Act cute")
            self.status = "Fehler bei Act cute"

    # ---------- Custom Poses ----------

    def move_legs_pose(self, status, angles, led_func=None, speed=70):
        self.status = status
        logger.info("Pose started: %s", status)

        if led_func:
            led_func()

        try:
            self.dog.legs_move([angles], immediately=True, speed=speed)
            self.dog.wait_legs_done()

            logger.info("Pose finished: %s", status)

        except Exception:
            logger.exception("Pose failed: %s", status)
            self.status = f"Fehler bei {status}"

    def ready_pose(self):
        self.set_led(style="breath", color="green", bps=1.2, brightness=0.6)

        ready_angles = [20, 20, -20, -20, 65, -40, -65, 40]

        self.move_legs_pose(
            status="Ready pose",
            angles=ready_angles,
            speed=70
        )

    def chill_pose(self):
        self.status = "Chill pose"
        logger.info("Pose started: Chill pose")

        try:
            self.set_led(style="breath", color="pink", bps=0.7, brightness=0.5)

            chill_angles = [35, 35, -35, -35, 90, -50, -90, 50]

            self.dog.legs_move([chill_angles], immediately=True, speed=60)
            self.dog.wait_legs_done()

            self.dog.head_move([[0, 10, -20]], immediately=True, speed=60)
            self.dog.wait_head_done()

            logger.info("Pose finished: Chill pose")

        except Exception:
            logger.exception("Pose failed: Chill pose")
            self.status = "Fehler bei Chill pose"

    def stop(self):
        self.status = "Stop"
        logger.info("Stop requested")

        try:
            self.led_stop()
            self.dog.body_stop()

        except Exception:
            logger.exception("Stop failed")
            self.status = "Fehler bei Stop"


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
        self.running = True

        self.setup_keybindings()

        logger.info("PiDog controller started")

    @property
    def status(self):
        return self.actions.status

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


if __name__ == "__main__":
    curses.wrapper(main)