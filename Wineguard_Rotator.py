#Python program to control Winegard Playmaker as an AZ/EL Rotor from Gpredict / any software that uses the hamlib API
#Original Author - Gabe Emerson / Saveitforparts 2024, Email: gabe@saveitforparts.com
#Modified Author - Brayden Herman / AZBUBBA 2026, Email Brayden.Herman@gmail.com

import serial
import socket 
import regex as re
import time

#initialize some variables
current_az = 0.0  
current_el = 0.0
index = 0

#gets the local ip so the user does not have to manualy set it
def get_local_ip():
    # Create a dummy UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an arbitrary external address (does not send packets)
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        # Fallback to loopback if no internet network interface is active
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

#Ask user for important vars instead of baking them into the code - allows this same code to be used on diffrent devices without having to modify the code for each device
while True: 
    # 1. Ask user for USB port to use and Serial Speed(Baudrate)
    selected_port = input("Enter Serial Port: ")
    selected_baud = input("Enter Baudrate (defualt: 115200): ") or '115200'
    selected_ip = input('Enter IP (leave blank to automaticly get the ip): ') or get_local_ip()
    selected_netport = int(input('Enter Network Port (default: 4533): ') or '4533')
    
    # 2. List the values back to the user
    print("\nYou entered:")
    print(f"Serial Port: {selected_port}")
    print(f"Serial Baudrate: {selected_baud}")
    print(f'IP: {selected_ip}')
    print(f'Network Port: {selected_netport}')
    
    # 3. Ask for confirmation
    confirm = input("\nIs this correct? (default n) (y/n): ").strip().lower() #forces input into lowercase to make code easier
    
    # Check if the cleaned input matches any of our allowed 'yes' options
    if confirm in ['y', 'yes']:
        break  # Exit the loop
    else:
        print("Please enter valid arguments\n" + "-"*20)


#define "carryout" as the serial port device to interface with
carryout = serial.Serial(
	port=selected_port,
	baudrate=selected_baud,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1)
	
print ('Carryout antenna connected on ', carryout.port)

carryout.write(bytes(b'q\r')) #go back to root menu in case firmware was left in a submenu
carryout.write(bytes(b'\r')) #clear firmware prompt to avoid unknown command errors
carryout.write(bytes(b'mot\r')) # go to mot menu - needed to access motor control commands
print('Please wait till homing is done')
carryout.write(bytes(b'h 0\r')) # home az
time.sleep(10)
carryout.write(bytes(b'h 1\r')) # home el
time.sleep(10)
print('Homing done')

#listen to local port for rotctld commands
listen_ip = selected_ip #Get IP from earlier
listen_port = selected_netport # Get Network Port from earlier
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind((listen_ip, listen_port))
client_socket.listen(1)

# Outer loop to keep the server running for new connections
while True:
    print ('\nListening for rotor commands on', listen_ip, ':', listen_port)
    conn, addr = client_socket.accept()
    print ('Connection from ', addr)

    # Inner loop to handle data from the currently connected client
    while True:
        data = conn.recv(100)  #get Gpredict's message
        if not data:
            print('Connection closed by client.')
            break
            
        cmd = data.decode("utf-8").strip().split(" ")   #grab the incoming command
        
        #print("Received: ",cmd)    #debugging, what did Gpredict send?
        
        if cmd[0] == "p":   #Gpredict is requesting current position
            response = "{}\n{}\n".format(current_az, current_el)
            conn.send(response.encode('utf-8'))
            
        elif cmd[0] == "P":   #Gpredict is sending desired position
            target_az = float(cmd[1])
            target_el = float(cmd[2])
            print(' Move antenna to:', target_az, ' ', target_el, end="\r")
            
            #tell Carryout to move to target position
            #carryout.write(bytes(b'mot\r\n')) #go to motor menu
            time.sleep(0.25)
            command_az = ('a ' + '0 '+ str(target_az) + '\r').encode('ascii')
            command_el = ('a ' + '1 '+ str(target_el) + '\r').encode('ascii')
            carryout.write(command_az)
            time.sleep(0.25)
            carryout.write(command_el)
            current_az = target_az
            current_el = target_el
                
            #Tell Gpredict things went correctly
            response="RPRT 0\n "  #Everything's under control, situation normal
            conn.send(response.encode('utf-8'))
            
            #read data from wineguard?

        elif cmd[0] == "S": #Gpredict says to stop
            print('Gpredict requested stop. Closing connection...')
            break # Breaks out of the inner loop, goes back to listening
            
        else:
            print('Unknown command received:', cmd[0])
            # Optional: you could choose to break here or just ignore it. 
            # Breaking will safely close the current connection.
            break

    # Clean up the closed connection before waiting for a new one
    conn.close()