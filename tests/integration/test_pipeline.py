"""Integration test for full simulator teleoperation pipeline."""
from src.hardware.robot.simulator import SimulatorRobotAdapter
from src.hardware.leader.simulator import SimulatorLeaderAdapter
from src.safety.safety_manager import SafetyManager
from src.teleoperation.teleop_controller import TeleopController

def test_teleoperation_simulation_pipeline():
    config = {
        "leader": {"scaling": {"position_ratio": 0.8, "orientation_ratio": 0.8}},
        "safety": {
            "watchdog": {"command_timeout_ms": 200},
            "velocity_enforcement": {"max_cartesian_linear_m_s": 0.3},
            "workspace_limits": {"bounding_box": {"x": [-0.65, 0.65], "y": [0.25, 0.8], "z": [0.03, 0.7]}},
        },
    }

    robot = SimulatorRobotAdapter(dof=6)
    leader = SimulatorLeaderAdapter()
    safety = SafetyManager(config)
    controller = TeleopController(robot, leader, safety, config)

    assert robot.connect() is True
    assert leader.connect() is True
    assert controller.engage() is True

    # Run 5 steps
    for _ in range(5):
        action = controller.step()
        assert action is not None
        assert action.target_tcp_pose is not None

    controller.disengage()
    robot.disconnect()
    leader.disconnect()
