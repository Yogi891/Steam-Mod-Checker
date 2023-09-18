# Steam-Mod-Checker
Parses steam workshop pages to determine if Mods or Files need updated
Currently is set up to communicate with pterodactyl game server management panel.
will attempt to auto install dependancys for pterodactyl.
Parses the file MODlist.txt containing a list of ID's needing checked.
creates hash of all update times and automaticly sets starting hash on starup.
rechecks after a defined time and compares hash, if different will send command to server warning players then restart after set amount of time
