import logging


logger = logging.getLogger(__name__)


class UltraSonic:
    def __init__(self, dog):
        self.dog = dog

    def read(self):
        """
        Reads the distance from the Sensor at Dog Head
        """
        try:
            distance = self.dog.ultrasonic.read_distance()
            return round(distance,2)
        except Exception:
            logger.exception("Could not read ultrasonic sensor")+