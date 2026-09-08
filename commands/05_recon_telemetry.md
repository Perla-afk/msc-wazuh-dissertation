# 05 - Reconnaissance Endpoint Telemetry

The original Sysmon setup did not give the inbound scan information needed for the Reconnaissance test. Windows Filtering Platform failure auditing was enabled on WIN11-LAB so Wazuh could receive Events 5152 and 5157. The same endpoint telemetry setup was kept for Baseline, Manual and AI-assisted Recon testing.

## Check endpoint Security log collection

**VALIDATION**

```powershell
Select-String -Path 'C:\Program Files (x86)\ossec-agent\ossec.conf' -Pattern '<location>Security</location>' -Context 3,10
```

## Check local shared agent configuration

```powershell
if (Test-Path 'C:\Program Files (x86)\ossec-agent\shared\agent.conf') { Get-Content 'C:\Program Files (x86)\ossec-agent\shared\agent.conf' } else { 'No shared agent.conf on endpoint' }
```

## Check Wazuh endpoint logs after restart

```powershell
Get-Content 'C:\Program Files (x86)\ossec-agent\ossec.log' -Tail 35
```

## Restart Wazuh agent when required during validation

```powershell
Restart-Service WazuhSvc; Start-Sleep -Seconds 10; Get-Service WazuhSvc
```

Event 5156 stayed excluded because it produced more normal connection noise. Events 5152 and 5157 were allowed for the Recon tests.
