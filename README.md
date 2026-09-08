# MSc Cybersecurity Dissertation - Wazuh Commands and Rules

This repository contains the main commands, scripts and Wazuh rules used during my MSc Cybersecurity dissertation project.

The project compared three Wazuh SIEM configurations:

1. Baseline/default Wazuh
2. Manually tuned Wazuh
3. AI-assisted Wazuh configuration generated using the OpenAI API

The research question used in the final dissertation is:

**Can AI-assisted configuration improve SIEM detection performance?**

## Lab setup

- Wazuh 4.14.6 on Ubuntu Server 24.04.4 LTS
- Windows 11 Pro endpoint with Wazuh Agent 4.14.6
- Sysmon64
- VirtualBox host-only network: `192.168.56.0/24`
- Wazuh server: `192.168.56.10`
- Windows endpoint: `192.168.56.104`
- Physical laptop host-only address: `192.168.56.1`

## What is inside

- `commands/` - commands used during setup, testing, validation and troubleshooting
- `scripts/windows/` - PowerShell commands used for the formal tests and time checks
- `scripts/ubuntu/` - Wazuh server health checks
- `rules/` - final Manual and AI-assisted Wazuh rules
- `ai/` - the Python generator, prompt and evidence input used for the AI Discovery rules
- `docs/` - a simple index showing where each group of commands is stored

## Important notes

- Formal latency results were only accepted when the clocks were within +/-500 ms, and normally much closer than this.
- Runs affected by clock drift were kept as evidence but were not used in the final results.
- `systeminfo`, `whoami`, `tasklist` and `ipconfig /all` are normal Windows commands as well. They were used to test whether Wazuh could detect the selected MITRE ATT&CK Discovery techniques. Running one of these commands does not automatically mean that an attack happened.
- The Reconnaissance test was limited to four TCP ports on one isolated Windows VM. No exploitation, passwords, malware or persistence were used.
- OpenAI API keys are not stored in this repository.

## Formal commands

The main commands used for the formal tests are in:

- `commands/02_formal_test_commands.md`
- `scripts/windows/formal_tests.ps1`

## Evidence

The screenshot evidence, Wazuh alert evidence, hashes, pilot runs and excluded runs are kept in the separate dissertation evidence archive. This repository is mainly for the commands, scripts and rule files used during the project.
