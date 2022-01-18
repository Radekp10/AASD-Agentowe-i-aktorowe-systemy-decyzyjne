from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import src.Messages as Messages

STATE_ONE = "GET_REQUEST_ABOUT_AVAILABLE_DRONES_STATE"
STATE_TWO = "SEND_RESPONSE_ABOUT_AVAILABLE_DRONES_STATE"
STATE_THREE = "GET_START_RESERVATION_REQUEST_STATE"
STATE_FOUR = "GET_END_RESERVATION_REQUEST_STATE"


class ControlStation(Agent):
    class ControlStationBehaviour(FSMBehaviour):
        async def on_start(self):
            print("[CONTROL_STATION]: Starting behaviour. . .")

        async def on_end(self):
            print("[CONTROL_STATION]: Behaviour finished with exit code {}.".format(self.exit_code))

    class StateOne(State):
        async def run(self):
            print("[CONTROL_STATION]: I'm at state 1 (initial state)")
            are_drones_available_request = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if are_drones_available_request:
                print("[CONTROL_STATION]: Message received with content: {}".format(are_drones_available_request.body))
            else:
                print("[CONTROL_STATION]: Did not received any message after 10 seconds")
            self.set_next_state(STATE_TWO)

    class StateTwo(State):
        async def run(self):
            print("[CONTROL_STATION]: I'm at state 2")
            are_drones_available_response = Message(to='AASD_REQUEST_HANDLER@01337.io')
            are_drones_available_response.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            are_drones_available_response.body = Messages.cs_drones_available_req_message(self.agent)
            await self.send(are_drones_available_response)
            print("[CONTROL_STATION]: Drones available sent")
            self.set_next_state(STATE_THREE)

    class StateThree(State):
        async def run(self):
            print("[CONTROL_STATION]: I'm at state 3")
            start_reservation_request = await self.receive(timeout=20)  # wait for a message for 10 seconds
            if start_reservation_request:
                print("[CONTROL_STATION]: Message received with content: {}".format(start_reservation_request.body))
            else:
                print("[CONTROL_STATION]: Did not received any message after 10 seconds")
            print("[CONTROL_STATION]: Start reservation made")

    class StateFour(State):
        async def run(self):
            print("[CONTROL_STATION]: I'm at state 4")
            end_reservation_request = await self.receive(timeout=20)  # wait for a message for 10 seconds
            if end_reservation_request:
                print("[CONTROL_STATION]: Message received with content: {}".format(end_reservation_request.body))
            else:
                print("[CONTROL_STATION]: Did not received any message after 10 seconds")
            print("[CONTROL_STATION]: End reservation made")

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.controlStationBehaviour = self.ControlStationBehaviour()
        self.customerId = '';

    async def setup(self):
        print("[CONTROL_STATION]: Agent starting . I'm agent {}".format(str(self.jid)))
        self.controlStationBehaviour.add_state(name=STATE_ONE, state=self.StateOne(), initial=True)
        self.controlStationBehaviour.add_state(name=STATE_TWO, state=self.StateTwo())
        self.controlStationBehaviour.add_state(name=STATE_THREE, state=self.StateThree())
        self.controlStationBehaviour.add_state(name=STATE_FOUR, state=self.StateFour())
        self.controlStationBehaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        self.controlStationBehaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.controlStationBehaviour.add_transition(source=STATE_THREE, dest=STATE_FOUR)
        self.add_behaviour(self.controlStationBehaviour)
