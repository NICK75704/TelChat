# TelChat
a python based server for chatting over telnet (WIP)

run server.oy and connect to the computer running it over telnet. 
Ex:
run server.py on computer with ip address "192.168.4.78"
on a seperate machine execute "telnet 192.168.4.78 51234" or on the same machine type "telnet localhost 51234". you can connect multiple clients, and set nicknames too. all message history will be stored in log.txt

(51234 is the port used in server.py, this can be changed)
