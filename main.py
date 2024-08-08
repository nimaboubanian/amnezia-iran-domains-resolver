import json
import socket
import sys
import os
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


def process_file(input_file, output_file, log_file='error_log.txt'):
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found.")

        with open(input_file, 'r') as f:
            domains = f.readlines()

        if not domains:
            error_msg = f"The input file '{input_file}' is empty."
            print(f"Warning: {error_msg}")
            log_error(log_file, input_file, error_msg)
            return

        # Initialize the output file with an empty list
        try:
            with open(output_file, 'w') as f:
                json.dump([], f)
        except IOError as e:
            error_msg = f"Unable to write to output file '{output_file}'. Please check file permissions and disk space."
            print(f"Error: {error_msg}")
            log_error(log_file, output_file, error_msg)
            return

        for domain in domains:
            hostname = domain.strip()
            if not hostname:
                continue  # Skip empty lines

            ip = resolve_domain(hostname, log_file=log_file)
            result = {
                "hostname": hostname,
                "ip": ip
            }

            try:
                # Read the existing content
                with open(output_file, 'r') as f:
                    results = json.load(f)

                # Append the new result
                results.append(result)

                # Write the updated content back to the file
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=4)

                print(f"Processed: {hostname}")
            except json.JSONDecodeError:
                error_msg = f"The output file '{output_file}' contains invalid JSON. It will be reset."
                print(f"Error: {error_msg}")
                log_error(log_file, output_file, error_msg)
                with open(output_file, 'w') as f:
                    json.dump([result], f, indent=4)
            except IOError as e:
                error_msg = f"Unable to update output file '{output_file}'. Please check file permissions and disk space. The result for '{hostname}' could not be saved."
                print(f"Error: {error_msg}")
                log_error(log_file, output_file, error_msg)

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
        print("Usage: python script_name.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = 'error_log.txt'

    process_file(input_file, output_file, log_file)
    print(f"Processing complete. Results have been saved to {output_file}")
    print(f"Any errors encountered have been logged to {log_file}")
