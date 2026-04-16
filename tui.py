#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static
from textual.reactive import reactive
import asyncio
import random

class InputLog(Static):
    logs = reactive("")

    def add_log(self, message: str):
        self.logs += f"{message}\n"
        self.update(self.logs)


class VulnScannerApp(App):

    CSS = """
    Screen {
        layout:vertical;
    }
    #log {
        height: 1fr;
        border: solid green;
        padding: 1;
    }

    #input {
        border: solid cyan;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield InputLog(id="log")
        yield Input(placeholder="Enter command...", id="input")
        yield Footer()

    async def on_mount(self):
        self.InputLog = self.query_one("#log", InputLog)
        self.input_box = self.query_one("#input", Input)

    async def on_input_submitted(self, event: Input.Submitted):
        command = event.value.strip()
        self.input_box.value = ""
        await self.handle_command(command)

    async def handle_command(self, command: str):
        self.InputLog.add_log(f"> {command}")

        if command.startswith("scan"):
            target = command.replace("scan", "").strip()

            if not target:
                self.InputLog.add_log("[-] No target specified")
                return

            self.InputLog.add_log(f"Beginning Scan on {target}")
            self.run_worker(self.scan_target(target))

        elif command == "help":
            self.InputLog.add_log("Commands:")
            self.InputLog.add_log(" scan <target>")
            self.InputLog.add_log(" help")
            self.InputLog.add_log(" exit")

        elif command == "exit":
            await self.action_quit()

        else:
            self.InputLog.add_log("[?] Unknown Command")

    async def scan_target(self, target):
        for _ in range(5):
            await asyncio.sleep(2)

            vuln_found = random.choice([True, False])

            if vuln_found:
                self.InputLog.add_log(
                    f"Vulnerability Found on {target} (port {random.randint(20,9000)})"
                )
            else:
                self.InputLog.add_log(
                    f"Checked port on {target} (port {random.randint(20,9000)})"
                )

        self.InputLog.add_log(f"[✓] Scan Complete: {target}")


if __name__ == "__main__":
    app = VulnScannerApp()
    app.run()