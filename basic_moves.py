from pidog import Pidog
import curses
from time import sleep


class PiDogController:
    """Initializes the PiDog with init values"""
    def __init__(self):
        self.stand_angles = [25, 25, -25, -25, 70, -45, -70, 45]
        self.sit_angles = [30, 30, -30, -30, 80, -45, -80, 45]
        
        self.dog = Pidog(  
            leg_init_angles=self.sit_angles,
            head_init_angles=[2, 2, -25],
            tail_init_angle=[0]
        )

        sleep(0.5)
        self.running = True
        self.status = "Bereit"
        
        
        
    def go_home(self, pose="stand"):
        if pose == "stand":
            self.stand()
        elif pose == "sit":
            self.sit()
    
    """Dog Lies down"""
    def lie_down(self):
        self.status = "Lie down"
        self.dog.do_action("lie", step_count=1, speed=100)
        
    
    def stand(self):
        self.status = "Stand"
        self.dog.do_action("stand", step_count=1, speed=70)
        
    def walkf(self):
        self.status = "Forward"
        self.dog.do_action("forward", step_count=3, speed=98)
        self.dog.wait_all_done()
        self.go_home("stand")

    def walkb(self):
        self.status = "Backward"
        self.dog.do_action("backward", step_count=3, speed=98)
        self.dog.wait_all_done()
        self.go_home("stand")


    def sit(self):
        self.status = "Sit"
        self.dog.legs_move([self.sit_angles], immediately=True, speed=80)
        self.dog.wait_legs_done()

    def doze_off(self):
        self.status = "Doze off"
        self.dog.do_action("doze_off", step_count=1, speed=100)

    def left(self):
        self.status = "Turn left"
        self.dog.do_action("turn_left", step_count=1, speed=120)
        self.dog.wait_all_done()
        self.go_home("stand")
        
    def right(self):
        self.status = "Turn right"
        self.dog.do_action("turn_right", step_count=1, speed=120)
        self.dog.wait_all_done()
        self.go_home("stand")
        
    def bark(self):
        self.status = "Bark"
        self.dog.do_action("head_bark", step_count=1, speed=100)
        self.dog.speak("single_bark_1", volume=50)
        sleep(1)

    def pushups(self):
        self.status = "Push ups"
        self.dog.do_action("push_up", step_count=4, speed=50)

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

    def shake_head(self, times=3, speed=100, angle=20):
        self.status = "Smooth shake head"

        home = [0, 0, -25]
        sequence = []

        for _ in range(times):
            sequence.extend([
                [5, 0, -25],
                [10, 0, -25],
                [15, 0, -25],
                [20, 0, -25],
                [15, 0, -25],
                [10, 0, -25],
                [5, 0, -25],
                [0, 0, -25],
                [-5, 0, -25],
                [-10, 0, -25],
                [-15, 0, -25],
                [-20, 0, -25],
                [-15, 0, -25],
                [-10, 0, -25],
                [-5, 0, -25],
                [0, 0, -25],
            ])

        sequence.append(home)

        self.dog.head_move(sequence, immediately=True, speed=speed)
        self.dog.wait_head_done()

    def stop(self):
        self.status = "Stop"
        self.dog.body_stop()

    def stop_and_sit(self):
        self.status = "Stop and sit"
        self.dog.body_stop()
        sleep(1)
        self.dog.do_action("sit", step_count=1, speed=100)

    def cleanup(self):
        try:
            self.dog.body_stop()
            self.dog.close()
        except Exception:
            pass

    def handle_key(self, key):
        if key == ord("w") or key == curses.KEY_UP:
            self.walkf()

        elif key == ord("s") or key == curses.KEY_DOWN:
            self.walkb()

        elif key == ord("a") or key == curses.KEY_LEFT:
            self.left()

        elif key == ord("d") or key == curses.KEY_RIGHT:
            self.right()

        elif key == ord("b"):
            self.bark()

        elif key == ord("e"):
            self.stand()

        elif key == ord("x"):
            self.sit()

        elif key == ord("l"):
            self.lie_down()

        elif key == ord("p"):
            self.pushups()

        elif key == ord("h"):
            self.wave()

        elif key == ord("n"):
            self.shake_head()

        elif key == ord(" "):
            self.stop()

        elif key == ord("q") or key == 27:
            self.running = False
            self.status = "Quit"


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
