### Project Title: Secure Nearest Neighbor Computation Using MP-SPDZ

### Description
This project demonstrates a secure multi-party computation (MPC) protocol for finding the nearest neighbor among multiple parties using the MP-SPDZ framework. The protocol is designed to calculate the Euclidean distance between an individual in need and each of the other participants, securely determine the closest individual, and then reveal the coordinates of the individual in need to this closest party.

### Features
- *Secure Distance Calculation*: Computes the squared Euclidean distances between an initiator and multiple participants using secure fixed-point arithmetic.
- *Privacy-Preserving Nearest Neighbor*: Determines the closest participant without revealing any intermediate distances or coordinates to any party other than the intended recipient.
- *Scalable Multi-Party Setup*: Configured to work with multiple parties, ensuring flexibility and scalability.

### Prerequisites
- *MP-SPDZ Framework*: Ensure MP-SPDZ is installed and configured on your system. Follow the installation instructions from the [MP-SPDZ GitHub repository](https://github.com/data61/MP-SPDZ).
- *Linux Environment*: The project is designed to run on a Linux system.

### How to Run
1. *Compile the Script*:
   sh
   ./compile.py -R 64 find_closest_individual
   
2. *Run the Compiled Script*:
   sh
   for i in {0..5}; do
       ./mascot-party.x $i find_closest_individual -pn 12171 -h localhost -N 6 &
   done
   wait
   

### Project Structure
- *find_closest_individual.mpc*: The main MPC script that performs secure nearest neighbor computation.
- *Compile and Run Instructions*: Detailed steps to compile and run the script in an MP-SPDZ environment.
- *Documentation*: Additional documentation on the protocol, including the theoretical background and security considerations.

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements or bug fixes. Ensure your code follows the project’s coding standards and includes appropriate tests.

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments
Special thanks to the developers of the MP-SPDZ framework for providing an excellent tool for secure multi-party computation.

---

This brief explanation provides a high-level overview of the project, including its purpose, features, prerequisites, usage instructions, and how to contribute. It is suitable for inclusion in a GitHub repository to help users understand the project and get started quickly.
