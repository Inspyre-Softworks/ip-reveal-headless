
# IP-Reveal Headless

IP-Reveal Headless is a script designed to fetch and display the system's hostname, external IP address, and internal IP address. This can be useful for network diagnostics, logging, or any situation where knowing the IP addresses of a machine is necessary.

## Features

- Retrieve the system's hostname
- Retrieve the system's external IP address using the IPIFY service
- Retrieve the system's internal IP address

## Installation

### Regular Users

To install the package from PyPI, use:

```sh
pip install ip-reveal-headless
```

### Contributors

If you want to contribute to the development of this project, you should clone the repository and use Poetry for dependency management.

1. Clone the repository:

```sh
git clone https://github.com/Inspyre-Softworks/ip-reveal-headless.git
cd ip-reveal-headless
```

2. Install Poetry if you haven't already:

```sh
pip install poetry
```

3. Install dependencies and activate the virtual environment:

```sh
poetry install
poetry shell
```

## Usage

You can run the script with various subcommands to retrieve different pieces of information:

```sh
ip_reveal_headless.py [subcommand]
```

### Subcommands


| Command            | Description                                                            | Aliases                                                                        |
|--------------------|------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| get_public         | Retrieve the external IP address.                                      | get-external, external, public, ip, get-ip, internet, get-internet, get-public |
| get_host           | Retrieve the system's hostname.                                        | get-hostname, hostname, host, name, get-name                                   |
| get_local          | Retrieve the internal IP address.                                      | local, get-private, private, get-internal, internal, get-local                 |
| get_all            | Retrieve the hostname, internal IP, and external IP in one call.       | all, reveal, get-all                                                           |
| print-version-info | Print the version information of IP-Reveal-Headless in a pretty table. | version-info, version, print-version-table, print-version-info                 |

----<br>

## Examples

- To get the external IP address:

```sh
ip-reveal get_public
```

- To get the hostname:

```sh
ip-reveal get_host
```

- To get the internal IP address:

```sh
ip-reveal get_local
```

- To get all information:

```sh
ip-reveal get_all
```

## Configuration

The script uses a configuration file and parsed arguments which are imported from the `ip_reveal_headless.config` module. Ensure that your configuration file is set up correctly for your environment.

## Logging

The script uses a logging device specified in the configuration (`LOG_DEVICE`). It logs debug information about the process of retrieving IP addresses and hostnames. Ensure that your logging configuration is set up to capture these logs.

## Dependencies

- `requests`
- `urllib3`
- `socket`
- `platform`

## Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or a pull request.

## License

This project is licensed under the MIT License.
