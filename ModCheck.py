testing = True #setting to true will test API connection to server and test mod file list

api_domain = 'https://your_domain.com'
api_key = 'ptlc_Pterodactyl_Client_API_Key'
server_id = '00ff00-Server_ID-00ff00ff00ff'

file_path = 'MODList.txt' #list of mod ID's each on seporate line
warn_time = 3 #minutes notice given to players before restart
warn_msg = f'Servermsg "Mod Updates needed, Server restart in {warn_time} minutes" '
check_interval = 30 #minutes to wait inbetween checks
parse_time = 1 #time in seconds between checking each mod



init = 1
print('Initializing')
try:
    from pydactyl import PterodactylClient
except:
    print("pydactyl is not installed and will be installed now")
    import importlib
    import subprocess

    try:
        subprocess.check_call(["pip", "install", "py-dactyl"])
        print("pydactyl has been successfully installed.\n please restart")
        input('Press enter to quit')
        init = -1
    except subprocess.CalledProcessError as e:
        init = -1
        print("Failed to install pydactyl: {e}")
        input('Press enter to quit')
if api_key == 'ptlc_Pterodactyl_Client_API_Key' or server_id == '00ff00-Server_ID-00ff00ff00ff' or api_domain == 'https://your_domain.com':
    print('You are missing one or more settings that need to be set')
    print('Please open this in a text editor and change/check "api_domain","api_key","server_id"')
    init = -1
    input('press enter to exit')

if init == -1:quit()

from urllib.request import urlopen
from datetime import datetime, timedelta
from pydactyl import PterodactylClient
import hashlib
from time import sleep



Hash_Old = hashlib.md5()
Hash_Current = hashlib.md5()


# Reformat Modlist
try:
    with open(file_path, 'r') as file:
        file_content = file.read()
    file_content = file_content.replace(',', ';')
    file_content = file_content.replace(';', '\n')
    file_content = file_content.replace(' ', '')
    file_content2 = [line for line in file_content.splitlines() if line.strip()]
    file_content = '\n'.join(file_content2)
    sleep(1) # time for file handle to close
    with open(file_path, 'w') as file:
        file.write(file_content)
    sleep(1) # time for file handle to close
    with open(file_path, 'r') as file:
        mod_count = 0
        for line in file:
            if not line.strip().isnumeric():
                init = -1
                print('Modlist contains non numeric characters')
                print('Please check the file')
                input('Press enter to exit')
                break
            mod_count += 1
    file_content = None #cleanup
    file_content2 = None #cleanup
    sleep(1) # time for file handle to close
except:
    init = -1
    print(f'"{file_path}" Not found or could not be accessed')
    input('Press enter to exit')
    quit()

def ModChecker():
    update_data = []
    with open(file_path, 'r') as file:
        line_counter = 0
        print("Checking Mods")
        for line in file:
            line_counter += 1
            print(f'{line_counter} of {mod_count}')
            url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={line.strip()}"
            page = urlopen(url)
            html_bytes = page.read()
            html_bytes.decode("utf-8")
            html_str = str(html_bytes)
            update_position = html_str.find("Updated")
            if update_position != -1:
                updated_content = html_str[update_position + len("update"):]

            for x in range(3):
                update_position = updated_content.find('<div class="detailsStatRight">')
                updated_content = updated_content[update_position + len('<div class="detailsStatRight">'):]
            update_position = updated_content.find('</div>')
            updated_content = updated_content[:update_position]
            print(f'{line} Last update was {updated_content}\n')
            update_data.append(updated_content.strip())
            sleep(parse_time)
    return(update_data)

def Srv_Restart():
    print("Restart Needed")
    api = PterodactylClient(api_domain, api_key, debug=True)
    print(f'sending {warn_msg}')
    api.client.servers.send_console_command(server_id, warn_msg)
    print(f'waiting {warn_time} minutes')

    sleep(warn_time*60)
    print("Sending Restart command")
    if testing: api.client.servers.get_server_utilization(server_id, detail=False)
    else: api.client.servers.send_power_action(server_id, 'restart')

def Srv_test():
    update_data = 0
    global test_counter
    try:
        test_counter += 1
    except:
        test_counter = 0
    if test_counter > 1:
        update_data = test_counter
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line == "": print(f'{file_path} is empty')
    except:
        print(f'{file_path} is missing or could not be read')
    return update_data

def Srv_Test_Restart():
    api = PterodactylClient(api_domain, api_key, debug=True)
    print('Console message to send = ',warn_msg)
    print('Testing api and get server utilization')
    print(api.client.servers.get_server_utilization(server_id, detail=False))

while init != -1:
    if testing: update_data = Srv_test()
    else: update_data = ModChecker()

    #print(update_data) #uncomment to see date,times of all most in list format
    serialized_data = str(update_data).encode()
    Hash_Current = hashlib.md5(serialized_data)
    if init == 1:
        print("Setting initial hash")
        Hash_Old = Hash_Current
        init = 0
        print ('initial hash = ',Hash_Current.hexdigest())
    if str(Hash_Current.hexdigest()) != str(Hash_Old.hexdigest()):
        if testing: Srv_Test_Restart()
        else: Srv_Restart()
        Hash_Old = Hash_Current
    print(Hash_Current.hexdigest())
    nxt_chk = datetime.now() + timedelta(minutes=check_interval)
    print("Next Check", nxt_chk.strftime('%Y-%m-%d %H:%M:%S'))
    if testing:
        sleep(5)
        if test_counter >= 2:
            input('Test Complete, Press enter to exit')
            break
    else: sleep(check_interval*60)

