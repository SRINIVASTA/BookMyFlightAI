import streamlit as st
from datetime import datetime, timedelta

# ----------- Agent definitions ------------

class PlanningAgent:
    def find_flights(self, destination, date, max_price):
        sample_flights = [
            {"flight": "NY123", "price": 280, "time": "08:00"},
            {"flight": "NY456", "price": 320, "time": "12:00"},
            {"flight": "NY789", "price": 250, "time": "18:00"},
        ]
        filtered = [f for f in sample_flights if f["price"] <= max_price]
        return filtered

class MemoryAgent:
    def get_user_preferences(self, user_id):
        preferences = {
            "user_1": {"seat": "aisle", "avoid_layovers": True},
            "default": {"seat": "window", "avoid_layovers": False},
        }
        return preferences.get(user_id, preferences["default"])

class BookingAgent:
    def book_flight(self, flight):
        return f"Flight {flight['flight']} booked successfully!"

class CriticAgent:
    def validate(self, flights, max_price):
        for f in flights:
            if f["price"] > max_price:
                return False, f"Flight {f['flight']} exceeds budget."
        return True, "All flights are within budget."

# ----------- Orchestrator ------------

class Orchestrator:
    def __init__(self):
        self.planning_agent = PlanningAgent()
        self.memory_agent = MemoryAgent()
        self.booking_agent = BookingAgent()
        self.critic_agent = CriticAgent()

    def process_request(self, user_id, destination, date, max_price):
        flights = self.planning_agent.find_flights(destination, date, max_price)
        preferences = self.memory_agent.get_user_preferences(user_id)
        valid, message = self.critic_agent.validate(flights, max_price)

        if not valid:
            return {"error": message}

        if flights:
            best_flight = min(flights, key=lambda f: f["price"])
            booking_result = self.booking_agent.book_flight(best_flight)
        else:
            return {"error": "No suitable flights found."}

        return {
            "flights_found": flights,
            "preferences": preferences,
            "booking_confirmation": booking_result,
            "validation_message": message,
        }

# ----------- Streamlit UI ------------

st.title("Agentic AI Flight Booking System")

with st.form("flight_form"):
    user_id = st.text_input("User ID", value="user_1")
    destination = st.text_input("Destination", value="New York")
    date_input = st.date_input("Flight Date", value=datetime.now() + timedelta(days=7))
    max_price = st.number_input("Max Price ($)", min_value=50, max_value=1000, value=300)
    submitted = st.form_submit_button("Find Flights")

if submitted:
    orchestrator = Orchestrator()
    result = orchestrator.process_request(user_id, destination, date_input, max_price)

    if "error" in result:
        st.error(result["error"])
    else:
        st.success(result["booking_confirmation"])
        st.write("### Flights Found:")
        st.write(result["flights_found"])
        st.write("### User Preferences:")
        st.write(result["preferences"])
        st.write("### Validation:")
        st.write(result["validation_message"])
