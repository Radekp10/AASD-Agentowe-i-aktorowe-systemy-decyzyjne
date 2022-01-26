import json

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

from src import Messages

STATE_ONE = "GET_FLIGHT_PARAMETERS_STATE"
STATE_TWO = "SET_FLIGHT_TRAJECTORY_STATE"
STATE_THREE = "MAKE_FLIGHT_STATE"

DRONE_ID = ""


class Drone(Agent):
    class DroneBehaviour(FSMBehaviour):
        async def on_start(self):
            print(f"[{DRONE_ID}]: Starting behaviour . . .")
            self.controlStationId = 'AASD_CONTROL_STATION@01337.io'
            drone_existance = Message(to='AASD_CONTROL_STATION@01337.io')
            drone_existance.set_metadata("performative", "inform")
            drone_existance.body = Messages.d_on_station(self.agent)
            await self.send(drone_existance)

        async def on_end(self):
            print(f"[{DRONE_ID}]: Behaviour finished with exit code {self.exit_code}.")

    class StateOne(State):
        async def run(self):
            print(f"[{DRONE_ID}]: I'm at state 1 (initial state)")
            flight_parameters = await self.receive(timeout=30)  # wait for a message for 10 seconds
            if flight_parameters and json.loads(flight_parameters.body)['title'] == Messages.RH_FLIGHT_PARAMETERS:
                print(f"[{DRONE_ID}]: Message received with content: {flight_parameters.body}")
                self.set_next_state(STATE_TWO)
            else:
                print(f"[{DRONE_ID}]: Did not received any message after 10 seconds")
                self.set_next_state(STATE_ONE)

    class StateTwo(State):
        async def run(self):
            print(f"[{DRONE_ID}]: I'm at state 2")
            print(f"[{DRONE_ID}]: Setting flight trajectory...")
            self.set_next_state(STATE_THREE)

    class StateThree(State):
        async def run(self):
            print(f"[{DRONE_ID}]: I'm at state 3")
            print(f"[{DRONE_ID}]: Flying...")
            self.set_next_state(STATE_ONE)

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.droneBehaviour = self.DroneBehaviour()

    async def setup(self):
        global DRONE_ID
        DRONE_ID = self.jid.localpart
        print(f"[{DRONE_ID}]: Agent starting . I'm agent {str(self.jid)}")
        self.droneBehaviour.add_state(name=STATE_ONE, state=self.StateOne(), initial=True)
        self.droneBehaviour.add_state(name=STATE_TWO, state=self.StateTwo())
        self.droneBehaviour.add_state(name=STATE_THREE, state=self.StateThree())
        self.droneBehaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        self.droneBehaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.droneBehaviour.add_transition(source=STATE_THREE, dest=STATE_ONE)
        self.droneBehaviour.add_transition(source=STATE_ONE, dest=STATE_ONE)
        self.add_behaviour(self.droneBehaviour)
