import threading
import pydirectinput

from PySide6.QtCore import QThread, Signal

class MacroWorker(QThread):
    status_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.stop_event = threading.Event()

        self.state = "buy"
        self.cycle = 0
        self.status = "idle"

        self.idlePos = (966, 230)
        self.chestPos = (965, 610)
        self.buyPos = (848, 544)

        pydirectinput.PAUSE = 0.05

    def stop(self):
        self.setStatus("Stopped")
        self.releaseKeys()
        self.stop_event.set()

    def is_running(self):
        return not self.stop_event.is_set()

    def delay(self, duration):
        """Sleep, but allow the macro to be stopped early."""
        return not self.stop_event.wait(duration)

    def holdKey(self, key, duration):
        pydirectinput.keyDown(key)

        try:
            self.delay(duration)
        finally:
            pydirectinput.keyUp(key)

    def openDoor(self):
        if not self.is_running():
            return
        
        pydirectinput.press("e")
        self.delay(7.8)

    def kill(self):
        pydirectinput.press("2")

        status_before = self.status
        self.setStatus("Killing monsters")

        for i in range(15):
            if not self.is_running():
                break

            pydirectinput.leftClick()
            self.delay(0.4)

        pydirectinput.press("1")

        self.setStatus(status_before)

    def goBack(self, key):
        self.holdKey("s", 1)

        if not self.is_running():
            return

        pydirectinput.keyDown(key)

        try:
            pydirectinput.press("q")
            self.delay(3.6)

            if not self.is_running():
                return

            pydirectinput.press("q")
            self.delay(3.6)
        finally:
            pydirectinput.keyUp(key)

        self.holdKey("w", 0.75)

    def reset(self):
        self.setStatus("Resetting")

        pydirectinput.press("esc")
        self.delay(0.1)
        pydirectinput.press("r")
        self.delay(0.1)
        pydirectinput.press("enter")

        self.setStatus("Idle")

    def rotate(self, direction):
        if not self.is_running():
            return  

        rottime = 0.725
        
        self.holdKey(direction, rottime)

    # main run loop function
    def run(self):
        while self.is_running():
            if not self.delay(1):
                break

            if self.state == "idle":
                if self.cycle >= 2:
                    self.cycle = 0
                    self.state = "buy"
                else:
                    self.state = "first"

                continue

            elif self.state == "first":
                self.setStatus("Trick or treating (left side)")

                pydirectinput.moveTo(self.idlePos[0], self.idlePos[1])
                pydirectinput.moveRel(1, 0)

                self.kill()

                self.holdKey("a", 5.1)
                self.holdKey("w", 0.8)

                pydirectinput.press("g")

                self.openDoor()
                for i in range(3):
                    self.holdKey("a", 2.35)
                    self.openDoor()

                self.kill()

                pydirectinput.keyDown("a")
                pydirectinput.keyDown("s")
                self.delay(1.3)
                pydirectinput.keyUp("a")
                pydirectinput.keyUp("s")

                self.rotate("left")
                self.openDoor()

                for i in range(3):
                    self.holdKey("a", 2.35)
                    self.openDoor()

                # done first quarter
                self.kill()
                pydirectinput.press("g")
                self.goBack("a")
                self.kill()

                self.openDoor()
                for i in range(3):
                    self.holdKey("a", 2.35)
                    self.openDoor()

                self.kill()

                pydirectinput.keyDown("a")
                pydirectinput.keyDown("s")
                self.delay(1.3)
                pydirectinput.keyUp("a")
                pydirectinput.keyUp("s")

                self.rotate("left")
                self.openDoor()

                for i in range(3):
                    self.holdKey("a", 2.35)
                    self.openDoor()

                self.kill()
                self.holdKey("a", 4)

                for i in range(20):
                    if not self.is_running():
                        break

                    pydirectinput.press("space")
                    self.delay(0.05)

                if not self.is_running():
                    break

                pydirectinput.keyDown("w")

                try:
                    for i in range(30):
                        if not self.is_running():
                            break

                        pydirectinput.press("space")
                        self.delay(0.05)
                finally:
                    pydirectinput.keyUp("w")

                if not self.is_running():
                    break

                self.delay(3)
                self.reset()

                if not self.delay(30):
                    break

                self.state = "second"

                continue

            elif self.state == "second":
                self.setStatus("Trick or treating (right side)")

                self.kill()

                self.holdKey("d", 5.1)
                self.holdKey("w", 0.75)

                pydirectinput.press("g")

                self.openDoor()

                for i in range(3):
                    self.holdKey("d", 2.35)
                    self.openDoor()

                self.kill()

                pydirectinput.keyDown("d")
                pydirectinput.keyDown("s")
                self.delay(1.3)
                pydirectinput.keyUp("d")
                pydirectinput.keyUp("s")

                self.rotate("right")
                self.openDoor()

                for i in range(3):
                    self.holdKey("d", 2.35)
                    self.openDoor()

                # done first quarter
                self.kill()
                pydirectinput.press("g")
                self.goBack("d")
                self.kill()

                self.openDoor()

                for i in range(3):
                    self.holdKey("d", 2.35)
                    self.openDoor()

                self.kill()

                pydirectinput.keyDown("d")
                pydirectinput.keyDown("s")
                self.delay(1.4)
                pydirectinput.keyUp("d")
                pydirectinput.keyUp("s")

                self.rotate("right")
                self.openDoor()

                for i in range(3):
                    self.holdKey("d", 2.35)
                    self.openDoor()
                self.kill()
                self.holdKey("d", 4)

                for i in range(20):
                    if not self.is_running():
                        break

                    pydirectinput.press("space")
                    self.delay(0.05)

                if not self.is_running():
                    break

                pydirectinput.keyDown("w")

                try:
                    for i in range(30):
                        if not self.is_running():
                            break

                        pydirectinput.press("space")
                        self.delay(0.05)
                finally:
                    pydirectinput.keyUp("w")

                if not self.is_running():
                    break

                self.delay(2)
                self.reset()

                if not self.delay(30):
                    break

                self.state = "idle"
                self.cycle += 1

                continue

            elif self.state == "buy":
                self.setStatus("Buying")

                pydirectinput.press("g")

                self.rotate("left")
                self.delay(0.1)
                self.rotate("left")

                pydirectinput.keyDown("w")

                try:
                    for i in range(14):
                        if not self.is_running():
                            break

                        pydirectinput.press("space")
                        self.delay(0.05)
                finally:
                    pydirectinput.keyUp("w")

                if not self.is_running():
                    break

                self.holdKey("s", 0.5)

                self.delay(3)

                pydirectinput.moveTo(
                    self.chestPos[0],
                    self.chestPos[1]
                )
                pydirectinput.moveRel(1, 0)

                self.delay(0.2)
                pydirectinput.leftClick()

                self.delay(0.5)

                pydirectinput.moveTo(
                    self.buyPos[0],
                    self.buyPos[1]
                )
                pydirectinput.moveRel(1, 0)

                self.delay(0.2)
                pydirectinput.leftClick()

                self.delay(2)

                pydirectinput.keyDown("w")

                try:
                    for i in range(40):
                        if not self.is_running():
                            break

                        pydirectinput.press("space")
                        self.delay(0.05)
                finally:
                    pydirectinput.keyUp("w")

                if not self.is_running():
                    break

                self.reset()

                if not self.delay(30):
                    break

                self.state = "idle"
                self.cycle = 0

                continue

    # cleanup
    def releaseKeys(self):
        keys = [
            "w", "a", "s", "d",
            "space", "left", "right",
            "up", "down"
        ]

        for key in keys:
            pydirectinput.keyUp(key)

    def setStatus(self, status=str):
        self.status = status
        self.status_changed.emit(status)