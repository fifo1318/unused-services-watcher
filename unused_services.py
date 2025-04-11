#!/usr/bin/env python3
import subprocess

def get_services():
    # Získaj všetky služby
    cmd = ["systemctl", "list-units", "--type=service", "--all", "--no-pager", "--no-legend"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip().split("\n")

def analyze_services(services):
    unused = []
    for line in services:
        parts = line.split()
        if len(parts) < 4:
            continue

        name = parts[0]
        load = parts[1]
        active = parts[2]
        sub = parts[3]

        # Podmienka: služba nie je aktívna
        if active != "active":
            unused.append((name, active, sub))

    return unused

def main():
    print("🔍 Hľadám nepoužívané alebo neaktívne služby...\n")
    services = get_services()
    unused = analyze_services(services)

    if unused:
        print("🔻 Neaktívne alebo zakázané služby:")
        for name, active, sub in unused:
            print(f"  - {name} | Stav: {active} ({sub})")
    else:
        print("✅ Všetky služby sú aktívne.")

if __name__ == "__main__":
    main()
