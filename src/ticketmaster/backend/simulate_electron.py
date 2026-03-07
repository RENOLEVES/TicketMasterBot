#!/usr/bin/env python3
import subprocess
import json
import sys
import os
import time
import threading

EXE_PATH = r"dist\task.exe"
CONFIG = {
    "url":      "https://www.ticketmaster.ca/twice-this-is-for-world-tour-hamilton-ontario-03-07-2026/event/1000633AAE9457A3",
    "email":    "zzhao260985652@gmail.com",
    "minPrice": "",
    "maxPrice": "",
    "tickType": "any",
    "interval": 9999
}

def main():
    exe = os.path.abspath(EXE_PATH)
    if not os.path.exists(exe):
        print(f"[ERR] task.exe not found at: {exe}")
        print(f"      Current dir: {os.getcwd()}")
        print(f"      Files here:  {os.listdir('dist') if os.path.exists('dist') else 'no dist folder'}")
        sys.exit(1)

    config_json = json.dumps(CONFIG)
    print(f"[SIM] Launching: {exe}")
    print(f"[SIM] Args:      {config_json[:80]}...")
    print(f"[SIM] {'─'*55}")

    proc = subprocess.Popen(
        [exe, config_json],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    def read_stdout():
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                t    = msg.get("type", "?")
                text = msg.get("text", "")
                lvl  = msg.get("level", "info")

                color = {"info": "", "warn": "\033[93m", "error": "\033[91m",
                         "success": "\033[92m"}.get(lvl, "")
                reset = "\033[0m" if color else ""

                if t == "log":
                    print(f"  {color}[LOG/{lvl.upper()}]{reset} {text}")
                elif t == "check_done":
                    print(f"  \033[96m[CHECK]{reset} total={msg.get('total',0)}  new_matches={msg.get('count',0)}")
                elif t == "ticket":
                    tk = msg.get("ticket", {})
                    print(f"  \033[92m[TICKET]{reset} ${tk.get('price','?')}  {tk.get('description','')}  [{tk.get('branding','')}]")
                elif t == "email_sent":
                    print(f"  \033[92m[EMAIL]{reset} sent to {msg.get('to','')}")
                elif t == "error":
                    print(f"  \033[91m[ERROR]{reset} {msg.get('text','')}")
                elif t == "stopped":
                    print(f"  [STOPPED] exit code={msg.get('code','?')}")
                else:
                    print(f"  [MSG/{t}] {line}")
            except json.JSONDecodeError:
                print(f"  [RAW] {line}")

    def read_stderr():
        for line in proc.stderr:
            line = line.strip()
            if line:
                print(f"  \033[91m[STDERR]{reset_} {line}", flush=True)
    reset_ = "\033[0m"

    t1 = threading.Thread(target=read_stdout, daemon=True)
    t2 = threading.Thread(target=read_stderr, daemon=True)
    t1.start()
    t2.start()

    try:
        print("[SIM] Running… press Ctrl+C to stop\n")
        proc.wait()
    except KeyboardInterrupt:
        print("\n[SIM] Interrupted — killing process")
        proc.kill()

    t1.join(timeout=2)
    t2.join(timeout=2)
    print(f"\n[SIM] Process exited with code: {proc.returncode}")


if __name__ == "__main__":
    main()