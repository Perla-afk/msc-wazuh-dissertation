# 06 - Manual Reconnaissance Rule

The final Manual Recon rule used Windows Event 5157. Earlier tests used 5152 and the parent T1595 mapping, but those were development steps and were not the final formal rule.

## Check the default Wazuh firewall alerts

```bash
sudo jq -c 'select((.rule.id|tostring)=="60104" and (((.data.win.system.eventID|tostring)=="5152") or ((.data.win.system.eventID|tostring)=="5157"))) | {timestamp:.timestamp,eventID:.data.win.system.eventID,eventdata:.data.win.eventdata}' /var/ossec/logs/alerts/alerts.json | tail -n 12
```

## Count event IDs

```bash
sudo jq -r 'select((.rule.id|tostring)=="60104" and (((.data.win.system.eventID|tostring)=="5152") or ((.data.win.system.eventID|tostring)=="5157"))) | .data.win.system.eventID' /var/ossec/logs/alerts/alerts.json | sort | uniq -c
```

## Check rule IDs

```bash
sudo grep -R -nE 'id="100104"|id="100105"' /var/ossec/etc/rules /var/ossec/ruleset/rules 2>/dev/null
```

## Change development rule to Event 5157

**DEVELOPMENT**

```bash
sudo sed -i 's/>^5152$</>^5157$</' /var/ossec/etc/rules/manual_recon_rules.xml
```

## Change the mapping to T1595.001

**DEVELOPMENT**

```bash
sudo sed -i 's/<id>T1595<\/id>/<id>T1595.001<\/id>/' /var/ossec/etc/rules/manual_recon_rules.xml
```

## Check the final rule file

```bash
sudo cat /var/ossec/etc/rules/manual_recon_rules.xml
```

## Test the rule and restart Wazuh

```bash
sudo /var/ossec/bin/wazuh-analysisd -t && sudo systemctl restart wazuh-manager && sudo systemctl is-active wazuh-manager
```

## Save the final rule hash

```bash
sudo sha256sum /var/ossec/etc/rules/manual_recon_rules.xml
```

Final SHA-256:

`c1603402779c1938e08b966f61d5f3861b1394d7d1adf621e3ed31593dbdf12a`

## Run the formal Manual Recon scan

```powershell
$start=Get-Date; "MAN-RECON-<NN> START = "+$start.ToString("yyyy-MM-dd HH:mm:ss.fff"); nmap -sT -Pn -p 135,139,445,3389 192.168.56.104
```

## Check the Manual Recon alerts

```bash
sudo jq -c 'select((.rule.id|tostring)=="100105") | {timestamp:.timestamp,rule_id:.rule.id,description:.rule.description,level:.rule.level,mitre:.rule.mitre,sourceAddress:.data.win.eventdata.sourceAddress,destAddress:.data.win.eventdata.destAddress,destPort:.data.win.eventdata.destPort,eventID:.data.win.system.eventID}' /var/ossec/logs/alerts/alerts.json | tail -n 5
```
