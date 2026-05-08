import logging


logger = logging.getLogger(__name__)


class IMUSensor:
    """Reads acceleration and gyroscope data from the PiDog IMU."""

    def __init__(self, dog):
        self.dog = dog

    def read_accel_raw(self):
        """Returns raw accelerometer values (ax, ay, az)."""
        return self._read_triplet("accData")

    def read_gyro_raw(self):
        """Returns raw gyroscope values (gx, gy, gz)."""
        return self._read_triplet("gyroData")

    def read_accel_g(self):
        """Returns acceleration in g units using 16384 LSB/g scale."""
        ax, ay, az = self.read_accel_raw()
        scale = 16384.0
        return ax / scale, ay / scale, az / scale

    def _read_triplet(self, attribute_name):
        try:
            values = getattr(self.dog, attribute_name)
        except Exception:
            logger.exception("Could not read IMU attribute: %s", attribute_name)
            return 0, 0, 0

        if not values or len(values) < 3:
            logger.warning("IMU attribute %s did not return three values", attribute_name)
            return 0, 0, 0

        try:
            return int(values[0]), int(values[1]), int(values[2])
        except Exception:
            logger.exception("Could not parse IMU values for %s: %s", attribute_name, values)
            return 0, 0, 0
