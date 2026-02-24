import subprocess

BINARY = "./program"
WORDLIST = "random.dic"

def run_with_argument(password):
    try:
        result = subprocess.run(
            [BINARY, password],
            capture_output=True,
            timeout=3
        )
        return result.stdout.decode(errors="ignore")
    except:
        return ""

def run_with_stdin(password):
    try:
        result = subprocess.run(
            [BINARY],
            input=password.encode(),
            capture_output=True,
            timeout=3
        )
        return result.stdout.decode(errors="ignore")
    except:
        return ""

def is_success(output):
    success_indicators = [
        "correct",
        "success",
        "flag",
        "access granted",
        "welcome"
    ]

    for indicator in success_indicators:
        if indicator.lower() in output.lower():
            return True

    return False


def brute_force():
    with open(WORDLIST, "r", errors="ignore") as f:
        for count, password in enumerate(f):
            password = password.strip()

            print(f"[{count+1}] Trying: {password}")

            # Try as argument
            output = run_with_argument(password)
            if is_success(output):
                print(f"\n✅ PASSWORD FOUND (argument): {password}")
                print("Output:\n", output)
                return

            # Try via stdin
            output = run_with_stdin(password)
            if is_success(output):
                print(f"\n✅ PASSWORD FOUND (stdin): {password}")
                print("Output:\n", output)
                return

    print("\n❌ Password not found in wordlist")


if __name__ == "__main__":
    brute_force()
