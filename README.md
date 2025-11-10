🧠 Code_Base_Genius: The Agentic Code-Documentation System
Code_Base_Genius is an AI-powered, multi-agent system designed to automatically generate high-quality, comprehensive Markdown documentation for any public GitHub repository.


💡 Overview
Code_Base_Genius is an AI-powered, multi-agent system built on the Jac programming language and the Jaseci platform. It operates autonomously: given a GitHub URL, it clones the repository, analyzes its structure and code relationships, and synthesizes a clear, human-readable documentation report.

While the system is optimized for Python and Jac codebases, its design is generalizable to other languages.

✨ Key Features
Autonomous Documentation Generation: Accepts a GitHub URL and produces a complete, structured Markdown document (docs.md).
Multi-Agent Architecture: Utilizes specialized, cooperating agents to handle different stages of the workflow, ensuring robustness and modularity.
Code Context Graph (CCG): Constructs a detailed graph capturing relationships between functions, classes, and modules (e.g., function calls, inheritance) to inform deep analysis and documentation.
Intelligent Planning: The Supervisor agent uses a file-tree map and README summary to prioritize the documentation of high-impact files first.
API Exposure: Provides an HTTP interface (Jac server with walkers) to allow a user to supply a repository URL and download the generated documentation.
⚙️ System Architecture: The Agent Pipeline
The system is implemented as a multi-agent pipeline, where each agent fulfills a specialized role in the documentation workflow:

Agent Role	Responsibility
Code Genius (Supervisor)	Orchestrates the workflow, receives the GitHub URL, delegates tasks, and aggregates intermediate results to assemble the final documentation.
Repo Mapper	Clones the repository, generates a structured file-tree representation (ignoring directories like .git), and produces a concise README summary for planning.
Code Analyzer	Performs deep code analysis, parses source files (e.g., using Tree-sitter), and constructs the Code Context Graph (CCG). It provides APIs to the Supervisor for querying relationships.
DocGenie	Synthesizes the final documentation, converting structured data from other agents into a well-organized Markdown document with necessary sections and diagrams.
🚀 Getting Started
Prerequisites
To run CodeGenius, you'll need:

Python 3.8+
Jaseci (The Jac runtime environment)
Git (for cloning repositories)
Installation
Clone the Repository
