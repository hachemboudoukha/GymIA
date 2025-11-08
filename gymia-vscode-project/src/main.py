import os
import sys
from gymia_integration.connector import GymIAConnector

def main():
    # Initialize the GymIA integration
    connector = GymIAConnector()

    # Run the integration logic
    connector.run()

if __name__ == "__main__":
    main()