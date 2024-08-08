# Amnezia Iran Domains Resolver

## Overview

The Amnezia Iran Domains Resolver is a tool designed to enhance the functionality of Amnezia VPN for users in Iran. It automatically fetches a list of Iranian domains, resolves them to their corresponding IP addresses, and formats the data for use with Amnezia VPN's split tunneling feature.

## Features

- Automatically fetches the latest list of Iranian domains from [bootmortis/iran-hosted-domains](https://github.com/bootmortis/iran-hosted-domains)
- Resolves domain names to IP addresses
- Generates a JSON file compatible with Amnezia VPN's split tunneling feature
- Runs daily via GitHub Actions to ensure up-to-date information
- Provides detailed error logs for troubleshooting

## How It Works

1. A GitHub Actions workflow runs daily at midnight UTC.
2. It fetches the latest `domains.txt` file from the [bootmortis/iran-hosted-domains](https://github.com/bootmortis/iran-hosted-domains) repository.
3. The Python script `domain_resolver.py` processes this file, resolving each domain to its IP address.
4. The script generates a `results.json` file containing the resolved domain-IP pairs.
5. A new release is created with the `results.json` and `error_log.txt` files as assets.

## Usage

### Accessing the Latest Results

1. Go to the [Releases](https://github.com/yourusername/amnezia-iran-domains-resolver/releases) page of this repository.
2. Download the `results.json` file from the latest release.
3. Import this file into your Amnezia VPN client for split tunneling configuration.

### Running the Script Locally

If you want to run the script on your local machine:

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/amnezia-iran-domains-resolver.git
   cd amnezia-iran-domains-resolver
   ```

2. Ensure you have Python 3.x installed.

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the script:
   ```
   python domain_resolver.py input_domains.txt output_results.json
   ```

5. Check the `output_results.json` for the results and `error_log.txt` for any errors.

## Project Structure

```
amnezia-iran-domains-resolver/
│
├── .github/
│   └── workflows/
│       └── update_and_release.yml
│
├── domain_resolver.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Contributing

Contributions to improve the project are welcome! Here's how you can contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the existing coding style.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Amnezia VPN](https://amnezia.org/) for their excellent VPN solution
- [bootmortis/iran-hosted-domains](https://github.com/bootmortis/iran-hosted-domains) for providing the list of Iranian domains
- All contributors who have helped to improve this project

## Disclaimer

This tool is provided for educational and informational purposes only. Please ensure you comply with all relevant laws and regulations when using VPNs or any other privacy-enhancing technologies.

## Contact

If you have any questions, feel free to open an issue or contact the repository owner.

---

Made with ❤️ for internet freedom and privacy
