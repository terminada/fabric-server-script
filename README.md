<h1 align="center">Minecraft Fabric Server creation script</h1>


[![Build Status](https://travis-ci.com/terminada/fabric-server-script.svg?branch=master)](https://travis-ci.com/terminada/fabric-server-script)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/terminada/fabric-server-script/?ref=repository-badge)

![IllumiStudios](https://img.shields.io/badge/Powered%20by-IllumiStudios-black)
[![ApexHosting](https://img.shields.io/badge/Host%20your%20server%20on-Apex%20Hosting-critical)](https://billing.apexminecrafthosting.com/aff.php?aff=2786)


Minecraft Server [setup](https://minecraft.gamepedia.com/Tutorials/Setting_up_a_server) script for Windows, MacOSX, Ubuntu, Debian, CentOS, Fedora... (Not Solaris at the moment), using Python and some dependencies.


## Demo
![screenshot-1](demos/screenshot-1.png "Screenshot 1")

## Installation and usage

For Windows download the `.exe` file from Releases

#### Run from source

```shell
git clone https://github.com/terminada/fabric-server-script.git
cd fabric-server-script
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 main.py
```

__Note__: Using `python3` on Windows 8/10 may open the __Store__, in that case use `python`

#### Build from source (Windows)

```shell
python -m PyInstaller main.py --noconfirm --name="fabric-server-script" --onefile
```

## Dependencies
Better check [requirements.txt](https://github.com/HoangTheBoss/fabric-server-script/blob/master/requirements.txt) for more updated contents
```
InquirerPy
psutil==5.8.0
pySmartDL==1.3.4
requests==2.26.0
speedtest-cli
PyInstaller
```

## Contribute
Do what you can to help the project. Issues and pull requests are welcome.

## I want to run my own MC server but don't have a dedicated machine for that
You can host your server at [Apex Hosting](https://billing.apexminecrafthosting.com/aff.php?aff=2786) for cheap!


