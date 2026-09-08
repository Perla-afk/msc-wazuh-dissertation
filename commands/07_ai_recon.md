# 07 - AI-Assisted Reconnaissance Rule

The Recon rule used the same API approach as the Discovery rules, but with a separate Recon prompt, evidence JSON and generator file.

## Create Recon generator from original generator

**DEVELOPMENT**

```bash
cp ~/ai_wazuh/ai_rule_generator.py ~/ai_wazuh/ai_recon_rule_generator.py
```

```bash
sed -i 's#rule_generation_prompt.txt#recon_rule_generation_prompt.txt#; s#baseline_gaps.json#recon_baseline_gap.json#; s#AI-GEN-%Y%m%d-%H%M%S#AI-RECON-GEN-%Y%m%d-%H%M%S#; s/AI-ASSISTED WAZUH RULE GENERATION/AI-ASSISTED WAZUH RECON RULE GENERATION/; s/first formal AI rule-generation request/first formal AI Recon rule-generation request/' ~/ai_wazuh/ai_recon_rule_generator.py
```

## Check the Python file and Recon JSON

```bash
python3 -m py_compile ~/ai_wazuh/ai_recon_rule_generator.py && echo "PASS: AI Recon generator syntax OK"
```

```bash
python3 -m json.tool ~/ai_wazuh/evidence/recon_baseline_gap.json >/dev/null && echo "PASS: Recon evidence JSON valid"
```

## Save the checks before generation

```bash
{ echo "=== AI RECON PRE-GENERATION RECORD ==="; date -Ins; echo "--- Time ---"; timedatectl; echo "--- Existing AI Discovery rules ---"; sudo grep -R -nE 'id="110100"|id="110101"|id="110102"|id="110103"' /var/ossec/etc/rules 2>/dev/null; echo "--- Existing Recon rules ---"; sudo grep -R -nE 'T1595|T1595\.001|id="100104"|id="100105"' /var/ossec/etc/rules 2>/dev/null || echo "PASS: No existing Recon rule"; echo "--- Input hashes ---"; sha256sum ~/ai_wazuh/ai_recon_rule_generator.py ~/ai_wazuh/prompts/recon_rule_generation_prompt.txt ~/ai_wazuh/evidence/recon_baseline_gap.json; } | tee ~/ai_wazuh/validation/AI_RECON_pre_generation.txt
```

## Activate the Python virtual environment

```bash
source ~/ai_wazuh/.venv/bin/activate
```

## Check the Python/OpenAI environment

```bash
which python && python -c 'import openai; print("OpenAI SDK:",openai.__version__)'
```

## Generate the Recon rules

**FORMAL CONFIGURATION GENERATION**

```bash
python ~/ai_wazuh/ai_recon_rule_generator.py
```

Formal generation run: `AI-RECON-GEN-20260905-135329`.

## Check that the generated rule IDs are free

```bash
IDS=$(grep -oP '<rule[^>]*id="\K[0-9]+' ~/ai_wazuh/outputs/AI-RECON-GEN-20260905-135329_generated_rules.xml | paste -sd'|' -); sudo grep -R -nE "id=\"($IDS)\"" /var/ossec/etc/rules /var/ossec/ruleset/rules 2>/dev/null || echo "PASS: Generated rule IDs are unused"
```

## Hash the generated files

```bash
sha256sum ~/ai_wazuh/outputs/AI-RECON-GEN-20260905-135329_exact_prompt.txt ~/ai_wazuh/outputs/AI-RECON-GEN-20260905-135329_raw_response.txt ~/ai_wazuh/outputs/AI-RECON-GEN-20260905-135329_generated_rules.xml ~/ai_wazuh/outputs/AI-RECON-GEN-20260905-135329_metadata.json
```

## Copy the unmodified generated XML into Wazuh

```bash
sudo cp ~/ai_wazuh/outputs/AI-RECON-GEN-20260905-135329_generated_rules.xml /var/ossec/etc/rules/ai_recon_generated_rules.xml
```

## Check that the generated and deployed files match

```bash
sha256sum ~/ai_wazuh/outputs/AI-RECON-GEN-20260905-135329_generated_rules.xml && sudo sha256sum /var/ossec/etc/rules/ai_recon_generated_rules.xml
```

## Test the generated rules in Wazuh

```bash
sudo /var/ossec/bin/wazuh-analysisd -t; echo "wazuh-analysisd exit status: $?"
```

## Human correction after the first functional test failed

**DEVELOPMENT / HUMAN CORRECTION**

```bash
sudo sed -i 's/<rule id="110104" level="0">/<rule id="110104" level="1">/' /var/ossec/etc/rules/ai_recon_generated_rules.xml
```

```bash
sudo sed -i '/<field name="win.eventdata.protocol">\^6\$<\/field>/a\    <options>no_log</options>' /var/ossec/etc/rules/ai_recon_generated_rules.xml
```

## Test the corrected rule

```bash
sudo /var/ossec/bin/wazuh-analysisd -t; echo "wazuh-analysisd exit status: $?"
```

## Save the corrected rule hash

```bash
sudo sha256sum /var/ossec/etc/rules/ai_recon_generated_rules.xml
```

Final corrected SHA-256:

`b8b47527f44481f4766d957866690a912b05d3e81b302485427b230341095c1f`

## Restart Wazuh manager

```bash
sudo systemctl restart wazuh-manager && sudo systemctl is-active wazuh-manager
```

## Run the formal AI Recon scan

```powershell
$start=Get-Date; "AI-RECON-<NN> START = "+$start.ToString("yyyy-MM-dd HH:mm:ss.fff"); nmap -sT -Pn -p 135,139,445,3389 192.168.56.104
```

## Check the AI Recon alerts

```bash
sudo jq -c 'select((.rule.id|tostring)=="110105") | {timestamp:.timestamp,rule_id:.rule.id,description:.rule.description,level:.rule.level,mitre:.rule.mitre,source:.data.win.eventdata.sourceAddress,destination:.data.win.eventdata.destAddress,port:.data.win.eventdata.destPort,eventID:.data.win.system.eventID}' /var/ossec/logs/alerts/alerts.json | tail -n 8
```
