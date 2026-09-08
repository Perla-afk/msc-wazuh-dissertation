#!/usr/bin/env bash
set -u
hostname && hostname -I
sudo systemctl is-active wazuh-manager
sudo /var/ossec/bin/agent_control -i 001
sudo /var/ossec/bin/agent_control -i 001 | grep -E 'Status|Last keep alive|Configuration hash|Shared file hash'
timedatectl
date '+%Y-%m-%d %H:%M:%S.%3N %Z %z'
