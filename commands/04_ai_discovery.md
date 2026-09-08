# 04 - AI-Assisted Discovery Rule Generation

The AI-assisted configuration used a Python program and the OpenAI API. The generated output was saved first and checked before it was copied into Wazuh.

## Check API key without printing it

**VALIDATION**

```bash
if [ -n "$OPENAI_API_KEY" ]; then echo "API key loaded securely"; else echo "API key missing"; fi
```

## Load API key interactively

**VALIDATION**

```bash
read -rsp "OpenAI API key: " OPENAI_API_KEY; echo; export OPENAI_API_KEY
```

## Check that the key was loaded without showing it

```bash
python -c 'import os; k=os.getenv("OPENAI_API_KEY",""); print("Loaded:", bool(k)); print("Starts with sk-:", k.startswith("sk-")); print("Contains whitespace:", any(c.isspace() for c in k)); print("Length:", len(k))'
```

## Activate Python virtual environment

```bash
source ~/ai_wazuh/.venv/bin/activate
```

## Check Python/OpenAI SDK

```bash
which python && python -c 'import openai; print("OpenAI SDK:",openai.__version__)'
```

## Check Python syntax

```bash
python -m py_compile ~/ai_wazuh/ai_rule_generator.py && echo "Python syntax OK"
```

## Hash the prompt and evidence input

```bash
sha256sum ~/ai_wazuh/prompts/rule_generation_prompt.txt ~/ai_wazuh/evidence/baseline_gaps.json
```

## Save the checks before generation

```bash
{ echo "=== AI PRE-GENERATION RECORD ==="; date -Ins; python -c "import openai; print('OpenAI SDK:',openai.__version__)"; sha256sum ~/ai_wazuh/ai_rule_generator.py ~/ai_wazuh/prompts/rule_generation_prompt.txt ~/ai_wazuh/evidence/baseline_gaps.json; } | tee ~/ai_wazuh/validation/AI_GEN_01_pre_generation.txt
```

## Run the formal API generation

**FORMAL CONFIGURATION GENERATION**

```bash
python ~/ai_wazuh/ai_rule_generator.py
```

The run ID was `AI-GEN-20260813-152823` using `gpt-5.6-terra`.

## Check that the generated XML can be parsed

```bash
python -c 'import xml.etree.ElementTree as ET; from pathlib import Path; p=sorted((Path.home()/"ai_wazuh/outputs").glob("*_generated_rules.xml"))[-1]; ET.parse(p); print("PASS: AI-generated XML is well-formed")'
```

## Check that the generated rule IDs are free

```bash
sudo grep -RnE '<rule[^>]*id="(110100|110101|110102|110103)"' /var/ossec/etc/rules /var/ossec/ruleset/rules 2>/dev/null || echo "PASS: IDs unused"
```

## Copy the generated XML into Wazuh

```bash
sudo cp ~/ai_wazuh/outputs/AI-GEN-20260813-152823_generated_rules.xml /var/ossec/etc/rules/ai_generated_rules.xml
```

## Check that the generated and deployed files match

```bash
sha256sum ~/ai_wazuh/outputs/AI-GEN-20260813-152823_generated_rules.xml; sudo sha256sum /var/ossec/etc/rules/ai_generated_rules.xml
```

## Test the rules in Wazuh

```bash
sudo /var/ossec/bin/wazuh-analysisd -t; echo "Exit status: $?"
```

## Restart manager

```bash
sudo systemctl restart wazuh-manager && sudo systemctl is-active wazuh-manager
```
