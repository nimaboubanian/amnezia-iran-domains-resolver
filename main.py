import json
import socket
import sys
from datetime import datetime


def log_error(log_file, input_data, error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - Input: {input_data} - Error: {error_message}\n"
    with open(log_file, 'a') as f:
        f.write(log_entry)


def resolve_domain(domain, timeout=5, log_file='error_log.txt'):
    try:
        socket.setdefaulttimeout(timeout)
        ip = socket.gethostbyname(domain.strip())
        return ip
    except socket.gaierror:
        error_msg = f"Could not resolve hostname '{domain}'. Please check if it's correct."
        print(f"Error: {error_msg}")
        log_error(log_file, domain, error_msg)
        return ""
    except socket.timeout:
        error_msg = f"Timeout occurred while resolving '{domain}'. The server might be slow or unreachable."
        print(f"Error: {error_msg}")
        log_error(log_file, domain, error_msg)
        return ""
    except Exception as e:
        error_msg = f"Unexpected error occurred while resolving '{domain}': {str(e)}"
        print(f"Error: {error_msg}")
        log_error(log_file, domain, error_msg)
        return ""


def merge_results(old_file, new_file, output_file):
    try:
        with open(old_file, 'r') as f:
            old_data = json.load(f)
    except FileNotFoundError:
        old_data = []

    with open(new_file, 'r') as f:
        new_data = json.load(f)

    # Create a dictionary from old data for easy lookup and update
    result_dict = {item['hostname']: item for item in old_data}

    # Update with new data
    for item in new_data:
        result_dict[item['hostname']] = item

    # Convert back to list
    merged_data = list(result_dict.values())

    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=2)


def process_file(input_file, output_file, log_file='error_log.txt'):
    try:
        with open(input_file, 'r') as f:
            domains = f.readlines()

        if not domains:
            error_msg = f"The input file '{input_file}' is empty."
            print(f"Warning: {error_msg}")
            log_error(log_file, input_file, error_msg)
            return

        results = []
        for domain in domains:
            hostname = domain.strip()
            if not hostname:
                continue  # Skip empty lines

            ip = resolve_domain(hostname, log_file=log_file)
            result = {
                "hostname": hostname,
                "ip": ip
            }
            results.append(result)
            print(f"Processed: {hostname}")

        # Write new results to a temporary file
        with open('temp_results.json', 'w') as f:
            json.dump(results, f, indent=2)

        # Merge new results with old results
        merge_results('old_results.json', 'temp_results.json', output_file)

        print(f"Processing complete. Results have been saved to {output_file}")

    except FileNotFoundError as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        log_error(log_file, input_file, error_msg)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        print(f"Error: {error_msg}")
        log_error(log_file, "process_file", error_msg)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = 'error_log.txt'

    process_file(input_file, output_file, log_file)
    print(f"Any errors encountered have been logged to {log_file}")