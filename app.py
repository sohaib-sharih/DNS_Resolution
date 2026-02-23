import dns.query
import dns.message
import dns.resolver

# 1. ROOT SERVER ADDRESS (One of the 13, e.g., 'a.root-servers.net')
ROOT_SERVER = '198.41.0.4' 

def simulate_dns_lookup(domain):
    print(f"--- Starting DNS Lookup for: {domain} ---\n")

    # STEP 1: Simulate Browser & OS Cache Check
    # In reality, the OS and Browser handle this. We simulate a "Cache Miss".
    print("[1] Browser & OS: Checking local cache... No record found.")
    print("[2] Browser: Requesting OS to fetch IP from DNS Resolver (ISP).")

    # STEP 2: The Resolver's Journey (Mimicking your ISP)
    print(f"[3] Resolver: Cache miss at ISP. Contacting Root Server at {ROOT_SERVER}...")
    
    # Query Root for TLD (e.g., .com)
    query = dns.message.make_query(domain, dns.rdatatype.A)
    response = dns.query.udp(query, ROOT_SERVER)
    
    # Root provides TLD servers (Authority section)
    tld_server_ip = response.additional[0][0].address
    print(f"[4] Root Server: 'I don't know {domain}, but here is the .com TLD server IP: {tld_server_ip}'")

    # STEP 3: Contact TLD Server
    print(f"[5] Resolver: Contacting TLD Server at {tld_server_ip}...")
    response = dns.query.udp(query, tld_server_ip)
    
    # TLD provides Authoritative Name Servers
    auth_ns_ip = None
    # We look for the IP of the authoritative server in the additional section
    for rrset in response.additional:
        if rrset.rdtype == dns.rdatatype.A:
            auth_ns_ip = rrset[0].address
            break
            
    print(f"[6] TLD Server: 'I found the authoritative servers for this domain. Go ask: {auth_ns_ip}'")

    # STEP 4: Final Authoritative Lookup
    print(f"[7] Resolver: Contacting Authoritative Server at {auth_ns_ip}...")
    response = dns.query.udp(query, auth_ns_ip)
    
    # Final IP Address
    final_ip = response.answer[0][0].address
    print(f"\n[SUCCESS] Authoritative Server: 'The IP for {domain} is {final_ip}'")
    print(f"[8] Resolver: Returning IP to OS, which saves it to cache and gives it to Browser.")
    print(f"[9] Browser: Connecting to {final_ip} to load your website.")

if __name__ == "__main__":
    simulate_dns_lookup("hunarmund.com")