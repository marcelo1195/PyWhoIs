# WHOIS Query Tool

## Overview

The `whois_query_tool.py` script is a component of a broader suite of scripts designed for **information gathering**. This tool specializes in performing WHOIS lookups for domain names, enabling users to retrieve detailed domain registration information. The script is written in Python and can function as both a standalone application and a module integrated into other projects.

## Features

- **Domain Validation**: Ensures that the input domain is in a valid format, supporting generic TLDs (e.g., `.com`) and second-level TLDs (e.g., `.com.br`).
- **IANA WHOIS Query**: Connects directly to the IANA WHOIS server to determine the authoritative WHOIS server for the queried domain.
- **WHOIS Query Execution**: Retrieves detailed WHOIS data from the authoritative WHOIS server.
- **Timeout Configuration**: Customizable timeout for socket connections to handle varying network conditions.
- **CLI Integration**: Accepts command-line arguments for flexible and efficient usage.
- **Modular Design**: Can be imported and utilized as a module in larger information-gathering frameworks.

## Dependencies

- Python 3.x
- Standard Python libraries:
  - `socket`
  - `re`
  - `argparse`

## Installation

1. Clone the repository or download the `whois_query_tool.py` file.
2. Ensure you have Python 3.x installed on your system.
3. No additional libraries are required, as the script relies on Python’s standard libraries.

## Usage

### Standalone

Run the script from the command line:

```bash
python whois_query_tool.py <domain> [--timeout <seconds>]
```

#### Examples:

1. Query a domain with default timeout:
   ```bash
   python whois_query_tool.py example.com
   ```

2. Query a domain with a custom timeout:
   ```bash
   python whois_query_tool.py example.com --timeout 15
   ```

### As a Module

The script can be imported and used as a component in larger projects:

```python
from whois_query_tool import get_whois_iana, query_whois_server, validate_domain

# Validate domain
if validate_domain("example.com"):
    # Query IANA for authoritative WHOIS server
    iana_response = get_whois_iana("example.com")
    print(iana_response)
```

## Script Structure

### Functions

1. **`validate_domain(domain)`**
   - Validates the format of the provided domain name.
   - Supports both generic and second-level TLDs (e.g., `.com.br`).

2. **`get_whois_iana(domain, *args, **kwargs)`**
   - Connects to the IANA WHOIS server to determine the authoritative WHOIS server for the given domain.

3. **`parse_iana_response(response, *args, **kwargs)`**
   - Parses the response from IANA to extract the authoritative WHOIS server.

4. **`query_whois_server(domain, whois_server, *args, **kwargs)`**
   - Queries the specified WHOIS server to retrieve detailed WHOIS information.

5. **`main(*args, **kwargs)`**
   - Handles command-line arguments and orchestrates the WHOIS query process.

### Command-Line Arguments

- `<domain>`: The domain name to query.
- `--timeout <seconds>`: Optional. Specifies the timeout for socket connections (default: 10 seconds).

## Error Handling

The script includes robust error handling for:
- Invalid domain formats.
- Network issues (e.g., timeouts, connection errors).
- Missing WHOIS servers in IANA responses.

## Limitations

- Does not parse or format the WHOIS response into specific fields (e.g., registrar, expiration date). Users must manually interpret the raw response.
- Does not cache results; repeated queries for the same domain will re-fetch data.

## Future Enhancements

- Add parsing of WHOIS responses into structured formats (e.g., JSON).
- Implement caching to optimize repeated queries.
- Expand support for querying IP addresses in addition to domain names.
- Integrate into a larger framework for automated information gathering.

## License

This script is provided "as-is" without warranty of any kind. You are free to modify and use it as part of your projects.

