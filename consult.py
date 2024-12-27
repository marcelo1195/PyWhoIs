import socket
import re
import argparse


def validate_domain(domain):
    """Validate if the domain has a valid format."""
    domain_regex = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.([A-Za-z]{2,63}(\.[A-Za-z]{2,63})?)$"
    return re.match(domain_regex, domain)


def get_whois_iana(domain, *args, **kwargs):
    """Query the IANA WHOIS server directly using a socket connection."""
    try:
        with socket.create_connection(("whois.iana.org", 43), timeout=kwargs.get("timeout", 10)) as s:
            s.sendall((domain + "\r\n").encode("utf-8"))
            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data
        return response.decode("utf-8", errors="ignore")
    except socket.error as e:
        print(f"Error connecting to the IANA WHOIS server: {e}")
        return None


def parse_iana_response(response, *args, **kwargs):
    """Extract the TLD WHOIS server from the IANA response."""
    match = re.search(r"whois:\s+([\w\.\-]+)", response)
    if match:
        return match.group(1)
    return None


def query_whois_server(domain, whois_server, *args, **kwargs):
    """Query the specified WHOIS server using a socket connection."""
    try:
        with socket.create_connection((whois_server, 43), timeout=kwargs.get("timeout", 10)) as conn:
            conn.sendall(f"{domain}\r\n".encode("utf-8"))
            response = b""
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                response += data
            return response.decode("utf-8", errors="ignore")
    except socket.error as e:
        print(f"Error connecting to the WHOIS server {whois_server}: {e}")
        return None


def main(*args, **kwargs):
    """Main function to handle WHOIS queries."""
    # Argument parser for command-line usage
    parser = argparse.ArgumentParser(description="WHOIS Query Tool")
    parser.add_argument("domain", help="Domain name to query (e.g., example.com)")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout for connections (default: 10s)")
    parsed_args = parser.parse_args(*args)

    domain = parsed_args.domain
    timeout = parsed_args.timeout

    if not validate_domain(domain):
        print("Invalid domain. Ensure the format is like example.com.")
        return

    print("\nQuerying IANA to retrieve the WHOIS server...")
    iana_response = get_whois_iana(domain, timeout=timeout)
    if not iana_response:
        print("Failed to get a response from the IANA WHOIS server.")
        return

    whois_server = parse_iana_response(iana_response)
    if not whois_server:
        print("WHOIS server not found in the IANA response.")
        return

    print(f"WHOIS server found: {whois_server}")
    print(f"Querying {whois_server} for detailed information...\n")
    whois_data = query_whois_server(domain, whois_server, timeout=timeout)

    if whois_data:
        print("IANA Query Result:")
        print(iana_response)
        print("WHOIS Query Result:")
        print(whois_data)
    else:
        print("Failed to retrieve information from the WHOIS server.")


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
