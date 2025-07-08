import flet as ft
import asyncio
import threading
import requests, time

URL        = "YOUR Phyphox Server"  
BUFFER     = "illum"                   
INTERVAL   = 0.3
THRESH_LUX = 200
WINDOW     = 2.0                  
TIMEOUT    = 10.0          

def latest_lux():
    """Return the newest illuminance value or None if buffer is empty."""
    res   = requests.get(f"{URL}/get?{BUFFER}", timeout=1).json()
    buf   = res["buffer"][BUFFER]["buffer"]
    if not buf:                   
        return None
    return buf[0]                

MOTIVATIONAL_LINES = [
    "Let's go! Keep pushing!",
    "You're crushing it!",
    "Feel the burn!",
    "Push through the pain!",
    "Unleash the beast!",
    "No pain, no gain!",
    "Repocalypse is here!",
]
ROASTS = [
    "Did you even try? 🥱",
    "My grandma does more!",
    "Was that a warmup?",
    "You call that a workout?",
    "The robot is disappointed... 🤖",
]

class PushupCounterApp(ft.Column):
    def __init__(self):
        super().__init__(alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.count = 0
        self.prev_v = None
        self.prev_t = time.time()
        self.last_significant_change_time = time.time()
        self.running = True
        self.motivation_idx = 0
        self.finalized = False
        self.img = ft.Image(src="image.png", width=250, height=250, fit=ft.ImageFit.CONTAIN)
        self.count_text = ft.Text(f"Pushups: {self.count}", size=40, weight=ft.FontWeight.BOLD)
        self.motivation = ft.Text(MOTIVATIONAL_LINES[0], size=24, italic=True)
        self.final_text = ft.Text("", size=32, weight=ft.FontWeight.W_700, color=ft.Colors.RED_400)
        self.controls = [
            self.img,
            self.count_text,
            self.motivation,
            self.final_text
        ]

    async def poll_lux(self):
        global URL, BUFFER, THRESH_LUX, WINDOW, INTERVAL, TIMEOUT
        while self.running:
            try:
                v = await asyncio.to_thread(latest_lux)
                t = time.time()
                if v is not None:
                    if self.prev_v is not None and abs(v - self.prev_v) > THRESH_LUX and (t - self.prev_t) < WINDOW:
                        self.count += 1/2
                        self.last_significant_change_time = t
                        self.count_text.value = f"Pushups: {self.count}"
                        self.motivation_idx = (self.motivation_idx + 1) % len(MOTIVATIONAL_LINES)
                        self.motivation.value = MOTIVATIONAL_LINES[self.motivation_idx]
                        self.update()
                    self.prev_v, self.prev_t = v, t
                # Timeout check
                if t - self.last_significant_change_time > TIMEOUT and not self.finalized:
                    self.running = False
                    self.finalized = True
                    await self.show_final()
                    break
            except Exception as e:
                self.motivation.value = f"⚡ error: {e}"
                self.update()
            await asyncio.sleep(INTERVAL)

    async def show_final(self):
        if self.count < 5:
            import random
            roast = random.choice(ROASTS)
            self.final_text.value = f"🛑 {roast} (Final count: {self.count})"
        else:
            self.final_text.value = f"Great job! Final count: {self.count} 💪"
        self.update()


def main(page: ft.Page):
    page.title = "Repocalypse Pushup Counter"
    page.bgcolor = ft.Colors.BLACK
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False
    app = PushupCounterApp()
    page.add(app)
    page.run_task(app.poll_lux)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="images")
