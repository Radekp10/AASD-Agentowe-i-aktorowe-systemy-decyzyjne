import datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message

class ControlStationStatusSender(Agent):
    class SendControlStationStatus(PeriodicBehaviour):
        async def run(self):
            control_station_status = Message(to='AASD_CONTROL_STATION_MONITOR@01337.io')
            control_station_status.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            control_station_status.body = "Control station status ok"
            await self.send(control_station_status)
            print("[CONTROL_STATION_STATUS_SENDER]: Params sent: " + control_station_status.body)
            self.test = 5

        async def on_end(self):
            print("[CONTROL_STATION_STATUS_SENDER]: Send control station status finished with exit code {}.".format(self.exit_code))
            await self.agent.stop()

        async def on_start(self):
            print("[CONTROL_STATION_STATUS_SENDER]: Starting send control station status . . .")

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.test = 10

    async def setup(self):
        print("[CONTROL_STATION_STATUS_SENDER]: Agent starting . I'm agent {}".format(str(self.jid)))
        start_at = datetime.datetime.now()
        b = self.SendControlStationStatus(period=self.test, start_at=start_at)
        self.add_behaviour(b)
