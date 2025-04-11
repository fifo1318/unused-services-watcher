#!/usr/bin/env python3
import subprocess

def get_services():
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
        active = parts[2]
        sub = parts[3]

        if active != "active":
            unused.append((name, active, sub))

    return unused

def ask_action(service_name):
    print(f"\n❔ Čo chceš urobiť so službou `{service_name}`?")
    print("   [s] Stop (zastaviť)")
    print("   [d] Disable (zakázať)")
    print("   [n] Nič")
    choice = input("   Voľba (s/d/n): ").lower().strip()

    if choice == "s":
        subprocess.run(["sudo", "systemctl", "stop", service_name])
        print(f"⛔ Služba `{service_name}` bola zastavená.")
    elif choice == "d":
        subprocess.run(["sudo", "systemctl", "disable", service_name])
        print(f"🚫 Služba `{service_name}` bola zakázaná.")
    else:
        print("↩️ Preskočené.")

def main():
    print("🔍 Hľadám neaktívne alebo zakázané služby...\n")
    services = get_services()
    unused = analyze_services(services)

    if unused:
        print("🔻 Neaktívne alebo zakázané služby:")
        for name, active, sub in unused:
            print(f"  - {name} | Stav: {active} ({sub})")

        for name, _, _ in unused:
            ask_action(name)
    else:
        print("✅ Všetky služby sú aktívne.")

if __name__ == "__main__":
    main()
