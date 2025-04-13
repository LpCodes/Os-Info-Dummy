# System Information Tool

A powerful Python-based system information tool that provides detailed insights about your computer's hardware and software configuration.

## Features

- **System Information**
  - Operating system details
  - System architecture
  - Processor information
  - Node name and version

- **Hardware Monitoring**
  - CPU usage and frequency
  - Memory usage and statistics
  - GPU information (if available)
  - Temperature sensors
  - Battery status (for laptops)

- **Storage Information**
  - Detailed disk partition information
  - Total, used, and free space
  - File system types

- **Network Information**
  - Network interfaces
  - IP addresses
  - Netmasks
  - Broadcast addresses

- **Process Information**
  - Top 5 processes by CPU usage
  - Process details including PID and memory usage

- **Additional Features**
  - System uptime
  - Boot time
  - Color-coded output
  - JSON output option

## Installation

1. Clone this repository:
```bash
git clone https://github.com/LpCodes/Os-Info-Dummy.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- `psutil`: For system and process information
- `GPUtil`: For GPU information
- `colorama`: For colored terminal output
- `platform`: Built-in Python module
- `argparse`: Built-in Python module
- `json`: Built-in Python module
- `datetime`: Built-in Python module

## Usage

### Basic Usage
```bash
python app.py
```

### JSON Output
To get the output in JSON format:
```bash
python app.py --json
```

## Output Format

The tool provides information in the following sections:

1. **System Information**
   - Basic system details
   - Architecture
   - Processor information

2. **CPU and Memory**
   - CPU usage and frequency
   - Memory statistics
   - Memory usage percentage

3. **Disk Information**
   - Partition details
   - Space usage
   - File system types

4. **Network Information**
   - Interface details
   - IP configurations
   - Network masks

5. **Additional Information**
   - System uptime
   - GPU details
   - Temperature readings
   - Top processes

6. **Battery Information** (if available)
   - Battery percentage
   - Power source
   - Time remaining

## Error Handling

The tool includes comprehensive error handling:
- Graceful handling of missing hardware components
- Informative error messages
- Fallback options for unavailable information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.



## Acknowledgments

- Thanks to the developers of `psutil` and `GPUtil` for their excellent libraries
- Inspired by various system monitoring tools 
