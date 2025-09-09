import socket
import dns.resolver
import os

DOMAIN = "example.com"
OUTPUT_FILE = "dns_results.txt"

try:
    results = []

    # 1. Resolve IP address
    ip_address = socket.gethostbyname(DOMAIN)
    line = f"IP address of {DOMAIN}: {ip_address}"
    print(line)
    results.append(line)

    # 2. Retrieve A, MX, and CNAME records
    for record_type in ["A", "MX", "CNAME"]:
        try:
            answers = dns.resolver.resolve(DOMAIN, record_type)
            for rdata in answers:
                line = f"{record_type} record: {rdata}"
                print(line)
                results.append(line)
        except Exception as e:
            line = f"{record_type} record lookup failed: {e}"
            print(line)
            results.append(line)

    # 3. Log results to file
    with open(OUTPUT_FILE, "w") as f:
        for line in results:
            f.write(line + "\n")

    print("\n✅ DNS query completed.")
    print("Results saved at:", os.path.abspath(OUTPUT_FILE))

except Exception as e:
    print("❌ Error:", e)
