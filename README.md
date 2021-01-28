Herkansing PTW (Gideon, Pieter, Santosh, Yannick en Thijs)

This application is a proof of concept for a steamclient connecting to a raspberry pi(server) to show different functionalities based on what the user is doing.

1. Run the file TI-basisopdracht.py the server.
2. Run the file TkinterGUI.py the client.
3. Press the button on the serverside to initialize the GUI**(alternative at bottom)
4. Use GUI widgets to activate functionalities

** change line 318    if (s.calls("switch") == 1):  to  if (s.calls("switch") == 0):

This repository also contains data analysation of the provided steam data in steam.json
