@echo off

REM start a remote capture session using the provided live capture 
REM tcp port as defined in UWM
REM adapt path to Wireshark and NetCat (nc.exe) binaries
REM 
REM NetCat for Windows can be found, e.g. at: https://nmap.org/ncat/
REM
REM sebastian.rieger@cs.hs-fulda.de

if -%1-==-- echo live capture tcp port not provided, please start as "capture-from-socket.bat <tcp-live-capture-port>" & exit /b

set NETCAT_PATH="C:\Users\Sebastian\Downloads\ncat"
set WIRESHARK_PATH="C:\Program Files\Wireshark\Wireshark.exe"
set VIRL_HOST="192.168.0.100"
set PCAP_PORT="%1"

start cmd /C "echo reading live capture from port %1, close Wireshark, to stop ... & %NETCAT_PATH% %VIRL_HOST% %PCAP_PORT% | %WIRESHARK_PATH% -k -i -"
