import datetime
import json
import random

from spade.agent import Agent

STATIONS_NUMBER = 20

# CONTROL_STATION
CD_DRONES_AVAILABLE = "Drones available"

# CUSTOMER
C_FLIGHT_PARAMS = "Flight parameters"
C_AFFIRMATIVE_DECISION = "Decision affirmative"

# DRONE

# REQUEST_HANDLER
RH_RQ_DRONES_AVAILABLE = "Are drones available?"
RH_RQ_FLIGHT_PROPOSITION = "Flight proposition"
RH_START_RESERVATION = "Start station reservation"
RH_END_RESERVATION = "End station reservation"
RH_FLIGHT_PARAMETERS = "Flight parameters"




# CONTROL_STATION

def cs_drones_available_req_message(agent: Agent):
    drones_available_request = {
        "title": "Drones available",
        "controlStationId": agent.jid,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(drones_available_request)


# CUSTOMER

def c_flight_params_message(agent: Agent):
    flight_request_params = {
        "title": "Flight parameters",
        "customerId": agent.jid,
        "startStationId": str(random.randrange(0, STATIONS_NUMBER, 1)),
        "endStationId": str(random.randrange(0, STATIONS_NUMBER, 1)),
        "createDate": datetime.datetime.now()
    }
    return json.dumps(flight_request_params)


def c_affirmative_decision(agent: Agent):
    decision = {
        "title": "Decision affirmative",
        "customerId": agent.jid,
        "decision": True,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(decision)


def c_reject_decision(agent: Agent):
    decision = {
        "title": "Rejection",
        "customerId": agent.jid,
        "decision": False,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(decision)


# REQUEST_HANDLER

def rh_drones_available_request(agent: Agent, start_station_id: str, end_station_id: str):
    request = {
        "title": "Are drones available?",
        "requestHandlerId": agent.jid,
        "startStationId": start_station_id,
        "endStationId": end_station_id,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(request)


def rh_flight_proposition_info(agent: Agent, drone_id: str, customer_id: str):
    proposition = {
        "title": "Flight proposition",
        "requestHandlerId": agent.jid,
        "droneId": drone_id,
        "customerId": customer_id,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(proposition)


def rh_start_flight_reservation(agent: Agent, drone_id: str, customer_id: str):
    reservation = {
        "title": "Start station reservation",
        "requestHandlerId": agent.jid,
        "droneId": drone_id,
        "customerId": customer_id,
        "reservationStatus": "started",
        "createDate": datetime.datetime.now()
    }
    return json.dumps(reservation)


def rh_end_flight_reservation(agent: Agent, drone_id: str, customer_id: str):
    reservation = {
        "title": "End station reservation",
        "requestHandlerId": agent.jid,
        "droneId": drone_id,
        "customerId": customer_id,
        "reservationStatus": "ended",
        "createDate": datetime.datetime.now()
    }
    return json.dumps(reservation)


def rh_flight_parameters(agent: Agent, drone_id: str, customer_id: str, start_station_id: str, end_station_id: str):
    parameters = {
        "title": "Flight parameters",
        "requestHandlerId": agent.jid,
        "droneId": drone_id,
        "customerId": customer_id,
        "startStationId": start_station_id,
        "endStationId": end_station_id,
    }
    return json.dumps(parameters)