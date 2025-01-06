import requests

# Constants
BRIGHTNESS_RANGE = (0, 100)
TEMPERATURE_RANGE = (143, 344)

# Configuration
PANELS = [
    {"name": "Left Panel", "ip": "192.168.1.217"},
    {"name": "Right Panel", "ip": "192.168.1.218"}
]

# Helper to validate values
def validate(value, min_value, max_value):
    return min_value <= value <= max_value

# Send command to a panel
def send_command(ip, data):
    url = f"http://{ip}:9123/elgato/lights"
    try:
        response = requests.put(url, json=data)
        if response.status_code == 200:
            print(f"Command sent successfully to {ip}")
        else:
            print(f"Error sending command to {ip}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error with {ip}: {e}")

# Build payload and send
def control_panels(action, value=None):
    for panel in PANELS:
        if action == "power":
            data = {"lights": [{"on": 1 if value else 0}], "numberOfLights": 1}
        elif action == "brightness" and validate(value, *BRIGHTNESS_RANGE):
            data = {"lights": [{"brightness": value}], "numberOfLights": 1}
        elif action == "temperature" and validate(value, *TEMPERATURE_RANGE):
            data = {"lights": [{"temperature": value}], "numberOfLights": 1}
        else:
            print(f"Invalid value for {action}: {value}")
            continue
        send_command(panel["ip"], data)

# Main menu
def main_menu():
    while True:
        print("\n--- Elgato Panel Control ---")
        print("1. Turn panels ON")
        print("2. Turn panels OFF")
        print("3. Adjust brightness")
        print("4. Change color temperature")
        print("5. Exit")
        try:
            option = int(input("Select an option: "))
            if option == 1:
                control_panels("power", True)
            elif option == 2:
                control_panels("power", False)
            elif option == 3:
                brightness = int(input(f"Enter brightness ({BRIGHTNESS_RANGE[0]}-{BRIGHTNESS_RANGE[1]}): "))
                control_panels("brightness", brightness)
            elif option == 4:
                temperature = int(input(f"Enter temperature ({TEMPERATURE_RANGE[0]}-{TEMPERATURE_RANGE[1]}): "))
                control_panels("temperature", temperature)
            elif option == 5:
                print("Exiting...")
                break
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a valid number.")

# Run the program
if __name__ == "__main__":
    main_menu()
