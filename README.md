# Transparency Study using Spade & Spade BDI

This repository is a basic setup to get started with a modified spade environment.


## Getting Started

- Install Requirements: Navigate into the repository and install the requirements using `pip install -r requirements.txt`.
- This codebase was intended to be used along with the transparency tool (see: https://github.com/fahidRM/agent-transparency-tool).
- Firstly, launch and start the transparency tool then run your MAS.
- Included in this repository are two examples, these are `counter.py` and `counter_bdi.asl.py`. These files can be run using the commands: `python3 counter.py` and `counter_bdi.asl.py` respectively.


## Using the Transparency tool with your own project

- Create your project files in / copy your existing project files to the root directory.
- Install the necessary requirements for your project excluding `agentspeak`, `spade` and `spade-bdi`.
- Launch and start the transparency tool (see: https://github.com/fahidRM/agent-transparency-tool).
- Update your code to import the logger using the statement `from stag_logger.Logger import WebLogger` then initialise the logger using the code: `WebLogger(mas_name="Counter BDI MAS", server="localhost", port=3700)`. This would post logs to the address `http://localhost:3700` which is the address/port that the transparency tool listens on. NOTE: This must be done before declaring the agents.
- Run your project as you normally would.

- A sample video demonstrating the setup is available here:  https://fahidrm.github.io/agent-transparency-tool/files/guides/agent_transparency_tool_with_spade.mp4




__NOTE: Please note this repository contains modified versions of `agentspeak`, `spade` and `spade-bdi` packages that are necessary for capturing the required logs.__


