# 🤖 EV3 Color Sorter — Robotic Arm with Inverse Kinematics

A LEGO EV3 robotic arm that automatically detects colored balls using a color sensor and sorts them to designated stations using inverse kinematics and a conveyor system.

Built as a university group project using LEGO Mindstorms EV3 and MicroPython.

---

## 📸 Demo

![Robot](media/Robo IMG 1.jpg)
![Robot](media/Robo IMG 2.jpg)

---

## ⚙️ How It Works

1. A ball is placed on the **conveyor belt**
2. The **color sensor** detects its color
3. The conveyor moves the ball to the correct station:
   - 🔵 **Blue** → Conveyor → Station 5 → Arm picks and drops at Station 1
   - 🔴 **Red** → Conveyor → Station 5 → Arm picks and drops at Station 2
   - ⚫ **Black** → Conveyor → Station 3
   - 🟢 **Green** → Conveyor → Station 4
4. The robotic arm uses **inverse kinematics** to calculate joint angles and move precisely

---

## 🧠 Kinematics

The arm solves for two joint angles given a target (x, y, z) coordinate:

- **θ1 (Base rotation)** — calculated using `atan2(y, x)`
- **θ2 (Elbow angle)** — geometric solution using the arm's link lengths and vertical offset

Link lengths (in mm):
| Link | Length |
|------|--------|
| l0   | 35     |
| l1   | 50     |
| l2   | 95     |
| l3   | 185    |
| l4   | 110    |

---

## 🔧 Hardware

- LEGO Mindstorms EV3 Brick
- 4x EV3 Motors (Ports A, B, C, D)
- 1x Color Sensor
- 2x Touch Sensors (for homing)
- Conveyor belt mechanism
- Custom gripper

---

## 📦 Requirements

- [LEGO EV3 MicroPython v2.0+](https://pybricks.com/)
- VS Code with the EV3 MicroPython extension

---

## 🚀 Running the Project

1. Flash the EV3 brick with the MicroPython image
2. Open the project in VS Code with the EV3 extension
3. Download and run `main.py` on the brick
4. The robot will home itself using touch sensors, then start sorting

---

## 👥 Team

Built as a group university project. Code, mechanical design, and calibration done collaboratively.

---

## 📌 Notes

- Gripper fingers must be **manually opened** before starting the program
- `base_error` can be adjusted to fine-tune the homing position
- Station coordinates are measured values and may need recalibration for different builds
