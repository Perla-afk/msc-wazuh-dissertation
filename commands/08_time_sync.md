# 08 - Time Synchronisation

Clock drift was found during early testing. Because latency used timestamps from different machines, the Wazuh server, physical laptop and WIN11-LAB were synchronized before the final timing runs.

## Wazuh server timezone

```bash
sudo timedatectl set-timezone Europe/London && timedatectl
```

```bash
date '+%Y-%m-%d %H:%M:%S.%3N %Z %z'
```

## Install Chrony on Wazuh server

```bash
sudo apt update && sudo apt install -y chrony
```

## Allow the host-only network to use the Wazuh server for NTP

```bash
grep -q '^allow 192\.168\.56\.0/24' /etc/chrony/chrony.conf || echo 'allow 192.168.56.0/24' | sudo tee -a /etc/chrony/chrony.conf
```

## Enable/start Chrony

```bash
sudo systemctl enable --now chrony && sudo systemctl restart chrony
```

## Check Chrony state

```bash
systemctl is-active chrony
```

```bash
chronyc tracking
```

```bash
sudo ss -lunp | grep ':123 ' || echo "ERROR: Chrony is not listening on UDP 123"
```

```bash
grep -n '^allow' /etc/chrony/chrony.conf
```

## Windows - use the Wazuh server as the NTP source

Run on the physical laptop and WIN11-LAB in Administrator PowerShell.

```powershell
Set-Service W32Time -StartupType Automatic; Start-Service W32Time; w32tm /config /manualpeerlist:"192.168.56.10,0x8" /syncfromflags:manual /update; w32tm /resync /force
```

## Windows - check NTP status

```powershell
w32tm /query /status
```

```powershell
w32tm /query /peers
```

## Windows - check the time offset from the Wazuh server

```powershell
w32tm /stripchart /computer:192.168.56.10 /samples:5 /dataonly
```

## Windows timezone check

```powershell
tzutil /g
```

Formal latency runs were only used when the measured clock offset was inside the chosen limit.
