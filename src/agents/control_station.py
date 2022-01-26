import json

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import src.Messages as Messages

STATE_ZERO = "GET_AVAILABILITY_FROM_DRONES_OR_MAKE_END_RESERVATION"
STATE_ONE = "GET_REQUEST_ABOUT_AVAILABLE_DRONES_STATE"
STATE_TWO = "SEND_RESPONSE_ABOUT_AVAILABLE_DRONES_STATE"
STATE_THREE = "GET_START_RESERVATION_REQUEST_STATE"
STATE_FOUR = "GET_END_RESERVATION_REQUEST_STATE"
# STATE_FIVE = "WAITING"

AVAILABLE_DRONES = []


class ControlStation(Agent):
    class ControlStationBehaviour(FSMBehaviour):
        async def on_start(self):
            print(f"[{self.agent.jid.localpart}]: Starting behaviour. . .")

        async def on_end(self):
            print(f"[{self.agent.jid.localpart}]: Behaviour finished with exit code {self.exit_code}.")

    class StateZero(State):
        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 0 (initial state)")
            available_drones = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if available_drones and json.loads(available_drones.body)['title'] == Messages.D_DRONE_AVAILABLE:
                message = json.loads(available_drones.body)
                print(f"[{self.agent.jid.localpart}]: Drones are available at station")
                AVAILABLE_DRONES.append(message['droneId'])
                self.set_next_state(STATE_ONE)
            elif available_drones and json.loads(available_drones.body)['title'] == Messages.RH_END_RESERVATION:
                message = json.loads(available_drones.body)
                print(f"[{self.agent.jid.localpart}]: Message received with content: {message['title']}")
                print(f"[{self.agent.jid.localpart}]: End reservation made")
                AVAILABLE_DRONES.append((message['droneId']).split('@', 1)[0].lower())
                self.set_next_state(STATE_ZERO)
            else:
                print(f"[{self.agent.jid.localpart}]: Did not received any message after 60 seconds")
                self.set_next_state(STATE_ZERO)

    class StateOne(State):
        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 1")
            are_drones_available_request = await self.receive(timeout=60)  # wait for a message for 10 seconds
            if are_drones_available_request and json.loads(are_drones_available_request.body)['title'] == Messages.RH_RQ_DRONES_AVAILABLE:
                message = json.loads(are_drones_available_request.body)
                print(f"[{self.agent.jid.localpart}]: Message received with content: {message['title']}")
                self.set_next_state(STATE_TWO)
            else:
                print(f"[{self.agent.jid.localpart}]: Did not received any message after 60 seconds")
                self.set_next_state(STATE_ONE)

    class StateTwo(State):
        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 2")
            are_drones_available_response = Message(to='AASD_REQUEST_HANDLER@01337.io')
            are_drones_available_response.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            are_drones_available_response.body = Messages.cs_drones_available_req_message(self.agent, AVAILABLE_DRONES[0])
            await self.send(are_drones_available_response)
            print(f"[{self.agent.jid.localpart}]: Drones available sent")
            self.set_next_state(STATE_THREE)

    class StateThree(State):
        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 3")
            start_reservation_request = await self.receive(timeout=100)  # wait for a message for 10 seconds
            if start_reservation_request and json.loads(start_reservation_request.body)['title'] == Messages.RH_START_RESERVATION:
                message = json.loads(start_reservation_request.body)
                droneId = (message['droneId']).split('@', 1)[0].lower()
                AVAILABLE_DRONES.remove(droneId)
                print(f"[{self.agent.jid.localpart}]: Message received with content: {message['title']}")
                print(f"[{self.agent.jid.localpart}]: Start reservation made")
            else:
                print(f"[{self.agent.jid.localpart}]: Did not received any message after 10 seconds")
            self.set_next_state(STATE_ZERO)

    # class StateFour(State):
    #     async def run(self):
    #         print(f"[{self.agent.jid.localpart}]: I'm at state 4")
    #         end_reservation_request = await self.receive(timeout=100)  # wait for a message for 10 seconds
    #         if end_reservation_request and json.loads(end_reservation_request.body)['title'] == Messages.RH_END_RESERVATION:
    #             message = json.loads(end_reservation_request.body)
    #             print(f"[{self.agent.jid.localpart}]: Message received with content: {message['title']}")
    #             print(f"[{self.agent.jid.localpart}]: End reservation made")
    #         else:
    #             print(f"[{self.agent.jid.localpart}]: Did not received any message after 40 seconds")
    #         self.set_next_state(STATE_ZERO)

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.controlStationBehaviour = self.ControlStationBehaviour()

    async def setup(self):
        print(f"[{self.jid.localpart}]: Agent starting . I'm agent {str(self.jid)}")
        self.controlStationBehaviour.add_state(name=STATE_ZERO, state=self.StateZero(), initial=True)
        self.controlStationBehaviour.add_state(name=STATE_ONE, state=self.StateOne())
        self.controlStationBehaviour.add_state(name=STATE_TWO, state=self.StateTwo())
        self.controlStationBehaviour.add_state(name=STATE_THREE, state=self.StateThree())
        # self.controlStationBehaviour.add_state(name=STATE_FOUR, state=self.StateFour())
        # self.controlStationBehaviour.add_state(name=STATE_FIVE, state=self.StateFive())
        self.controlStationBehaviour.add_transition(source=STATE_ZERO, dest=STATE_ONE)
        self.controlStationBehaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        self.controlStationBehaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        # self.controlStationBehaviour.add_transition(source=STATE_THREE, dest=STATE_FOUR)
        # self.controlStationBehaviour.add_transition(source=STATE_ZERO, dest=STATE_FOUR)
        self.controlStationBehaviour.add_transition(source=STATE_ZERO, dest=STATE_ZERO)
        self.controlStationBehaviour.add_transition(source=STATE_THREE, dest=STATE_ZERO)
        self.controlStationBehaviour.add_transition(source=STATE_ONE, dest=STATE_ONE)
        # self.controlStationBehaviour.add_transition(source=STATE_FOUR, dest=STATE_ZERO)
        self.add_behaviour(self.controlStationBehaviour)
