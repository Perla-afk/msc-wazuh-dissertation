# 10 - Development and Excluded Commands

These commands and tests show problems found during the project and how they were fixed. They are **not used in the final statistics**.

## Clock drift investigation

```powershell
Get-Service W32Time | Select-Object Status,StartType,Name
```

```powershell
Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff K"; w32tm /query /status
```

```powershell
w32tm /stripchart /computer:192.168.56.10 /samples:5 /dataonly
```

## Wazuh NTP server checks during troubleshooting

```bash
systemctl is-active chrony 2>/dev/null; systemctl is-active systemd-timesyncd 2>/dev/null
```

```bash
sudo ss -lunp | grep ':123 ' || echo "Nothing listening on UDP 123"
```

```bash
dpkg -l | grep -E '^ii\s+(chrony|ntp|ntpsec)\s' || echo "No NTP server package installed"
```

## AI Recon uncorrected functional pilot

**EXCLUDED / VALIDATION**

```powershell
$start=Get-Date; "AI-RECON-UNCORRECTED-PILOT-02 START = "+$start.ToString("yyyy-MM-dd HH:mm:ss.fff"); nmap -sT -Pn -p 135,139,445,3389 192.168.56.104
```

Windows Event 5157 was present during this test, but the uncorrected AI Recon rule did not create rule `110105` inside the observation window. This test was kept as validation evidence and was not used as a formal result.

## Corrected AI Recon diagnostic

**VALIDATION**

```powershell
$start=Get-Date; "AI-RECON-CORRECTED-DIAGNOSTIC-02 START = "+$start.ToString("yyyy-MM-dd HH:mm:ss.fff"); nmap -sT -Pn -p 135,139,445,3389 192.168.56.104
```

The corrected rule worked in this validation test. After that, the configuration was frozen and the three formal AI Recon runs were completed.
