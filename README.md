# Load Balancing base on throughput using Mininet and Ryu Controller

## Project Team

❤️ Thank you for the contributions of all the members ❤️



| **Name**              | **Class**               | **StudentCode**          |
|-------------------    |-------------------------|--------------------------|
| **Trần Hồng Khải**    | 20KTMT1                 | 106200231                |
| **Ngô Xuân Sỹ**       | 20KTMT1                 | 106200244                |
| **Trần Đình Thi**     | 20KTKT1                 | 106200246                |
| **Nguyễn Đức Hoàng**  | 20KTMT1                 | 106200261                |

---

## Overview

This project implements a Load Balancing solution using Mininet and Ryu Controller. The aim is to simulate a network environment where traffic is distributed efficiently across multiple servers.

## Directory Structure

- **lb_core**: Contains the core load balancing logic and implementation.
- **mininet**: Includes scripts and configurations for setting up the Mininet environment.
- **result**: Stores the results and logs generated from running the simulations.
- **tb**: Testing and benchmarking scripts.

## Prerequisites

- Python 3.x
- Mininet
- Ryu Controller
- Linux Ubuntu 22.04LTS

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ngoxuansy30082002/SDN_LoadBalancing.git
    cd SDN_LoadBalancing
    ```

2. Set up Mininet and Ryu Controller following their respective installation guides:
    - [Mininet Installation Guide](http://mininet.org/download/)
    - [Ryu Controller Installation Guide](https://ryu.readthedocs.io/en/latest/getting_started.html)
## Usage

### Scenario 1: With Load Balancing

#### Running the Ryu Controller with Load Balancing

1. Navigate to the `lb_core` directory:
    ```bash
    cd lb_core
    ```

2. Start the Ryu Controller with the load balancing application:
    ```bash
    ryu-manager lb_final.py
    ```

#### Starting the Mininet Topology

1. Navigate to the `mininet` directory:
    ```bash
    cd ../mininet
    ```

2. Run the Mininet topology script:
    2.1 If you want automated performance testing with the iperf3:
    ```bash
    sudo python3 auto_iperf.py
    ```
    2.2 If you want to test performance manually with your own tool:
    ```bash
    sudo python3 manual_test.py
    ```

### Scenario 2: Without Load Balancing

#### Starting the Mininet Topology

1. Navigate to the `mininet` directory:
    ```bash
    cd mininet
    ```

2. Run the Mininet topology script:
    ```bash
    sudo python your_topology_script_without_lb.py
    ```

#### Running the Ryu Controller without Load Balancing

1. Navigate to the `lb_core` directory:
    ```bash
    cd ../lb_core
    ```

2. Start the Ryu Controller without the load balancing application:
    ```bash
    ryu-manager your_non_lb_app.py
    ```

### Generating Traffic and Viewing Results

1. Once Mininet and Ryu Controller are running, you can start generating traffic to test the scenarios.
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
