# 01 - Lab Health Checks

These commands were used to check that the Wazuh server and Windows endpoint were working before testing.

## Wazuh server - Ubuntu

**VALIDATION**

```bash
hostname && hostname -I
```

```bash
sudo systemctl is-active wazuh-manager
```

```bash
sudo /var/ossec/bin/agent_control -i 001
```

```bash
sudo /var/ossec/bin/agent_control -i 001 | grep -E 'Status|Last keep alive|Configuration hash|Shared file hash'
```

## Windows endpoint

**VALIDATION**

```powershell
Get-Service Sysmon64,wazuhsvc
```

```powershell
Test-NetConnection 192.168.56.10 -Port 1514
```

```powershell
Get-Content 'C:\Program Files (x86)\ossec-agent\ossec.log' -Tail 20
```

The expected state was that Sysmon and the Wazuh agent were running, the agent was connected to `192.168.56.10:1514/tcp`, and the manager showed the endpoint as active.
