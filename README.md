Light-duty two-axis Az/El rotor using portable satellite antenna. 
The code provided is based on code written by Saveitforparts: https://github.com/saveitforparts/Carryout-Rotor/tree/main
For setup details, please refer to the link above

**What's changed:**
- Updates commands to support the Winegard PathwayX1 (q to go to main menu -> mot to enter the motor menu -> a to change angle)
- Auto-grabs the PC's IP address to make it easier on the user
- The code provided by Saveitforparts has specific parameters baked into the code. To make the code easier to use and allow the same code to be used on other devices without changing the code. The code now asks users to input the information.
- Removed the code that reads the position from the PathwayX1 Board - May be added later once I figure out how to implement it

**Requirements:**
- They can be installed individually or by running "pip install -r requirements.txt"
- Python
- pyserial / python3-serial
- regex
- socket

**Hardware:**
- My model uses a 6-pin phone jack using the RS485 protocol for serial communication; any 6-pin phone cable should work. I've only tested RJ12
- My model uses the RS485 protocol, so you need to find a way to take the 6-pin RJ12 to RS485 to USB
- I used a USB to RS485 adapter
- Amazon Link to what I used:
- RJ12 Cable: https://www.amazon.com/dp/B01M04P82Q?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1
- USB to RS485: https://www.amazon.com/dp/B0CRSVHBQT?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

**Instructions:**
- Connect the serial cable 
- Connect power to the dish
- Run the included .py file
- Enter the name/location of the USB port the serial cable is plugged into
- Enter the Baudrate; for me it's 115200, but it could be different depending on the dish you are using
- Press "enter" if you want the program to set the IP automatically, but if you want to use something different, enter it here (if you don't know 100% what you are doing, leave it blank and let the system automatically grab the IP)
- Enter the port you would like to use. Press "enter" to leave the default value
- The system will ask you to confirm your responses
- The device will home the motors. When homing is done, the dish will point North (AZ 0)
- Adjust the **WHOLE ASSEMBLY** (not just the dish) so that it points north
- Connect Gpredict 
