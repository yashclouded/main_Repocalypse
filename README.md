# 🏋️‍♂️ Repocalypse Push‑up Counter
*A spiffy (stylish) little desktop/web app that counts your push‑ups in real time by sipping data from a Phyphox live server.*


---

## ⚙️ How it works
1. **Phyphox** streams illuminance (lux) values from your phone’s light sensor.  
2. The app polls that `/get?illum` buffer every `300 ms`.  
3. A swing (∆lux > 200) within a 2 s window is taken as **½ rep** – down + up ⇒ one full push‑up.  
4. If no rep‑worthy changes arrive for 10 s, the session “times out” and you get either a rousing “Great job!” or a savage roast 😂.

> **Why lux?**  
> Your torso typically shades then reveals the phone’s flashlight/room light each time you move—cheap, cheerful, and surprisingly robust.

---

## ✨ Features
| Feature | TL;DR |
|---------|-------|
| Real‑time counter | Smooth UI built with **Flet** (Flutter‑powered Python UI). |
| Motivation/roasts | Random hype lines or cheeky burns depending on performance. |
| Auto‑stop timer | Ends gracefully after inactivity, so you don’t have to Ctrl‑C. |
| Easy tweaking | All magic numbers at the top of `app.py`. |

---

## 🛠️ Prerequisites
* **Python ≥ 3.10**  
* A phone (or any device) running the **Phyphox** app with the *Illuminance* experiment shared over Wi‑Fi.
* A Laser Which Points on the LiDAR sensor of phone.

