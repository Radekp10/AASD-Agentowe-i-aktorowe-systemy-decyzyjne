import json

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import src.Messages as Messages

STATE_ONE = "GET_FLIGHT_PARAMETERS_STATE"
STATE_TWO = "SEND_REQUEST_ABOUT_AVAILABLE_DRONES_STATE"
STATE_THREE = "GET_RESPONSE_ABOUT_AVAILABLE_DRONES_STATE"
STATE_FOUR = "GIVE_FLIGHT_PROPOSITION_STATE"
STATE_FIVE = "GET_DECISION_STATE"
STATE_SIX = "SEND_START_RESERVATION_STATE"
STATE_SEVEN = "SEND_END_RESERVATION_STATE"
STATE_EIGHT = "SEND_FLIGHT_PARAMETERS_TO_DRONE_STATE"

CUSTOMER_ID = "AASD_CUSTOMER@01337.io"
START_STATION_ID = ""
END_STATION_ID = ""
DRONE_ID = "AASD_DRONE@01337.io"


class RequestHandler(Agent):
    class RequestHandlerBehaviour(FSMBehaviour):

        async def on_start(self):
            print(f"[{self.agent.jid.localpart}]: Starting behaviour . . .")

        async def on_end(self):
            print(f"[{self.agent.jid.localpart}]: Behaviour finished with exit code {self.exit_code}.")

    class StateOne(State):

        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 1")
            flight_parameters = await self.receive(timeout=100)  # wait for a message for 10 seconds
            if flight_parameters and json.loads(flight_parameters.body)['title'] == Messages.C_FLIGHT_PARAMS:
                message = json.loads(flight_parameters.body)
                print(f"[{self.agent.jid.localpart}]: Message received with content: {flight_parameters.body}")
                global START_STATION_ID
                START_STATION_ID = message['startStationId']
                global END_STATION_ID
                END_STATION_ID = message['endStationId']
                self.set_next_state(STATE_TWO)
            else:
                print(f"[{self.agent.jid.localpart}]: Did not received any message after 10 seconds")
                self.set_next_state(STATE_ONE)

    class StateTwo(State):
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 2")
            are_drones_available_request = Message(to="AASD_CONTROL_STATION@01337.io")
            are_drones_available_request.set_metadata("performative", "inform")
            are_drones_available_request.body = Messages.rh_drones_available_request(self, START_STATION_ID,
                                                                                     END_STATION_ID, CUSTOMER_ID)
            await self.send(are_drones_available_request)
            self.set_next_state(STATE_THREE)

    class StateThree(State):
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 3")
            are_drones_available_response = await self.receive(timeout=100)
            if are_drones_available_response:
                print(f"[{self.agent.jid.localpart}]: Message received with content: {are_drones_available_response.body}")
                message = json.loads(are_drones_available_response.body)
                self.set_next_state(STATE_FOUR)
            else:
                print(f"[{self.agent.jid.localpart}]: Did not received any message after 100 seconds")
                self.set_next_state(STATE_THREE)

    class StateFour(State):
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 4")
            flight_proposition = Message(to='AASD_CUSTOMER@01337.io')
            flight_proposition.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            flight_proposition.body = Messages.rh_flight_proposition_info(self.agent, DRONE_ID, CUSTOMER_ID)
            await self.send(flight_proposition)
            print(f"[{self.agent.jid.localpart}]: Proposition sent")
            self.set_next_state(STATE_FIVE)

    class StateFive(State):
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 5")
            customer_decision = await self.receive(timeout=30)  # wait for a message for 10 seconds
            if customer_decision:
                print(f"[{self.agent.jid.localpart}]: Message received with content: {customer_decision.body}")
                self.set_next_state(STATE_SIX)
            else:
                print(f"[{self.agent.jid.localpart}]: Did not received any message after 10 seconds")
                self.set_next_state(STATE_FIVE)

    class StateSix(State):
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 6")
            reservation_start = Message(to=START_STATION_ID)  # wait for a message for 10 seconds
            reservation_start.set_metadata("performative", "inform")
            reservation_start.body = Messages.rh_start_flight_reservation(self.agent, DRONE_ID, CUSTOMER_ID,
                                                                          START_STATION_ID, END_STATION_ID)
            await self.send(reservation_start)
            print(f"[{self.agent.jid.localpart}]: Start reservation sent")
            self.set_next_state(STATE_SEVEN)

    class StateSeven(State):
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 7")
            reservation_end = Message(to=END_STATION_ID)  # wait for a message for 10 seconds
            reservation_end.set_metadata("performative", "inform")
            reservation_end.body = Messages.rh_end_flight_reservation(self.agent, DRONE_ID, CUSTOMER_ID, END_STATION_ID)
            await self.send(reservation_end)
            print(f"[{self.agent.jid.localpart}]: End reservation sent")
            self.set_next_state(STATE_EIGHT)

    class StateEight(State):
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            print(f"[{self.agent.jid.localpart}]: I'm at state 8")
            flight_parameters = Message(to='AASD_DRONE@01337.io')  # wait for a message for 10 seconds
            flight_parameters.set_metadata("performative", "inform")
            flight_parameters.body = Messages.rh_flight_parameters(self.agent, DRONE_ID, CUSTOMER_ID,
                                                                   START_STATION_ID, END_STATION_ID)
            await self.send(flight_parameters)
            print(f"[{self.agent.jid.localpart}]: Flight parameters sent")
            self.set_next_state(STATE_ONE)

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.requestHandlerBehaviour = self.RequestHandlerBehaviour()

    async def setup(self):
        print(f"[{self.jid.localpart}]: Agent starting . I'm agent {str(self.jid)}")
        self.requestHandlerBehaviour.add_state(name=STATE_ONE, state=self.StateOne(self.jid), initial=True)
        self.requestHandlerBehaviour.add_state(name=STATE_TWO, state=self.StateTwo(self.jid))
        self.requestHandlerBehaviour.add_state(name=STATE_THREE, state=self.StateThree(self.jid))
        self.requestHandlerBehaviour.add_state(name=STATE_FOUR, state=self.StateFour(self.jid))
        self.requestHandlerBehaviour.add_state(name=STATE_FIVE, state=self.StateFive(self.jid))
        self.requestHandlerBehaviour.add_state(name=STATE_SIX, state=self.StateSix(self.jid))
        self.requestHandlerBehaviour.add_state(name=STATE_SEVEN, state=self.StateSeven(self.jid))
        self.requestHandlerBehaviour.add_state(name=STATE_EIGHT, state=self.StateEight(self.jid))

        self.requestHandlerBehaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        self.requestHandlerBehaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.requestHandlerBehaviour.add_transition(source=STATE_THREE, dest=STATE_FOUR)
        self.requestHandlerBehaviour.add_transition(source=STATE_FOUR, dest=STATE_FIVE)
        self.requestHandlerBehaviour.add_transition(source=STATE_FIVE, dest=STATE_SIX)
        self.requestHandlerBehaviour.add_transition(source=STATE_SIX, dest=STATE_SEVEN)
        self.requestHandlerBehaviour.add_transition(source=STATE_SEVEN, dest=STATE_EIGHT)
        self.requestHandlerBehaviour.add_transition(source=STATE_EIGHT, dest=STATE_ONE)
        self.requestHandlerBehaviour.add_transition(source=STATE_ONE, dest=STATE_ONE)
        self.requestHandlerBehaviour.add_transition(source=STATE_THREE, dest=STATE_THREE)
        self.requestHandlerBehaviour.add_transition(source=STATE_FIVE, dest=STATE_FIVE)
        self.add_behaviour(self.requestHandlerBehaviour)
