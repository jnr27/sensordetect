# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 14:54:28 2025

@author: jaime
"""

import RPi.GPIO as GPIO
import time

# GPIO Pin Setup
SENSOR_PIN = 17  # Example GPIO pin

class SENSOR_DETECTOR:
  
    def __init__(self):
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SENSOR_PIN, GPIO.IN)
        self.sensor_value = GPIO.input(SENSOR_PIN)  # Initialize the sensor state
        self.output_value = self.sensor_value  # Function block output to hold sensor value
        self.monitoring = False  # To control when to monitor the sensor

    def update_sensor(self):
        """
        Continuously update the sensor value by reading the GPIO pin.
        """
        self.sensor_value = GPIO.input(SENSOR_PIN)
        self.output_value = self.sensor_value  # Update the function block output value

    def check_vibration(self):
        """
        Check if the vibration sensor detects vibration.
        Returns True if vibration is detected (pin state is LOW).
        """
        return self.sensor_value == GPIO.LOW

    def schedule(self, event_input_name, event_input_value):
        """
        Event-triggered schedule method to start/stop the monitoring.
        """
        if event_input_name == 'INIT':
            # Initialization event to set the sensor and start monitoring
            print("Initializing sensor...")
            self.monitoring = True  # Start monitoring when initialized
            return [event_input_value, None, None]  # Return INIT state
        
        elif event_input_name == 'READ':
            if self.monitoring:
                self.update_sensor()  # Continuously update the sensor value
                print("Checking sensor for vibration...")
                # Trigger the output event READ_O with the current sensor value
                return [None, event_input_value, self.output_value]  # Return updated sensor value
            else:
                print("Monitoring not started. Please initialize the sensor first.")
                return [None, event_input_value, None]  # If monitoring hasn't started, return None

    def monitor_sensor(self):
        """
        Monitor the sensor continuously and update the sensor value.
        This method keeps checking the GPIO pin for changes in the sensor's state.
        """
        while True:
            if self.monitoring:
                self.update_sensor()  # Continuously update the sensor value
                time.sleep(0.1)  # Small delay to avoid high CPU usage
            else:
                time.sleep(1)  # Wait before checking if monitoring is enabled


if __name__ == "__main__":
    # Create an instance of the sensor detector
    sensor = SENSOR_DETECTOR()
    
    # Start the monitoring loop in a separate thread to allow continuous checking
    import threading
    monitor_thread = threading.Thread(target=sensor.monitor_sensor)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Example: Initialize the sensor (trigger event)
    sensor.schedule('INIT', None)
    
    # Simulate periodic reading (this could be part of the main loop or event-driven)
    while True:
        result = sensor.schedule('READ', None)
        print(f"Sensor Value: {result[2]}")  # Print continuously updated sensor value
        time.sleep(1)  # Delay between reads (this could vary depending on your needs)
