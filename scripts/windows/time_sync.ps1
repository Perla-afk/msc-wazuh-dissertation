Set-Service W32Time -StartupType Automatic; Start-Service W32Time; w32tm /config /manualpeerlist:"192.168.56.10,0x8" /syncfromflags:manual /update; w32tm /resync /force
w32tm /query /status
w32tm /query /peers
w32tm /stripchart /computer:192.168.56.10 /samples:5 /dataonly
tzutil /g
