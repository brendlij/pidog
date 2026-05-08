import logging


logger = logging.getLogger(__name__)


class SDDSensor:
    """Detects sound direction from the PiDog in degrees."""

    def __init__(self, dog):
        self.dog = dog

    def is_detected(self):
        """Returns True when the sound direction module detects sound."""
        try:
            return bool(self.dog.ears.isdetected())
        except Exception:
            logger.exception("Could not read SDD detection state via ears.isdetected()")
            return False

    def read_direction(self):
        """Returns sound direction in degrees (0-359), or -1 if unavailable."""
        try:
            value = self.dog.ears.read()
            return int(value)
        except Exception:
            logger.exception("Could not read sound direction via ears.read(); using fallback")
            return self._read_direction_fallback("dirData")

    def _read_direction_fallback(self, attribute_name):
        try:
            value = getattr(self.dog, attribute_name)
        except Exception:
            logger.exception("Could not read SDD fallback attribute: %s", attribute_name)
            return -1

        if value is None:
            logger.warning("SDD attribute %s returned None", attribute_name)
            return -1

        # Some implementations may return a sequence, keep only first element.
        if isinstance(value, (list, tuple)):
            if not value:
                logger.warning("SDD attribute %s returned an empty sequence", attribute_name)
                return -1
            value = value[0]

        try:
            return int(value)
        except Exception:
            logger.exception("Could not parse SDD value for %s: %s", attribute_name, value)
            return -1