# Physical Hardware Setup Guide

## Hardware Specifications Required

Before enabling physical motion, operators must supply exact hardware details to complete the vendor adapter:

| Parameter | Description | Status |
|---|---|---|
| **Robot Manufacturer** | e.g. Franka Emika, Universal Robots, Kinova | `TODO: CONFIGURATION REQUIRED` |
| **Robot Model** | e.g. FR3, UR5e, Gen3, Custom | `TODO: CONFIGURATION REQUIRED` |
| **Robot Controller** | Controller firmware / hardware revision | `TODO: CONFIGURATION REQUIRED` |
| **Number of Joints** | 6-DoF or 7-DoF | `TODO: CONFIGURATION REQUIRED` |
| **End Effector / Gripper** | Robotiq 2F-85, OnRobot, pneumatic | `TODO: CONFIGURATION REQUIRED` |
| **Master / Leader Model** | GELLO, Aloha Master, Haply, 3Dconnexion | `TODO: CONFIGURATION REQUIRED` |
| **Camera Models** | Intel RealSense D435i/D405, USB UVC, Basler | `TODO: CONFIGURATION REQUIRED` |
| **Workstation OS & Kernel** | Ubuntu 22.04 LTS with PREEMPT_RT kernel | Recommended for real-time safety |
| **Physical E-Stop Circuit** | Dual-channel Category 3/4 hardware loop | MANDATORY prior to power-on |

## Network Setup
- Connect the robot controller to a dedicated network interface card (NIC) isolated from public office Wi-Fi/Internet to prevent jitter and unsolicited broadcast storms.
- Configure static IP (e.g. `192.168.1.100` / subnet `255.255.255.0`).
- Ensure firewall permits bidirectional UDP/TCP packets on the vendor designated real-time ports.
