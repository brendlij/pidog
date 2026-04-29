from pidog import Pidog
import curses
from time import sleep


from pidog import Pidog
import curses
from time import sleep


class PiDogActions:
    """All actions the dog can do."""

    def __init__(self, dog):
        self.dog = dog
        self.status = "Bereit"

        self.stand_angles = [25, 25, -25, -25, 70, -45, -70, 45]
        self.sit_angles = [30, 30, -30, -30, 80, -45, -80, 45]

    def go_home(self, pose="stand"):
        if pose == "stand":
            self.stand()
        elif pose == "sit":
            self.sit()

    def stand(self):
        self.status = "Stand"
        self.dog.do_action("stand", step_count=1, speed=70)
        self.dog.wait_all_done()

    def sit(self):
        self.status = "Sit"
        self.dog.legs_move([self.sit_angles], immediately=True, speed=80)
        self.dog.wait_legs_done()

    def walk_forward(self):
        self.status = "Forward"
        self.dog.do_action("forward", step_count=3, speed=98)
        self.dog.wait_all_done()
        self.go_home("stand")

    def walk_backward(self):
        self.status = "Backward"
        self.dog.do_action("backward", step_count=3, speed=98)
        self.dog.wait_all_done()
        self.go_home("stand")

    def turn_left(self):
        self.status = "Turn left"
        self.dog.do_action("turn_left", step_count=1, speed=120)
        self.dog.wait_all_done()
        self.go_home("stand")

    def turn_right(self):
        self.status = "Turn right"
        self.dog.do_action("turn_right", step_count=1, speed=120)
        self.dog.wait_all_done()
        self.go_home("stand")

    def lie_down(self):
        self.status = "Lie down"
        self.dog.do_action("lie", step_count=1, speed=100)
        self.dog.wait_all_done()

    def bark(self):
        self.status = "Bark"
        self.dog.do_action("head_bark", step_count=1, speed=100)
        self.dog.speak("single_bark_1", volume=50)
        sleep(1)
        self.go_home("sit")

    def pushups(self):
        self.status = "Push ups"
        self.dog.do_action("push_up", step_count=4, speed=50)
        self.dog.wait_all_done()
        self.go_home("stand")

    def wave(self):
        self.status = "Wave"

        sit = self.sit_angles

        paw_up = [10, -35, -30, -30, 80, -45, -80, 45]
        paw_left = [10, -10, -30, -30, 80, -45, -80, 45]
        paw_right = [10, -55, -30, -30, 80, -45, -80, 45]

        self.dog.legs_move([sit], immediately=True, speed=80)
        self.dog.wait_legs_done()

        for _ in range(3):
            self.dog.legs_move(
                [paw_up, paw_left, paw_up, paw_right],
                immediately=False,
                speed=80
            )

        self.dog.wait_legs_done()
        self.go_home("sit")

    def shake_head(self):
        self.status = "Shake head"

        home = [0, 0, -25]

        sequence = [
            [10, 0, -25],
            [20, 0, -25],
            [10, 0, -25],
            [0, 0, -25],
            [-10, 0, -25],
            [-20, 0, -25],
            [-10, 0, -25],
            [0, 0, -25],
        ]

        for _ in range(3):
            self.dog.head_move(sequence, immediately=True, speed=100)
            self.dog.wait_head_done()

        self.dog.head_move([home], immediately=True, speed=80)
        self.dog.wait_head_done()

    def stop(self):
        self.status = "Stop"
        self.dog.body_stop()


class PiDogController:
    """Keyboard controller for the PiDog."""

    def __init__(self):
        self.dog = Pidog(
            leg_init_angles=[30, 30, -30, -30, 80, -45, -80, 45],
            head_init_angles=[2, 2, -25],
            tail_init_angle=[0]
        )

        sleep(0.5)

        self.actions = PiDogActions(self.dog)
        self.running = True

    @property
    def status(self):
        return self.actions.status

    def handle_key(self, key):
        if key == ord("w") or key == curses.KEY_UP:
            self.actions.walk_forward()

        elif key == ord("s") or key == curses.KEY_DOWN:
            self.actions.walk_backward()

        elif key == ord("a") or key == curses.KEY_LEFT:
            self.actions.turn_left()

        elif key == ord("d") or key == curses.KEY_RIGHT:
            self.actions.turn_right()

        elif key == ord("e"):
            self.actions.stand()

        elif key == ord("x"):
            self.actions.sit()

        elif key == ord("l"):
            self.actions.lie_down()

        elif key == ord("b"):
            self.actions.bark()

        elif key == ord("p"):
            self.actions.pushups()

        elif key == ord("h"):
            self.actions.wave()

        elif key == ord("n"):
            self.actions.shake_head()

        elif key == ord(" "):
            self.actions.stop()

        elif key == ord("q") or key == 27:
            self.running = False
            self.actions.status = "Quit"

    def cleanup(self):
        try:
            self.dog.body_stop()
            self.dog.close()
        except Exception:
            pass

def draw_menu(stdscr, dog):
    stdscr.clear()

    stdscr.addstr(0, 0, "╔══════════════════════════════════════╗")
    stdscr.addstr(1, 0, "║           PiDog Controller           ║")
    stdscr.addstr(2, 0, "╚══════════════════════════════════════╝")

    stdscr.addstr(4, 0, "Movement")
    stdscr.addstr(5, 0, "  W / ↑      Forward")
    stdscr.addstr(6, 0, "  S / ↓      Backward")
    stdscr.addstr(7, 0, "  A / ←      Turn left")
    stdscr.addstr(8, 0, "  D / →      Turn right")

    stdscr.addstr(10, 0, "Actions")
    stdscr.addstr(11, 0, "  E          Stand")
    stdscr.addstr(12, 0, "  X          Sit")
    stdscr.addstr(13, 0, "  L          Lie down")
    stdscr.addstr(14, 0, "  H          Wave")
    stdscr.addstr(15, 0, "  B          Bark")
    stdscr.addstr(16, 0, "  N          Shake head")
    stdscr.addstr(17, 0, "  P          Push ups")

    stdscr.addstr(19, 0, "Control")
    stdscr.addstr(20, 0, "  Space      Stop")
    stdscr.addstr(21, 0, "  Q / ESC    Quit")

    stdscr.addstr(23, 0, f"Status: {dog.status}")

    stdscr.refresh()


def main(stdscr):
    dog = PiDogController()

    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)

    stdscr.nodelay(True)
    stdscr.keypad(True)

    try:
        while dog.running:
            draw_menu(stdscr, dog)

            key = stdscr.getch()

            if key != -1:
                dog.handle_key(key)

            sleep(0.05)

    finally:
        dog.cleanup()


if __name__ == "__main__":
    curses.wrapper(main)
