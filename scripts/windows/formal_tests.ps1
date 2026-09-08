
# T1059.003 - Windows Command Shell
$start=Get-Date; Write-Host "<RUN-ID> START: $($start.ToString('yyyy-MM-dd HH:mm:ss.fff'))"; cmd.exe /c echo WAZUH_T1059_003_TEST

# T1059.001 - PowerShell
$start=Get-Date; Write-Host "<RUN-ID> START: $($start.ToString('yyyy-MM-dd HH:mm:ss.fff'))"; powershell.exe -NoProfile -Command "Write-Output 'WAZUH_T1059_001_TEST'"

# T1082 - System Information Discovery
$start=Get-Date; Write-Host "<RUN-ID> START: $($start.ToString('yyyy-MM-dd HH:mm:ss.fff'))"; systeminfo.exe | Out-Null

# T1033 - System Owner/User Discovery
$start=Get-Date; Write-Host "<RUN-ID> START: $($start.ToString('yyyy-MM-dd HH:mm:ss.fff'))"; whoami.exe

# T1057 - Process Discovery
$start=Get-Date; Write-Host "<RUN-ID> START: $($start.ToString('yyyy-MM-dd HH:mm:ss.fff'))"; tasklist.exe | Out-Null

# T1016 - System Network Configuration Discovery
$start=Get-Date; Write-Host "<RUN-ID> START: $($start.ToString('yyyy-MM-dd HH:mm:ss.fff'))"; ipconfig.exe /all | Out-Null

# T1595.001 - Restricted Active Scanning
$start=Get-Date; Write-Host "<RUN-ID> START = $($start.ToString('yyyy-MM-dd HH:mm:ss.fff'))"; nmap -sT -Pn -p 135,139,445,3389 192.168.56.104
