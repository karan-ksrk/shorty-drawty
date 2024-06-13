import socket
import pyautogui

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))  # Bind to all interfaces on port 5000
server_socket.listen(1)

print("Server is listening on port 5000...")

# Define a whitelist of allowed macros
whitelist = {
    # "ctrl+c": ["ctrl", "c"],
    # "ctrl+v": ["ctrl", "v"],
    # "ctrl+z": ["ctrl", "z"],
    # "ctrl+y": ["ctrl", "y"],
    # "ctrl+a": ["ctrl", "a"],
    # "alt+tab": ["alt", "tab"],
    # "ctrl+shift+esc": ["ctrl", "shift", "esc"],
    # "win+d": ["win", "d"],
    # "win+r": ["win", "r"],
    # "win+e": ["win", "e"],
    "alt+w+1": ["alt", "w", "1"],
    "alt+w+2": ["alt", "w", "2"],
    "alt+w+3": ["alt", "w", "3"],
    "alt+x": ["alt", "x"],
    "alt+s": ["alt", "s"],
    "alt+i": ["alt", "i"],
    "alt+r": ["alt", "r"],
    # Add more allowed macros as needed
}

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        macro_input = data.decode('utf-8').strip().lower()
        print(f"Received macro: {macro_input}")

        if macro_input in whitelist:
            print(f"Executing macro: {macro_input}")
            pyautogui.hotkey(*whitelist[macro_input])
        else:
            print(f"Rejected macro: {macro_input}")

    client_socket.close()
    print(f"Connection with {addr} closed")
