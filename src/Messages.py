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


# DRONE

def d_on_station(agent: Agent):
    drone_availability = {
        "droneId": agent.jid.localpart
    }
    return json.dumps(drone_availability, default=str)


# CONTROL_STATION

def cs_status(agent: Agent, availableDrones: str):
    status = {
        availableDrones: availableDrones
    }
    return json.dumps(status)

def cs_is_this_drone_available_req_message(agent: Agent):
    drones_available_request = {
        "title": "",
        "controlStationId": agent.jid.localpart,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(drones_available_request, default=str)

def cs_drones_available_req_message(agent: Agent, droneId: str):
    drones_available_request = {
        "title": "Drones available",
        "controlStationId": agent.jid.localpart,
        "droneId": droneId,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(drones_available_request, default=str)


# CUSTOMER

def c_status(agent: Agent, startStationId: str, endStationId: str):
    status = {
        "title": "status",
        "startStationId": startStationId,
        "endStationId": endStationId
    }
    return json.dumps(status)

def c_flight_params_message(agent: Agent, startStationId: str, endStationId: str):
    flight_request_params = {
        "title": "Flight parameters",
        "customerId": agent.jid.localpart,
        "startStationId": startStationId,
        "endStationId": endStationId,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(flight_request_params, default=str)


def c_affirmative_decision(agent: Agent):
    decision = {
        "title": "Decision affirmative",
        "customerId": agent.jid.localpart,
        "decision": True,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(decision, default=str)


def c_reject_decision(agent: Agent):
    decision = {
        "title": "Rejection",
        "customerId": agent.jid.localpart,
        "decision": False,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(decision, default=str)


# REQUEST_HANDLER

def rh_status(agent: Agent, customer_id: str, start_station_id: str, end_station_id: str, drone_id: str):
    status = {
        "title": "Request handler status",
        "customerId": customer_id,
        "startStationId": start_station_id,
        "endStationId": end_station_id,
        "droneId": drone_id
    }
    return json.dumps(status)

def rh_drones_available_request(agent: Agent, start_station_id: str, end_station_id: str, customer_id: str):
    request = {
        "title": "Are drones available?",
        "requestHandlerId": agent.jid.localpart,
        "startStationId": start_station_id,
        "endStationId": end_station_id,
        "customerId": customer_id,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(request, default=str)


def rh_flight_proposition_info(agent: Agent, drone_id: str, customer_id: str):
    proposition = {
        "title": "Flight proposition",
        "requestHandlerId": agent.jid.localpart,
        "droneId": drone_id,
        "customerId": customer_id,
        "createDate": datetime.datetime.now()
    }
    return json.dumps(proposition, default=str)


def rh_start_flight_reservation(agent: Agent, drone_id: str, customer_id: str, start_station_id: str, end_station_id: str):
    reservation = {
        "title": "Start station reservation",
        "requestHandlerId": agent.jid.localpart,
        "droneId": drone_id,
        "customerId": customer_id,
        "startStationId": start_station_id,
        "endStationId": end_station_id,
        "reservationStatus": "started",
        "createDate": datetime.datetime.now()
    }
    return json.dumps(reservation, default=str)


def rh_end_flight_reservation(agent: Agent, drone_id: str, customer_id: str, end_station_id: str):
    reservation = {
        "title": "End station reservation",
        "requestHandlerId": agent.jid.localpart,
        "droneId": drone_id,
        "customerId": customer_id,
        "endStationId": end_station_id,
        "reservationStatus": "ended",
        "createDate": datetime.datetime.now()
    }
    return json.dumps(reservation, default=str)


def rh_flight_parameters(agent: Agent, drone_id: str, customer_id: str, start_station_id: str, end_station_id: str):
    parameters = {
        "title": "Flight parameters",
        "requestHandlerId": agent.jid.localpart,
        "droneId": drone_id,
        "customerId": customer_id,
        "startStationId": start_station_id,
        "endStationId": end_station_id,
    }
    return json.dumps(parameters, default=str)