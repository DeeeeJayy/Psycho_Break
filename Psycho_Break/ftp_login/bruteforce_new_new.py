import subprocess

BINARY = "./program"
WORDLIST = "random.dic"

def brute_force():
    with open(WORDLIST, "r", errors="ignore") as f:
        for count, password in enumerate(f):
            password = password.strip()

            print(f"[{count+1}] Trying: {password}")

            try:
                result = subprocess.run(
                    [BINARY, password],
                    capture_output=True,
                    timeout=2
                )

                output = result.stdout.decode(errors="ignore")

                # If it's not "Incorrect", we likely found it
                if "Incorrect" not in output:
                    print("\n✅ PASSWORD FOUND:", password)
                    print("Program Output:\n", output)
                    return

            except subprocess.TimeoutExpired:
                print("Timeout, skipping...")
                continue

    print("\n❌ Password not found in wordlist")

if __name__ == "__main__":
    brute_force()
