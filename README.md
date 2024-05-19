# Load Balancing base on throughput using Mininet and Ryu Controller

## Project Team

❤️ Thank you for the contributions of all the members ❤️



| **Name**          | **Role**                | **Contact**              |
|-------------------|-------------------------|--------------------------|
| ![Member1](https://via.placeholder.com/30) **Member 1** | Project Leader          | [member1@example.com](mailto:member1@example.com) |
| ![Member2](https://via.placeholder.com/30) **Member 2** | Developer               | [member2@example.com](mailto:member2@example.com) |
| ![Member3](https://via.placeholder.com/30) **Member 3** | Network Specialist      | [member3@example.com](mailto:member3@example.com) |
| ![Member4](https://via.placeholder.com/30) **Member 4** | Tester                  | [member4@example.com](mailto:member4@example.com) |

---

## Overview

This project implements a Load Balancing solution using Mininet and Ryu Controller. The aim is to simulate a network environment where traffic is distributed efficiently across multiple servers.

## Directory Structure

- **lb_core**: Contains the core load balancing logic and implementation.
- **mininet**: Includes scripts and configurations for setting up the Mininet environment.
- **result**: Stores the results and logs generated from running the simulations.
- **tb**: (Provide a brief description of what this directory contains, e.g., testing and benchmarking scripts).

## Prerequisites

- Python 3.x
- Mininet
- Ryu Controller
- Other dependencies listed in `requirements.txt` (if you have one)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Mininet and Ryu Controller following their respective installation guides:
    - [Mininet Installation Guide](http://mininet.org/download/)
    - [Ryu Controller Installation Guide](https://osrg.github.io/ryu/)

## Usage

### Starting the Mininet Topology

1. Navigate to the `mininet` directory:
    ```bash
    cd mininet
    ```

2. Run the Mininet topology script:
    ```bash
    sudo python your_topology_script.py
    ```

### Running the Ryu Controller

1. Navigate to the `lb_core` directory:
    ```bash
    cd ../lb_core
    ```

2. Start the Ryu Controller with the load balancing application:
    ```bash
    ryu-manager your_lb_app.py
    ```

### Generating Traffic and Viewing Results

1. Once Mininet and Ryu Controller are running, you can start generating traffic to test the load balancing.
2. Scripts or commands to generate traffic should be located in the `tb` directory or described here.
3. View the results in the `result` directory after the simulation.

## Results

Results of the simulations, including logs and performance metrics, are stored in the `result` directory. Detailed analysis of the results can be found in the result files.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Mininet Team for the network emulation tool.
- Ryu SDN Framework for providing the controller.
- Any other acknowledgements...

## Contact

For any questions or inquiries, please contact [your email or contact information].
