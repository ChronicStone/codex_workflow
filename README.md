# Codex Project Workflow

Codex workflow for optimize token usage and managing long-running implementation plans across multiple sessions

> NOTE: This workflow has scope only within the current project. When you start a new project, you will need to install the workflow again.

## Installation

### 1. Move the ZIP file to the project

Download the ZIP file and move it to the root directory of the project where you want to use the workflow.

```text
my-project/
├── codex_workflows.zip
└── ...
```

### 2. launch Codex app or Codex cli in the project directory, tell it to install the default workflow

Send the following request to the Codex:
> Please extract `codex_workflows.zip`, read the extracted `workflows_setup_guide.md` file, and perform the entire installation process within it.

## Configuration Questions

After installation, the Codex will ask the following questions in sequence.

### 1. Workflow Style and Design Principles (optinal)

The Codex will ask about the project's workflow style and core design principles.
You can describe requirements such as:

- Prioritize modular design;
- Keep dependencies low;
- Do not change public APIs without prior approval;
- Prioritize C/C++ and limit dynamic allocation;
- Always run relevant tests after modifications.

### 2. Power Configuration

The default workflow is designed to save tokens for the ChatGPT Plus package. The Codex will ask if you want to enable each advanced option individually.

- Allow more subagents (currently a maximum of 3) and allow more than one `executor_sol` call.
- Set `executor_luna` and `tester` to the `max` model_reasoning_effort. Currently `xhigh`. 
- Allow subagents to send more detailed report packets to the main agent (event and final report are currently limited to 150 & 250 words).
- Allow subagents to retry more times when stuck/blocked before replacing them (currently 2). The new subagent will have to reload the context packet, but this will reduce the risk of getting stuck; consider this.

## Restart codex after installation

## How to use the workflow with the Codex

There are 3 work routes:
- Light route: Default, for light and medium tasks. Original Codex, minimal context, no need for further explanation.
- Heavy route: For the deployment of heavy plans and tasks. The main agent will coordinate the workers. Sol 5.6 high/xhigh should be used as the main agent.
- Medium route: Coordinating multiple subagents for a less heavy task can sometimes cost more tokens than having the main agent do the work itself. Letting the main agent do the work will be faster. Sol 5.6 medium is recommended.

- Normally, you don't need to do anything.
- When starting or continuing a plan in progress, tell the codex in the prompt: "use medium route / use heavy route. ..."
(The codex will not automatically activate the medium/heavy route. The selected route will be maintained throughout the work session unless you actively change the route.)
- When you want to end a session, clean up and update documents, commit, etc., tell the codex: "end this session. ...". 
Follow this procedure so that ongoing projects can be smoothly resumed in a future session. You can still continue the session after that if needed. 

## Customize the workflow

- Customize the End-of-Session handoff to suit your needs in AGENTS.md
- Add the custom subagents you want in ~/.codex/agents
.... 