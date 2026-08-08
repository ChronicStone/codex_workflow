<h3 align="center"><big><big><strong>SIMPLE&emsp;&emsp;───&emsp;&emsp;EASY&emsp;&emsp;───&emsp;&emsp;EFFICIENT</strong></big></big></h3>
<p align="center"><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(to use)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(to install)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(token consumption)</small></p>
<hr>

![Workflow illustration](illustration.png)

A workflow designed to drastically reduce overall token usage, support seamless deployment across multiple sessions, and remain extremely simple to use.

> ⭐ For lightweight tasks, it won’t overdo things. Light route is default.

## 1. Quick installation ⚙️

Requires Python 3.11 or newer for deterministic lifecycle operations.

### Open Codex CLI / Codex app from your project directory 

▶️ Send:

```text
Download and extract the latest GitHub Release from https://github.com/viettran-edgeAI/codex_workflow/releases. Then read the bundled `codex_workflow/install.md` and follow it to complete the installation.
```
> ⭐ Recommended: use 5.6 Luna xhigh for installation. 

🔄 Restart Codex after installation

New sessions do not check for a newer workflow release by default. To enable
the check, send `codex_workflow --enable_auto_update`. To disable it again,
send `codex_workflow --disable_auto_update`.

To remove the workflow, send `codex_workflow --remove`. It first shows a
destructive dry-run summary and requires a second explicit confirmation.

## 2. Workflow usage 

### This workflow has 3 routes:
- Light route : No subagents, no workflow, minimal context.
- Heavy route : Deploy subagents, full workflow.
- Medium route: Main agent performs the work; only Explorer and the dedicated
  End-of-Session worker are used.

### How to use
- Normally, for simple work, general Q&A, you don't need to do anything. `light route` is the default route.

--------------------------------
- When starting or continuing a plan in progress, just tell Codex in the prompt: "

```text
use medium route / use heavy route. [your task description]".
```
> Codex stays on the selected route until you change it, so you don’t need to repeat it in every prompt.

--------------------------------
If the implementation plan is not yet complete, but the context window is nearly full or already been compacted too many times, or you simply want to pause the work, trigger the **End-of-Session** handoff by sending:

```text
end this session. [more details if needed].
```
> 💡 You can still continue the session after that mesage.

To resume the unfinished work in a new session, send:

```text
use heavy route. continue the unfinished work.
```
---------------
> **⭐ Recommendation:** Assign very large and complex tasks to the `heavy route` to make the most of its capabilities and maximize token usage savings.

## 3. More details 🧭 
For the complete command reference, installed-file map, scripted customization
guide, and Heavy-route design, see [workflow_usage.md](workflow_usage.md).
