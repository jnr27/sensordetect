import RPi.GPIO as GPIO

# GPIO Pin Setup
SENSOR_PIN = 17  # Example GPIO pin

class SENSOR_DETECTOR:
  
    def __init__(self):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SENSOR_PIN, GPIO.IN)

    def check_vibration(self):
       
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:
            return True  
        else:
           return False  
  
    def schedule(self, event_input_name, event_input_value):
       
        if event_input_name == 'INIT':
            print("Initializing sensor...")
            return [event_input_value, None, None] 
        elif event_input_name == 'READ':
            print("Checking sensor for vibration...")
            vibration_status = self.check_vibration()
            return [None, event_input_value, vibration_status] 