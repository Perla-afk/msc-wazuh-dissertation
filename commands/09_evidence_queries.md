# 09 - Evidence and Alert Queries

These commands were used to check the Wazuh JSON files and confirm the event IDs, rule IDs, fields and MITRE ATT&CK mappings used in the results.

## Check generic Windows Filtering Platform alerts

```bash
sudo jq -c 'select((.rule.id|tostring)=="60104" and (((.data.win.system.eventID|tostring)=="5152") or ((.data.win.system.eventID|tostring)=="5157"))) | {timestamp:.timestamp,eventID:.data.win.system.eventID,sourceAddress:.data.win.eventdata.sourceAddress,destinationAddress:.data.win.eventdata.destAddress,destinationPort:.data.win.eventdata.destPort,direction:.data.win.eventdata.direction}' /var/ossec/logs/alerts/alerts.json | tail -n 5
```

## Check Event 5157 data from 192.168.56.1

```bash
sudo jq -c 'select((.rule.id|tostring)=="60104" and (.data.win.system.eventID|tostring)=="5157" and .data.win.eventdata.sourceAddress=="192.168.56.1") | {timestamp:.timestamp,eventID:.data.win.system.eventID,source:.data.win.eventdata.sourceAddress,destination:.data.win.eventdata.destAddress,port:.data.win.eventdata.destPort}' /var/ossec/logs/alerts/alerts.json | tail -n 15
```

## Manual Recon rule alerts

```bash
sudo jq -c 'select((.rule.id|tostring)=="100105") | {timestamp:.timestamp,rule_id:.rule.id,description:.rule.description,level:.rule.level,mitre:.rule.mitre,sourceAddress:.data.win.eventdata.sourceAddress,destAddress:.data.win.eventdata.destAddress,destPort:.data.win.eventdata.destPort,eventID:.data.win.system.eventID}' /var/ossec/logs/alerts/alerts.json | tail -n 5
```

## AI Recon rule alerts

```bash
sudo jq -c 'select((.rule.id|tostring)=="110105") | {timestamp:.timestamp,rule_id:.rule.id,description:.rule.description,level:.rule.level,mitre:.rule.mitre,source:.data.win.eventdata.sourceAddress,destination:.data.win.eventdata.destAddress,port:.data.win.eventdata.destPort,eventID:.data.win.system.eventID}' /var/ossec/logs/alerts/alerts.json | tail -n 8
```

## Check recent alerts for WIN11-LAB

```bash
sudo jq -c 'select(.agent.id=="001") | {timestamp:.timestamp,agent:.agent.name,rule_id:.rule.id,description:.rule.description}' /var/ossec/logs/alerts/alerts.json | tail -n 20
```

## Check archive logging state

```bash
sudo grep -nE '<logall>|<logall_json>' /var/ossec/etc/ossec.conf; sudo ls -lh /var/ossec/logs/archives/archives.json 2>/dev/null || echo "archives.json not present"
```
