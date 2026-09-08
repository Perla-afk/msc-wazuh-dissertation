# 03 - Manual Discovery Configuration

The Manual configuration kept the default Wazuh rules and added four custom rules for the Discovery commands that were missed in the Baseline tests.

## Check rule IDs

**VALIDATION**

```bash
sudo grep -R -nE 'id="100100"|id="100101"|id="100102"|id="100103"' /var/ossec/etc/rules 2>/dev/null
```

## Test Wazuh rule syntax

**VALIDATION**

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

## Restart Wazuh manager after adding the rules

**VALIDATION**

```bash
sudo systemctl restart wazuh-manager && sudo systemctl is-active wazuh-manager
```

## Final Manual Discovery rules

- `100100` - T1082 `systeminfo.exe`
- `100101` - T1033 `whoami.exe`
- `100102` - T1057 `tasklist.exe`
- `100103` - T1016 `ipconfig.exe /all`

The final XML file is included in `rules/manual_discovery_rules.xml`.
