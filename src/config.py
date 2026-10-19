import os
from dotenv import load_dotenv

load_dotenv()

LTA_API_KEY = os.getenv("LTA_API_KEY")
BUS_ARRIVAL_URL = "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival"
STOPS_FILE = "config/stops.txt"
OUTPUT_DIR = "data/raw/bus_arrival"