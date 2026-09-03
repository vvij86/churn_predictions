Ticket Request: Provision Databricks ML Development Cluster for Mercer Churn Project

[Cluster Specifications]
- Cluster Type: All-Purpose (Interactive Development)
- Access Mode: Single User (Data Privacy Isolation Policy)
- Runtime: Databricks Runtime 18.0 LTS ML (or highest available 17.x LTS ML)
- Engine: Photon Acceleration Enabled
- Scaling: Enabled (Minimum 2 Workers / Maximum 8 Workers)
- Auto-Termination: 30 minutes of inactivity
- Instance Strategy: Spot Instances for Workers (to optimize cloud budget), On-Demand for Driver.
- Node Type Requirement: Memory-Optimized (Minimum 16GB RAM per core, r-family or equivalent).
