import logging


logger = logging.getLogger(__name__)


class DualTouchSensor:
    """Reads touch sensor data from the PiDog's head."""

    def __init__(self, dog):
        self.dog = dog

    def read(self):
        """
        Reads the dual touch sensor on the PiDog's head.
        
        Returns:
            str: One of the following values:
                - "LS": Touched from left to right (front to back)
                - "RS": Touched from right to left
                - "L": Left side only touched
                - "R": Right side only touched
                - "N": Not touched
        """
        try:
            return self.dog.dual_touch.read()
        except Exception:
            logger.exception("Could not read dual touch sensor")
            return "N"
