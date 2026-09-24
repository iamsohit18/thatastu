"""Robotics platform standard exceptions hierarchy."""


class RoboTeleopError(Exception):
    """Base exception for all RoboTeleop errors."""
    pass


class HardwareConnectionError(RoboTeleopError):
    """Raised when hardware communication fails or times out."""
    pass


class SafetyViolationError(RoboTeleopError):
    """Raised when safety limits (workspace, velocity, collision) are breached."""
    pass


class EmergencyStopActiveError(RoboTeleopError):
    """Raised when an operation is attempted while E-Stop is active."""
    pass


class SynchronizationError(RoboTeleopError):
    """Raised when sensor timestamp clock drift or gap threshold is exceeded."""
    pass


class ConfigurationError(RoboTeleopError):
    """Raised when missing hardware specs or invalid parameters are provided."""
    pass


class EpisodeRecordingError(RoboTeleopError):
    """Raised during episode capture or storage failure."""
    pass
