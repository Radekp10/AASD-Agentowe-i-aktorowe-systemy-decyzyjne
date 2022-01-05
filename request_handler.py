import time
import asyncio
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.message import Message


STATE_ONE = "STATE_GET_FLIGHT_PARAMETERS"
STATE_TWO = "STATE_GIVE_FLIGHT_PROPOSITION"
STATE_THREE = "STATE_GET_DECISION"


class RequestHandler(Agent):
    class RequestHandlerBehaviour(FSMBehaviour):
        async def on_start(self):
            print("REQUEST_HANDLER: Starting behaviour . . .")

        async def on_end(self):
            print("REQUEST_HANDLER: Behaviour finished with exit code {}.".format(self.exit_code))

    class StateOne(State):
        async def run(self):
            print("REQUEST_HANDLER: I'm at state one")
            flightParameters = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if flightParameters:
                print("REQUEST_HANDLER: Message received with content: {}".format(flightParameters.body))
            else:
                print("REQUEST_HANDLER: Did not received any message after 10 seconds")
            self.set_next_state(STATE_TWO)

    class StateTwo(State):
        async def run(self):
            print("REQUEST_HANDLER: I'm at state two")
            flightProposition = Message(to='AASD_CUSTOMER@01337.io')
            flightProposition.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            flightProposition.body = "Flight proposition"
            await self.send(flightProposition)
            print("REQUEST_HANDLER: Propositon sent, moving to state 3")
            self.set_next_state(STATE_THREE)

    class StateThree(State):
        async def run(self):
            print("REQUEST_HANDLER: I'm at state three")
            customerDecision = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if customerDecision:
                print("REQUEST_HANDLER: Message received with content: {}".format(customerDecision.body))
            else:
                print("REQUEST_HANDLER: Did not received any message after 10 seconds")


    async def setup(self):
        print("REQUEST_HANDLER: Agent starting . I'm agent {}".format(str(self.jid)))
        self.requestHandlerBehaviour = self.RequestHandlerBehaviour()
        self.requestHandlerBehaviour.add_state(name=STATE_ONE, state=self.StateOne(), initial=True)
        self.requestHandlerBehaviour.add_state(name=STATE_TWO, state=self.StateTwo())
        self.requestHandlerBehaviour.add_state(name=STATE_THREE, state=self.StateThree())
        self.requestHandlerBehaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        self.requestHandlerBehaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.add_behaviour(self.requestHandlerBehaviour)


