# PA-H Framework Replication Package

This repository provides the source code (Python implementation) of the PA-H framework and data used to evaluate the RM-H Supervisor, which is the implementation of the new PA-H  metascheduler, utilizing the Rate Monotonic (RM) priority assignment rule.  This is a support to the paper "Optimal processor management for priority driven schedulers with energy harvesting" by M. CHETTO, for the Computer Journal. 

## Core Components

*  PAH_Supervisor.py: The main meta-scheduler logic. It implements the novel concepts of Slack Time and Preemption Slack Energy using the formulas defined in Equations 2, 3, 4, and 5 of the paper. It is the meta-scheduling logic that is called at every scheduling event. Outputs are 1) A true/false signal for busy/idle decision and 2)  the values of slack time and slack Energy.

*  RM_Scheduler.py: A baseline Rate Monotonic dispatcher. It manages the ready queue based on task periods and executes tasks ASAP, disregarding energy levels or forecasts.

*  PFPasap_Scheduler.py: An implementation of the Fixed Priority As-Soon-As-Possible algorithm, which executes tasks immediately until energy depletion occurs.

*  Energy_Harvester_Model.py: It simulates a constant energy harvesting rate P_p based on the Replenishment Ratio (ρ). 

*  Energy_Storage_Unit.py: Models battery behavior, including capacity limits (C) and the lower-bound threshold (E_{min}). This module manages the battery state. It handles charging (from the harvester) and discharging (from job execution) while enforcing physical limits​.

## Task Set Generation
We use synthetic task sets that adhere to the hypotheses described in the experimental setup of the paper:
*  Task_Generator.py: Implements the UUnifast algorithm to generate task utilizations for a total utilization factor of U = 0.6.

*   Job_Set_Builder.py: Converts periodic tasks into specific job instances $(r_i, C_i, E_i, d_i)$. This script expands the periodic tasks into a list of specific Job instances that occur during the simulation horizon Tsim​.

## Execution and Experiments
Scripts designed to automate the 1,000 simulations per configuration as detailed in the paper:
*  Run_Experiments.py: The script  iterates through varying values of (ρ) (1.0, 1.2, 1.4) and different battery capacities.

*   Data_Collector.py: Records experimental outputs, specifically the Deadline Success Ratio (DSR) and the Minimum Storage Capacity (Cmin). This script serves as the interface between the raw simulation results and the final analysis. Its primary job is to take the list of DSR values from the 1,000 runs and compute the statistical metrics required.

## Analysis & Visualization
*   Plot_Results.py:  It  generates the Feasibility Surface and comparative DSR curves.
*   Statistical_Analysis.py: It calculates the 95% confidence intervals presented in Figures 5 and 6 of the paper.

## Contact
For questions regarding the mathematical proofs, please refer to the paper of the Computer Journal.

## License
This project is licensed under the MIT License for open academic collaboration while ensuring that the original authors are credited.

