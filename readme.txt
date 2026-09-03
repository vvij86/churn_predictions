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



To help you populate your infrastructure ticket precisely, here is the complete menu of standard configurations available within the Databricks cluster provisioning interface.
------------------------------
## 1. Cluster Type (Compute Options)
Databricks offers three primary architecture styles depending on your workload automation and budget limits:

* All-Purpose Compute (Interactive): Used for exploratory analysis in notebooks. Multiple data scientists can share it, or it can be locked to one person. It features auto-termination rules.
* Job Compute (Workflows): Automated clusters spun up instantly by the Databricks Job Scheduler to run a production pipeline, then automatically terminated the second the notebook finishes. Costs roughly half the price of All-Purpose compute.
* Serverless Compute: Fully managed by Databricks. You do not choose nodes or scaling laws; the platform instantly provisions SQL warehouses or notebook compute on demand with zero cold-start time.

------------------------------
## 2. Access Modes (Security & Governance)
These options dictate user isolation and how security rules (like Unity Catalog data access controls) are applied to the compute layer:

* Single User: Dedicated entirely to one specific user. Supports all programming languages (Python, SQL, R, Scala). Highly recommended for ML development because it allows installation of custom system libraries.
* Shared: A multi-tenant cluster where multiple users can execute code simultaneously. It uses secure isolation barriers but restricts certain low-level system changes.
* No Isolation Shared: A legacy mode that allows multi-user access without strict security guardrails. Not recommended for sensitive financial or superannuation data.

------------------------------
## 3. Databricks Runtime (DBR) Types
Runtimes determine the core engine version, Apache Spark version, and pre-packaged tools:

* Standard Runtime: Includes Apache Spark, Delta Lake, and basic Python/SQL/Scala core tools. Best for traditional data engineering (ETL).
* Machine Learning (ML) Runtime: Built on top of the Standard Runtime but pre-installs hundreds of ML libraries (Scikit-learn, XGBoost, PyTorch, TensorFlow, MLflow) and fine-tunes GPU configurations.
* GenAI / Quantum (Advanced): Specialized niche runtimes explicitly optimized for massive LLM training pipelines or specific mathematical compute packages.

------------------------------
## 4. Node Types (Virtual Machine Sizes)
Node selection depends entirely on your cloud provider (AWS or Azure). They are grouped into four primary performance families:

* Memory-Optimized (R-Family / Standard_R): High RAM-to-CPU ratio. Crucial for ML training to prevent Out-Of-Memory (OOM) errors during heavy data matrix shuffles.
* Compute-Optimized (C-Family / Standard_F): High CPU clock speeds, lower RAM. Best for running fast math operations or stateless code loops.
* General Purpose (M-Family / Standard_D): Balanced CPU and RAM. Standard entry point for basic data exploration.
* GPU-Enabled (G/P-Family / Standard_NC): Features dedicated NVIDIA graphics cards. Mandatory for deep learning or training heavy transformer models.

------------------------------
## 5. Scaling Mechanics
Controls how the cluster expands and shrinks based on real-time execution stress:

* Autoscaling: You define a minimum and maximum worker threshold. The cluster monitors Spark task backlogs and automatically adds nodes when needed, discarding them when the workload drops.
* Fixed Scale: You specify an exact, unchanging number of worker nodes. Safe for budgeting, but can lead to slow execution or resource waste if sized poorly.
* Local / Single Node: Zero worker nodes; the driver node handles both code execution and data storage. Perfect for lightweight testing on tiny data sets.

------------------------------
## 6. Availability Zone / Pricing Tiers
Determines how the cloud provider physically provisions the background virtual hardware:

* On-Demand Instances: Guaranteed hardware availability. Highly reliable, but billed at standard premium cloud pricing. Best for the cluster Driver node.
* Spot / Low-Priority Instances: Discounted excess cloud capacity (up to 80% cheaper). The cloud provider can reclaim these nodes with short notice. Best for Worker nodes, as Databricks automatically migrates active data tasks if a Spot node is lost.

To finalize your ticket, let me know:

* Are you deploying this on AWS or Azure?
* Do you prefer Serverless management, or does your DevOps team require you to specify exact virtual machine node sizes?

I can map these structural options directly to the exact vendor-specific codes (e.g., Azure VM series or AWS EC2 codes) you need.

