# Command Index

This file shows where the main commands are stored and whether they were used for a formal test, validation, development or an excluded test.

| Stage | File | What it contains |
|---|---|---|
| Lab checks | `commands/01_lab_health_checks.md` | Wazuh server, agent, services and network checks |
| Formal Execution and Discovery tests | `commands/02_formal_test_commands.md` | The six main ATT&CK test commands |
| Manual Discovery rules | `commands/03_manual_discovery.md` | Manual rule checks, validation and restart commands |
| AI Discovery | `commands/04_ai_discovery.md` | Python environment, API generation, hashes and deployment |
| Recon telemetry | `commands/05_recon_telemetry.md` | Windows Security log and Wazuh agent checks used for the Recon test |
| Manual Recon | `commands/06_manual_recon.md` | Manual Recon rule development, validation and formal scan |
| AI Recon | `commands/07_ai_recon.md` | AI Recon generation, validation, correction and formal tests |
| Time sync | `commands/08_time_sync.md` | Chrony and Windows time setup and offset checks |
| Evidence queries | `commands/09_evidence_queries.md` | Commands used to check Wazuh alerts, event IDs and MITRE mapping |
| Development and excluded tests | `commands/10_development_and_excluded.md` | Commands kept to show problems that were found and fixed |

## Labels used in the command files

- **FORMAL** - directly used for a final formal test.
- **VALIDATION** - used to check that the setup was working correctly.
- **DEVELOPMENT** - used while creating or fixing a rule/configuration.
- **EXCLUDED** - kept as evidence, but not used in the final statistics.
