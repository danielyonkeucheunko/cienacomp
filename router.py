import subprocess
import sys
import time
import select

from simulation import read_hardware_state, write_hardware_state, calculate_f, mutate_hardware, mutate_database, create_hardware_file, file_path

def print_cli_history(history):
    for entry in history:
        print(entry)

def swap_state(file_path, history, t):
    state_values, control_values, signal_values = read_hardware_state(file_path)
    history.append(f"{t} swap {state_values[0]} {state_values[1]}")
    state_values[0], state_values[1] = state_values[1], state_values[0]
    write_hardware_state(file_path, state_values, control_values, signal_values)

def process_cli_input(file_path, history, t):
    # Process CLI input here
    try:
        user_input = input("Enter CLI command: ")
        command, *args = user_input.split()
        if command == "set":
            index = int(args[0]) - 1
            value = int(args[1])
            if index < 0 or index >3 :
                print(f"Invalid Input - Error: {index}")
            else:
                mutate_database(file_path, index, value)
                history.append(f"{t} set {index} {value}")
    except Exception as e:
        print(f"Invalid Input - Error: {str(e)}")

def main():
    history = []
    t = 0


    while t < 60:
        state_values, control_values, signal_values = read_hardware_state(file_path)
        t += 1

        # Write Your Code Here Start

        print("\nWhat did operation did you want to perform?\n"
        "1. Forward Data Traffic\n2. Handle Control Traffic\n"
        f"3. Manage Functionality\n10. Exit Program Early and Print History\n\nCurrent Time = {t}\n")

        # Take user input 
        user_case = input("Operation (1-3): ") 

        try:
            # convert input to int
            user_case = int(user_case) 
        except:
            print("Input is likely not a number...") 

        match user_case: 
            # If user selects 1, forward user traffic
            case 1: 
                number = calculate_f(*state_values, *control_values)
                print(f"Output: f() = {number}")
            
            # If user selects 2, handle control traffic
            case 2:
                mutate_hardware(file_path, signal_values[0] - 1, signal_values[1])
            
            # If user selects 3, manage functionality
            case 3:
                process_cli_input(file_path, history, t)
            
            # If user selects 10, break out of the loop and display history
            case 10:
                break
            case _:
                print("Invalid Input.")
        
        # Implement Case 4 Every 10 Seconds
        # Swap 
        if t % 10 == 0:
            swap_state(file_path,history, t)
                


        # Write Your Code Here End

        time.sleep(1)  # Wait for 1 second before polling again
    print(history) # Print history at the end

if __name__ == '__main__':
    main()