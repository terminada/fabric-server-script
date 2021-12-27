import argparse
from argparse import HelpFormatter
from operator import attrgetter
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import NumberValidator,PathValidator
import os,psutil,speedtest,requests,pathlib,subprocess
from pySmartDL import SmartDL

# import server_fetcher as sf


class SortingHelpFormatter(HelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter('option_strings'))
        super(SortingHelpFormatter, self).add_arguments(actions)

def check_java():
    sp = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = str(sp.communicate())
    if output.find("Runtime") == -1:
        return False
    return True
  
def size(nbytes):
    suffixes = ['', 'K', 'M']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes //= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s%s' % (f, suffixes[i])

def net_speed(confirm):
    if not confirm:
        return 0
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download(threads=8)
    s.upload(threads=8)
    results_dict = s.results.dict()
    return round((min(results_dict["download"], results_dict["upload"])) / 1048576)

def calc_players(net, ram):
    ram_int = int(ram[:-1])
    net_players = int(net) / 0.5
    ram_players = (ram_int * 0.75) / 256
    max_player = round(min(ram_players, net_players))
    return max_player

def getminecraftversions():
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    json = requests.get(url).json()
    versions = []
    for i in json["versions"]:
        versions.append(i["id"])
    return versions

# def getfabricinstaller():

def fabric_installer_wrapper(mcversion, install_dir):
    # getfabricinstaller()
    if not pathlib.Path("fabric_installer.jar").is_file():
        # return
        response = requests.get("https://meta.fabricmc.net/v2/versions/installer")
        obj = SmartDL(response.json()[0]["url"], "./fabric_installer.jar")
        obj.start()

    os.system("java -jar fabric_installer.jar server -snapshot -downloadMinecraft -dir " + install_dir + " -mcversion " + mcversion)

def make_server(name, version, eula, mem, slots):
    pathlib.Path(name).mkdir(parents=True, exist_ok=True)
    fabric_installer_wrapper(version, name)
    open(os.path.join(name, "eula.txt"), 'w+').write(("eula=" + str(eula).lower()))

    generated_script = "java -Xms" + mem + " -Xmx" + mem + " -jar fabric-server-launch.jar"
    open(os.path.join(name, "start.bat"), 'w+').write(generated_script)
    open(os.path.join(name, "start.sh"), 'w+').write("%s\n%s\n" % ("#!/bin/sh", generated_script))
    # writelines(["#!/bin/sh", generated_script])

    response = requests.get("https://server.properties/")
    server_properties = response.text
    server_properties = server_properties.replace("max-players=20", ("max-players=" + slots))
    server_properties = server_properties.replace("motd=A Minecraft Server", ("motd=" + name))
    server_properties = server_properties.replace("spawn-protection=16", "spawn-protection=0")
    open(os.path.join(name, "server.properties"), 'w+').write(server_properties)

def load_properties(filepath):
    sep = "="
    comment_char="#"
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"') 
                props[key] = value 
    return props
    

# Main code:
versions = getminecraftversions()

# Argument Handling
argparser = argparse.ArgumentParser(description="Fabric Server Script.", prog="main.py", usage="%(prog)s [options]", formatter_class=SortingHelpFormatter)
argparser.add_argument("-H", "--headless", help="Create a server in headless mode.", action="store_true", default=False)
argparser.add_argument("-v", "--version", help="Minecraft Version of the server.", choices=versions, metavar="VERSION")
argparser.add_argument("-e", "--eula", help="Accept Minecraft EULA?", action="store_true", default=False)
argparser.add_argument("-m", "--memory", help="Amount of RAM in Megabytes(MB) to allocate to the server. This will also be used to automatically calculate maximum player slots.", type=int)
argparser.add_argument("-S", "--speedtest", help="Run network speedtest to detect bandwidth. Automatically calculate maximum player slots. Ignored if --network is provided.", action="store_true", default=False)
argparser.add_argument("-N", "--network", help="Your bandwidth in Megabits(Mbps). Used to calculate maximum player slots.", type=int)
argparser.add_argument("-s", "--slots", help="Maximum number of player online. This will ignore automatically calculated maximum player slots.", type=int)
argparser.add_argument("-n", "--name", help="Server name/MOTD.", type=str, default="server")
args = argparser.parse_args()

if args.headless:
    server_name = args.name
    server_version = args.version
    server_eula = args.eula
    server_mem = args.mem + "M"

    server_speed = str(net_speed(args.speedtest))
    server_speed = args.network

    server_slots = str(calc_players(server_speed, server_mem))
    server_slots = args.slots

    make_server(name=server_name, version=server_version, eula=server_eula, mem=server_mem, slots=server_slots)


# Main loop:
while True:
    menu = inquirer.select(
        message="Da hell u want?",
        choices=[
            Choice("make", name="Make a Minecraft server!"), 
            Separator(),
            Choice("configure", name="Configure a Minecraft server."), 
            # Choice("add", name="Add a Minecraft server.")
        ]
    ).execute()

    if menu == "make":
        print("Minecraft (Fabric) server creation wizard...")
        server_name = inquirer.text(message="Your server name (used for MOTD):", default="server").execute()
        server_version = inquirer.fuzzy(message="Server Minecraft version.", choices=versions).execute()
        server_eula = inquirer.confirm(message="Accept Minecraft EULA?", default=False).execute()

        server_mem = size(psutil.virtual_memory().available)
        server_mem = inquirer.text(
            message="Amount of RAM in Megabytes(MB) to allocate to the server. Press ENTER to use suggested value:", 
            default=server_mem[:-1],
            validate=NumberValidator(float_allowed=False)
        ).execute() + "M"

        # server_speed = 0
        # confirm_speedtest = inquirer.confirm(message="Perform network speed test to calculate maximum player slots?", default=True).execute()
        # if inquirer.confirm(message="Perform network speed test to calculate maximum player slots?", default=True).execute():
        server_speed = str(net_speed(inquirer.confirm(message="Perform network speed test to calculate maximum player slots?", default=True).execute()))
        server_speed = inquirer.text(
            message="Your bandwidth in Megabits(Mbps). Press ENTER to use suggested value:", 
            default=server_speed,
            validate=NumberValidator(float_allowed=False)
        ).execute()

        server_slots = str(calc_players(server_speed, server_mem))
        server_slots = inquirer.text(
            message="Maximum number of player online. Press ENTER to use calculated value:", 
            default=server_slots,
            validate=NumberValidator(float_allowed=False)
        ).execute()

        make_server(name=server_name, version=server_version, eula=server_eula, mem=server_mem, slots=server_slots)

    if menu == "configure":
        print("Minecraft (Fabric) server configuration wizard...")
        config_menu = inquirer.select(
            message="What do you want to configure?", 
            choices=[
                Choice("properties", name="Properties file."),
                Separator(),
                Choice("bash", name="Bash launch script (start.sh)."),
                Choice("batch", name="Batch launch script (start.bat).")
            ]
        ).execute()

        if config_menu == "properties":
            properties_path = str(pathlib.Path().resolve())
            while not properties_path.endswith("server.properties"):
                properties_path = inquirer.filepath(
                    message="Specify server.properties file location:",
                    default=properties_path,
                    validate=PathValidator(is_file=True, message="Not a file."),
                    only_files=True
                ).execute()
            properties = load_properties(properties_path)
            # properties_key = ""
            while True:
                properties_key = inquirer.fuzzy(
                    message="Choose property to change (quit to exit):", 
                    choices = [Choice(key) for key in properties]
                )
                if properties_key == "quit":
                    break
                properties[properties_key] = inquirer.text(
                    message="Value for property " + properties_key + " :",
                    choices = properties[properties_key]
                )
            # properties_key_lookups = [Choice(key) for key in properties]
            

        if config_menu == "bash":
            properties_path = str(pathlib.Path().resolve())
            while not properties_path.endswith(".sh"):
                properties_path = inquirer.filepath(
                    message="Specify start.sh file location:",
                    default=properties_path,
                    validate=PathValidator(is_file=True, message="Not a file."),
                    only_files=True
                ).execute()

        if config_menu == "batch":
            properties_path = str(pathlib.Path().resolve())
            while not properties_path.endswith(".bat"):
                properties_path = inquirer.filepath(
                    message="Specify start.bat file location:",
                    default=properties_path,
                    validate=PathValidator(is_file=True, message="Not a file."),
                    only_files=True
                ).execute()


