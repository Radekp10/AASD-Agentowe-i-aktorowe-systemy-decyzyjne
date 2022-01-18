import datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message

class DronesStatusSender(Agent):
    class SendDroneStatus(PeriodicBehaviour):
        async def run(self):
            drone_status = Message(to='AASD_DRONES_MONITOR@01337.io')
            drone_status.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            drone_status.body = "Drone status ok"
            await self.send(drone_status)
            print("[DRONES_STATUS_SENDER]: Params sent: " + drone_status.body)

        async def on_end(self):
            print("[DRONES_STATUS_SENDER]: Send drone status finished with exit code {}.".format(self.exit_code))
            await self.agent.stop()

        async def on_start(self):
            print("[DRONES_STATUS_SENDER]: Starting send drone status . . .")

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)

    async def setup(self):
        print("[DRONES_STATUS_SENDER]: Agent starting . I'm agent {}".format(str(self.jid)))
        start_at = datetime.datetime.now()
        b = self.SendDroneStatus(period=10, start_at=start_at)
        self.add_behaviour(b)
