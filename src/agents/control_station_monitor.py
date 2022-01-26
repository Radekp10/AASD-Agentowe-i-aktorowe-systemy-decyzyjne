from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message


class ControlStationMonitor(Agent):
    class GetControlStationStatus(CyclicBehaviour):
        async def run(self):
            print("[CONTROL_STATION_MONITOR]: Waiting for drone status")
            control_station_status = await self.receive(timeout=15)  # wait for a message for 15 seconds
            if control_station_status:
                print("[CONTROL_STATION_MONITOR]: Message received with content: {}".format(control_station_status.body))
            else:
                print("[CONTROL_STATION_MONITOR]: Did not received status message after 15 seconds")

        async def on_end(self):
            await self.agent.stop()

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)

    async def setup(self):
        print("[CONTROL_STATION_MONITOR]: Agent starting . I'm agent {}".format(str(self.jid)))
        b = self.GetControlStationStatus()
        self.add_behaviour(b)
