import logging


logger = logging.getLogger(__name__)


class BaseIdleMode:
    """Base skeleton for an idle mode strategy."""

    name = "base"
    interval_sec = 3.0

    def __init__(self, actions):
        self.actions = actions

    def on_enter(self):
        """Hook called when mode gets activated."""
        pass

    def on_exit(self):
        """Hook called when mode gets deactivated."""
        pass

    def tick(self):
        """Hook called periodically while mode is active."""
        pass


class CalmIdleMode(BaseIdleMode):
    """Placeholder for calm idle behavior."""

    name = "calm"
    interval_sec = 4.0

    def tick(self):
        # Intentionally empty skeleton.
        pass


class CuriousIdleMode(BaseIdleMode):
    """Placeholder for curious idle behavior."""

    name = "curious"
    interval_sec = 2.5

    def tick(self):
        # Intentionally empty skeleton.
        pass


class SleepyIdleMode(BaseIdleMode):
    """Placeholder for sleepy idle behavior."""

    name = "sleepy"
    interval_sec = 5.0

    def tick(self):
        # Intentionally empty skeleton.
        pass


class IdleModeManager:
    """Coordinates activation and periodic execution of idle modes."""

    def __init__(self, actions):
        self._modes = {
            CalmIdleMode.name: CalmIdleMode(actions),
            CuriousIdleMode.name: CuriousIdleMode(actions),
            SleepyIdleMode.name: SleepyIdleMode(actions),
        }
        self.active_mode = None
        self._last_tick_ts = 0.0

    @property
    def active_name(self):
        if self.active_mode is None:
            return "off"
        return self.active_mode.name

    def enable(self, mode_name):
        mode = self._modes.get(mode_name)

        if mode is None:
            logger.warning("Unknown idle mode requested: %s", mode_name)
            return False

        if self.active_mode is mode:
            return True

        self.disable()
        self.active_mode = mode
        self._last_tick_ts = 0.0

        try:
            self.active_mode.on_enter()
        except Exception:
            logger.exception("Idle mode on_enter failed: %s", mode_name)

        logger.info("Idle mode enabled: %s", mode_name)
        return True

    def disable(self):
        if self.active_mode is None:
            return

        previous_name = self.active_mode.name

        try:
            self.active_mode.on_exit()
        except Exception:
            logger.exception("Idle mode on_exit failed: %s", previous_name)

        self.active_mode = None
        self._last_tick_ts = 0.0
        logger.info("Idle mode disabled: %s", previous_name)

    def tick(self, now_ts):
        if self.active_mode is None:
            return

        if self._last_tick_ts == 0.0:
            self._last_tick_ts = now_ts
            return

        if now_ts - self._last_tick_ts < self.active_mode.interval_sec:
            return

        self._last_tick_ts = now_ts

        try:
            self.active_mode.tick()
        except Exception:
            logger.exception("Idle mode tick failed: %s", self.active_mode.name)
