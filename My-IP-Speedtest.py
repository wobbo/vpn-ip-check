#!/usr/bin/env python3

# Ernst Lanser
# 2026-03-30

# sudo apt install python3
# wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-aarch64.tgz
# tar -xzf ookla-speedtest-1.2.0-linux-aarch64.tgz 
# sudo mv speedtest /usr/local/bin/
# speedtest --accept-license --accept-gdpr
# python3 ./My-IP-Speedtest.py

import gi
import requests
import subprocess
import json
import threading
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


API_URL = "http://ip-api.com/json/"
COOLDOWN_SECONDS = 30


class MyIPWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="My IP Speedtest")

        self.set_border_width(20)
        self.set_default_size(360, 260)
        self.set_resizable(False)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add(box)

        self.label = Gtk.Label()
        self.label.set_xalign(0)
        self.label.set_selectable(True)
        self.label.set_can_focus(False)

        self.button = Gtk.Button(label="Update")
        self.button.connect("clicked", self.on_refresh_clicked)

        box.pack_start(self.label, True, True, 0)
        box.pack_start(self.button, False, False, 0)

        self.last_test_time = 0

        self.update_all()


    def update_label(self, speedtest_text):

        text = (
            f"<b>Public IP:</b>\n{self.ip}\n\n"
            f"<b>Provider:</b>\n{self.isp}\n\n"
            f"<b>Country:</b>\n{self.country}\n\n"
            f"<b>Speedtest:</b>\n{speedtest_text}"
        )

        self.label.set_markup(text)


    def cooldown_loop(self):

        while True:

            remaining = int(
                COOLDOWN_SECONDS - (time.time() - self.last_test_time)
            )

            if remaining <= 0:

                GLib.idle_add(self.button.set_label, "Update")
                GLib.idle_add(self.button.set_sensitive, True)

                break


            GLib.idle_add(
                self.button.set_label,
                f"Update {remaining}s"
            )

            time.sleep(1)


    def update_all(self):

        now = time.time()

        if now - self.last_test_time < COOLDOWN_SECONDS:

            self.button.set_sensitive(False)

            threading.Thread(
                target=self.cooldown_loop,
                daemon=True
            ).start()

            return


        self.last_test_time = now
        self.button.set_sensitive(False)

        threading.Thread(
            target=self.fetch_ip_info
        ).start()


    def fetch_ip_info(self):

        try:

            response = requests.get(API_URL, timeout=5)
            data = response.json()

            self.ip = data.get("query", "unknown")
            self.country = data.get("country", "unknown")
            self.isp = data.get("isp", "unknown")

        except Exception:

            self.ip = "unknown"
            self.country = "unknown"
            self.isp = "unknown"


        GLib.idle_add(
            self.update_label,
            "\n"
        )

        threading.Thread(
            target=self.run_speedtest
        ).start()


    def run_speedtest(self):

        self.phase = "\n"
        self.finished = False


        def timer_loop():

            dots = ["", ".", "..", "..."]
            i = 0

            while not self.finished:

                animated = self.phase.replace(
                    "...",
                    dots[i]
                )

                GLib.idle_add(
                    self.update_label,
                    f"{animated}\n"
                )

                i = (i + 1) % 4

                time.sleep(1)


        threading.Thread(
            target=timer_loop,
            daemon=True
        ).start()


        try:

            process = subprocess.Popen(
                [
                    "speedtest",
                    "--accept-license",
                    "--accept-gdpr",
                    "--format=jsonl"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )


            for line in process.stdout:

                data = json.loads(line)
                event = data.get("type")


                if event == "testStart":

                    self.phase = "Selecting server..."

                elif event == "ping":

                    self.phase = "Testing ping...\n"

                elif event == "download":

                    self.phase = "Testing download...\n"

                elif event == "upload":

                    self.phase = "Testing upload...\n"


                elif event == "result":

                    ping = f"{round(data['ping']['latency'])} ms"
                    download = f"{round(data['download']['bandwidth'] * 8 / 1_000_000)} Mbps"
                    upload = f"{round(data['upload']['bandwidth'] * 8 / 1_000_000)} Mbps"


                    final = (
                        f"Ping: {ping}\n"
                        f"Download: {download}\n"
                        f"Upload: {upload}"
                    )

                    GLib.idle_add(
                        self.update_label,
                        final
                    )

                    break


        except Exception:

            GLib.idle_add(
                self.update_label,
                "Speedtest failed\n\n"
            )


        self.finished = True

        GLib.idle_add(
            self.button.set_sensitive,
            True
        )


    def on_refresh_clicked(self, widget):

        self.update_all()


def main():

    win = MyIPWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
