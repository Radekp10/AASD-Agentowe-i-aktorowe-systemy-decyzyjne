import json

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

from src import Messages

STATE_ONE = "GET_FLIGHT_PARAMETERS_STATE"
STATE_TWO = "SET_FLIGHT_TRAJECTORY_STATE"
STATE_THREE = "MAKE_FLIGHT_STATE"


class Drone(Agent):
    class DroneBehaviour(FSMBehaviour):
        async def on_start(self):
            print("[DRONE]: Starting behaviour . . .")
            self.controlStationId = 'AASD_CONTROL_STATION@01337.io'
            drone_existance = Message(to='AASD_CONTROL_STATION@01337.io')
            drone_existance.set_metadata("performative", "inform")
            drone_existance.body = Messages.d_on_station(self.agent)

        async def on_end(self):
            print("[DRONE]: Behaviour finished with exit code {}.".format(self.exit_code))

    class StateOne(State):
        async def run(self):
            print("[DRONE]: I'm at state 1 (initial state)")
            flight_parameters = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if flight_parameters:
                message = json.load(flight_parameters.body)
                self.plannedControlStationId = message['endStationId']
                print("[DRONE]: Message received with content: {}".format(flight_parameters.body))
            else:
                print("[DRONE]: Did not received any message after 10 seconds")
            self.set_next_state(STATE_TWO)

    class StateTwo(State):
        async def run(self):
            print("[DRONE]: I'm at state 2")
            print("[DRONE]: Setting flight trajectory...")
            self.set_next_state(STATE_THREE)

    class StateThree(State):
        async def run(self):
            self.controlStationId = self.plannedControlStationId
            print("[DRONE]: I'm at state 3")
            print("[DRONE]: Flying...")

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.droneBehaviour = self.DroneBehaviour()

    async def setup(self):
        print("[DRONE]: Agent starting . I'm agent {}".format(str(self.jid)))
        self.droneBehaviour.add_state(name=STATE_ONE, state=self.StateOne(), initial=True)
        self.droneBehaviour.add_state(name=STATE_TWO, state=self.StateTwo())
        self.droneBehaviour.add_state(name=STATE_THREE, state=self.StateThree())
        self.droneBehaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        self.droneBehaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.add_behaviour(self.droneBehaviour)
