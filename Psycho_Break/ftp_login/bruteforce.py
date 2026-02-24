import subprocess
import os

ENCRYPTED_FILE = "program"
WORDLIST = "random.dic"
OUTPUT_FILE = "decrypted_output"

def looks_like_script(data):
    text = data.decode(errors="ignore")

    if text.startswith("#!/bin/bash"):
        return "bash"
    if text.startswith("#!/usr/bin/env python") or text.startswith("#!/usr/bin/python"):
        return "python"
    if "import " in text or "echo " in text:
        return "possible_script"

    return None


def syntax_check(script_type, filepath):
    try:
        if script_type == "bash":
            result = subprocess.run(["bash", "-n", filepath],
                                    capture_output=True)
            return result.returncode == 0

        if script_type == "python":
            result = subprocess.run(["python3", "-m", "py_compile", filepath],
                                    capture_output=True)
            return result.returncode == 0

        return False
    except:
        return False


def try_password(password):
    try:
        result = subprocess.run(
            [
                "openssl", "enc", "-aes-256-cbc",
                "-d",
                "-in", ENCRYPTED_FILE,
                "-out", OUTPUT_FILE,
                "-pass", f"pass:{password}"
            ],
            capture_output=True
        )

        if result.returncode != 0:
            return False

        with open(OUTPUT_FILE, "rb") as f:
            data = f.read()

        script_type = looks_like_script(data)
        if not script_type:
            return False

        if syntax_check(script_type, OUTPUT_FILE):
            print(f"\n✅ Password Found: {password}")
            print(f"Detected script type: {script_type}")
            return True

        return False

    except:
        return False


def brute_force():
    with open(WORDLIST, "r", encoding="utf-8", errors="ignore") as f:
        for count, line in enumerate(f):
            password = line.strip()
            print(f"Trying {count+1}: {password}")

            if try_password(password):
                print("Decrypted file saved as:", OUTPUT_FILE)
                return

    print("\n❌ Password not found in wordlist")


if __name__ == "__main__":
    brute_force()
