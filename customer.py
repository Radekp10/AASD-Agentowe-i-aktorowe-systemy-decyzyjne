import time
import asyncio
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.message import Message

STATE_ONE = "STATE_GIVE_REQUIREMENTS"
STATE_TWO = "STATE_GET_FLIGHT_PROPOSITION"
STATE_THREE = "STATE_GIVE_DECISION"


class Customer(Agent):
    class CustomerBehaviour(FSMBehaviour):
        async def on_start(self):
            print("CUSTOMER: Starting behaviour. . .")

        async def on_end(self):
            print("CUSTOMER: Behaviour finished with exit code {}.".format(self.exit_code))

    class StateOne(State):
        async def run(self):
            print("CUSTOMER: I'm at state one (initial state)")
            flightParameters = Message(to='AASD_REQUEST_HANDLER@01337.io')
            flightParameters.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            flightParameters.body = "Flight params"
            await self.send(flightParameters)
            print("CUSTOMER: Params sent, moving to state 2")
            self.set_next_state(STATE_TWO)

    class StateTwo(State):
        async def run(self):
            print("CUSTOMER: I'm at state two")
            flightProposition = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if flightProposition:
                print("CUSTOMER: Message received with content: {}".format(flightProposition.body))
            else:
                print("CUSTOMER: Did not received any message after 10 seconds")
            self.set_next_state(STATE_THREE)

    class StateThree(State):
        async def run(self):
            print("CUSTOMER: I'm at state three")
            customerDecision = Message(to='AASD_REQUEST_HANDLER@01337.io')
            customerDecision.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            customerDecision.body = "Decision"
            await self.send(customerDecision)
            print("CUSTOMER: Decision sent")


    async def setup(self):
        print("CUSTOMER: Agent starting . I'm agent {}".format(str(self.jid)))
        self.customerBehaviour = self.CustomerBehaviour()
        self.customerBehaviour.add_state(name=STATE_ONE, state=self.StateOne(), initial=True)
        self.customerBehaviour.add_state(name=STATE_TWO, state=self.StateTwo())
        self.customerBehaviour.add_state(name=STATE_THREE, state=self.StateThree())
        self.customerBehaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        self.customerBehaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.add_behaviour(self.customerBehaviour)
