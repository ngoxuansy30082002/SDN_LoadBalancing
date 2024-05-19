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

    2.1. If you want automated performance testing with the iperf3:
    ```bash
    sudo python3 auto_iperf.py
    ```
    2.2. If you want to test performance manually with your own tool:
    ```bash
    sudo python3 manual_test.py
    ```

### Scenario 2: Without Load Balancing

#### Running the Ryu Controller without Load Balancing

1. Navigate to the `lb_core` directory:
    ```bash
    cd lb_core
    ```

2. Start the Ryu Controller without the load balancing application:
    ```bash
    ryu-manager no_lb_final.py
    ```

#### Starting the Mininet Topology

1. Navigate to the `mininet` directory:
    ```bash
    cd ../mininet
    ```

2. Run the Mininet topology script:
    
    2.1. If you want automated performance testing with the iperf3:
    ```bash
    sudo python3 auto_iperf.py
    ```
    2.2. If you want to test performance manually with your own tool:
    ```bash
    sudo python3 manual_test.py
    ```

### Generating Traffic and Viewing Results

1. Once Mininet and Ryu Controller are running, you can start generating traffic to test the scenarios.
2. Our sample traffic generation scripts are located in the `tb` directory.
3. Simulation results are saved in the `result` directory.
4. Instructions for generating http traffic:

    4.1. In mininet environment:
    ```bash
    xterm h1 h2 h3 h4 h5 h6 h7
    ```
    4.2. In h1,h2,h3's command window:
    ```bash
    python3 SDN_LoadBalancing/tb/tb_http/sv.py
    ```
    4.3. In h4,h5,h6,h7's command window:
     ```bash
    python3 SDN_LoadBalancing/tb/tb_http/cl.py
    ```

## Results

Results of the simulations, including logs and performance metrics, performance chart are stored in the `result` directory. Detailed analysis of the results can be found in the result files.

## Contact

For any questions or inquiries, please contact [ngoxuansy30082002@gmail.com](mailto:ngoxuansy30082002@gmail.com).
