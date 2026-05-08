import logging
import time

logger = logging.getLogger(__name__)


class FaceDetectionSensor:
    """Wrapper around vilib face detection (if available).

    Provides a stable API: read(), is_detected(), direction().
    """

    def __init__(self, dog=None):
        self.dog = dog
        self._available = False
        self._last = {
            'human_x': 0,
            'human_y': 0,
            'human_w': 0,
            'human_h': 0,
            'human_n': 0,
        }

        try:
            from vilib import Vilib

            self._Vilib = Vilib
            # Start camera/display only if running on actual device.
            try:
                self._Vilib.camera_start(vflip=False, hflip=False)
                # Do not force web display here; let user configure if needed
                # self._Vilib.display(local=True, web=True)
                self._Vilib.face_detect_switch(True)
                self._available = True
                logger.info("Vilib camera started and face detection enabled")
                time.sleep(0.5)
            except Exception:
                logger.exception("Could not start Vilib camera; face detection may not work")
        except Exception:
            logger.debug("vilib not available; face detection disabled")
            self._Vilib = None

    def read(self):
        """Return the latest detection parameters as a dict."""
        if not self._available:
            return dict(self._last)

        try:
            params = self._Vilib.detect_obj_parameter
n            # Extract known keys
            for k in ('human_x', 'human_y', 'human_w', 'human_h', 'human_n'):
                if k in params:
                    self._last[k] = int(params[k])
            return dict(self._last)
        except Exception:
            logger.exception("Error reading face detection parameters")
            return dict(self._last)

    def is_detected(self):
        data = self.read()
        return bool(data.get('human_n', 0))

    def direction(self, width=320, deadzone=40):
        """Return 'left', 'right' or 'center' based on detected face center.

        - `width` is camera width in pixels
        - `deadzone` is half-width around center considered 'center'
        """
        data = self.read()
        n = data.get('human_n', 0)
        if not n:
            return 'none'

        cx = data.get('human_x', width // 2)
        center = width // 2
        if cx < center - deadzone:
            return 'left'
        if cx > center + deadzone:
            return 'right'
        return 'center'
