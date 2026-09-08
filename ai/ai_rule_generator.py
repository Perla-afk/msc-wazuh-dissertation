from openai import OpenAI
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import time
import sys

BASE = Path.home() / "ai_wazuh"
PROMPT_FILE = BASE / "prompts" / "rule_generation_prompt.txt"
EVIDENCE_FILE = BASE / "evidence" / "baseline_gaps.json"
OUTPUT_DIR = BASE / "outputs"
MODEL = "gpt-5.6-terra"

def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_xml(text):
    fenced = re.search(r"```xml\s*(.*?)```", text, re.IGNORECASE | re.DOTALL)
    if fenced:
        return fenced.group(1).strip()
    group = re.search(r"(<group\b.*?</group>)", text, re.IGNORECASE | re.DOTALL)
    if group:
        return group.group(1).strip()
    return None

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")
    evidence = EVIDENCE_FILE.read_text(encoding="utf-8")
    final_prompt = prompt_template.replace("{BASELINE_EVIDENCE}", evidence)
    run_time = datetime.now(timezone.utc)
    run_id = run_time.strftime("AI-GEN-%Y%m%d-%H%M%S")
    print("=== AI-ASSISTED WAZUH RULE GENERATION ===")
    print("Run ID:", run_id)
    print("Model requested:", MODEL)
    print("Prompt SHA-256:", sha256_text(final_prompt))
    print()
    print("WARNING: This is the first formal AI rule-generation request.")
    print("The complete raw output will be saved without modification.")
    print()
    confirmation = input("Type GENERATE to make the API request: ")
    if confirmation != "GENERATE":
        print("Generation cancelled. No API request sent.")
        sys.exit(0)
    client = OpenAI()
    start = time.perf_counter()
    response = client.responses.create(model=MODEL, input=final_prompt)
    duration = time.perf_counter() - start
    raw_response = response.output_text
    xml = extract_xml(raw_response)
    raw_file = OUTPUT_DIR / f"{run_id}_raw_response.txt"
    prompt_file = OUTPUT_DIR / f"{run_id}_exact_prompt.txt"
    xml_file = OUTPUT_DIR / f"{run_id}_generated_rules.xml"
    metadata_file = OUTPUT_DIR / f"{run_id}_metadata.json"
    raw_file.write_text(raw_response, encoding="utf-8")
    prompt_file.write_text(final_prompt, encoding="utf-8")
    if xml:
        xml_file.write_text(xml + "\n", encoding="utf-8")
    metadata = {
        "run_id": run_id,
        "timestamp_utc": run_time.isoformat(),
        "requested_model": MODEL,
        "returned_model": response.model,
        "response_id": response.id,
        "request_duration_seconds": round(duration, 3),
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.total_tokens,
        "prompt_sha256": sha256_text(final_prompt),
        "raw_response_sha256": sha256_text(raw_response),
        "xml_extracted": xml is not None,
        "xml_sha256": sha256_text(xml) if xml else None,
        "human_corrections_before_generation": 0
    }
    metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print()
    print("=== GENERATION COMPLETE ===")
    print("Returned model:", response.model)
    print("Response ID:", response.id)
    print("Request duration:", round(duration, 3), "seconds")
    print("Input tokens:", response.usage.input_tokens)
    print("Output tokens:", response.usage.output_tokens)
    print("Total tokens:", response.usage.total_tokens)
    print("XML extracted:", "YES" if xml else "NO")
    print()
    print("Raw response:", raw_file)
    print("Exact prompt:", prompt_file)
    if xml:
        print("Generated XML:", xml_file)
    print("Metadata:", metadata_file)
    print()
    print("IMPORTANT: The generated XML has NOT been installed or modified.")

if __name__ == "__main__":
    main()
