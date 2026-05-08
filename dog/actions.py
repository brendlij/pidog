from time import sleep
import logging

logger = logging.getLogger(__name__)

class PiDogActions:
    """All actions the dog can do."""

    def __init__(self, dog):
        self.dog = dog
        self.status = "Ready"

        self.stand_angles = [25, 25, -25, -25, 70, -45, -70, 45]
        self.sit_angles = [30, 30, -30, -30, 80, -45, -80, 45]

        self.led_idle()
        # Track a simple head pitch state for manual forward/back control.
        initial_pitch = -25
        try:
            init = getattr(self.dog, "head_init_angles", None)
            if init and len(init) >= 3:
                initial_pitch = int(init[2])
        except Exception:
            logger.debug("Could not read head_init_angles from dog, using default")

        self.head_pitch = initial_pitch

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
        self.set_led(style="breath", color="blue", bps=1, brightness=0.3)

    def led_move(self):
        self.set_led(style="boom", color="cyan", bps=2, brightness=0.6)

    def led_action(self):
        self.set_led(style="breath", color="magenta", bps=2, brightness=0.5)

    def led_cute(self):
        self.set_led(style="breath", color="pink", bps=1, brightness=0.7)

    def led_bark(self):
        self.set_led(style="bark", color="red", bps=2, brightness=0.8)

    def led_stop(self):
        self.set_led(style="boom", color="yellow", bps=2, brightness=0.6)

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
            self.status = f"Error during {status}"

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
            self.status = "Error during Bark"

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
            self.status = "Error during Push ups"

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
            self.set_led(style="breath", color="white", bps=1, brightness=0.25)
            self.do_action("doze_off", step_count=1, speed=40)

            logger.info("Action finished: Doze off")

        except Exception:
            logger.exception("Action failed: Doze off")
            self.status = "Error during Doze off"

    def nod_lethargy(self):
        self.status = "Nod lethargy"
        logger.info("Action started: Nod lethargy")

        try:
            self.set_led(style="breath", color="cyan", bps=1, brightness=0.3)
            self.do_action("nod_lethargy", step_count=3, speed=40)

            logger.info("Action finished: Nod lethargy")

        except Exception:
            logger.exception("Action failed: Nod lethargy")
            self.status = "Error during Nod lethargy"

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
        self.status = "Tilting head left"
        logger.info("Action started: Tilting head left")

        try:
            self.led_cute()

            # Preserve current forward/back pitch when tilting left/right.
            roll = 15
            pitch = int(getattr(self, "head_pitch", -25))
            self.dog.head_move([[0, roll, pitch]], immediately=True, speed=40)
            self.dog.wait_head_done()

            logger.info("Action finished: Tilting head left")

        except Exception:
            logger.exception("Action failed: Tilting head left")
            self.status = "Error during Tilting head left"

    def tilting_head_right(self):
        self.status = "Tilting head right"
        logger.info("Action started: Tilting head right")

        try:
            self.led_cute()

            # Preserve current forward/back pitch when tilting left/right.
            roll = -15
            pitch = int(getattr(self, "head_pitch", -25))
            self.dog.head_move([[0, roll, pitch]], immediately=True, speed=40)
            self.dog.wait_head_done()

            logger.info("Action finished: Tilting head right")

        except Exception:
            logger.exception("Action failed: Tilting head right")
            self.status = "Error during Tilting head right"

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

    def head_forward(self, step=5):
        """Move the head forward by increasing pitch (degrees).

        This keeps a simple internal pitch state and issues an absolute
        head_move using that pitch. The method clamps values to a
        sensible range to avoid extreme angles.
        """
        self.status = "Head forward"
        try:
            self.head_pitch = min(self.head_pitch + int(step), 60)
            self.dog.head_move([[0, 0, int(self.head_pitch)]], immediately=True, speed=50)
            self.dog.wait_head_done()
            logger.info("Head moved forward to pitch=%s", self.head_pitch)
        except Exception:
            logger.exception("Head forward failed")
            self.status = "Error during Head forward"

    def head_backward(self, step=5):
        """Move the head backward by decreasing pitch (degrees)."""
        self.status = "Head backward"
        try:
            self.head_pitch = max(self.head_pitch - int(step), -60)
            self.dog.head_move([[0, 0, int(self.head_pitch)]], immediately=True, speed=50)
            self.dog.wait_head_done()
            logger.info("Head moved backward to pitch=%s", self.head_pitch)
        except Exception:
            logger.exception("Head backward failed")
            self.status = "Error during Head backward"

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
            self.status = "Error during Act cute"

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
            self.status = f"Error during {status}"

    def ready_pose(self):
        self.set_led(style="breath", color="green", bps=1, brightness=0.6)

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
            self.set_led(style="breath", color="pink", bps=1, brightness=0.5)

            chill_angles = [35, 35, -35, -35, 90, -50, -90, 50]

            self.dog.legs_move([chill_angles], immediately=True, speed=60)
            self.dog.wait_legs_done()

            self.dog.head_move([[0, 10, -20]], immediately=True, speed=60)
            self.dog.wait_head_done()

            logger.info("Pose finished: Chill pose")

        except Exception:
            logger.exception("Pose failed: Chill pose")
            self.status = "Error during Chill pose"

    def stop(self):
        self.status = "Stop"
        logger.info("Stop requested")

        try:
            self.led_stop()
            self.dog.body_stop()

        except Exception:
            logger.exception("Stop failed")
            self.status = "Error during Stop"