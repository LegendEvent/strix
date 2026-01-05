<p align="center">
  <a href="https://strix.ai/">
    <img src=".github/logo.png" width="150" alt="Strix Logo">
  </a>
</p>

<h1 align="center">Strix</h1>

<h2 align="center">Open-source AI Hackers to secure your Apps</h2>

<div align="center">

[![Python](https://img.shields.io/pypi/pyversions/strix-agent?color=3776AB)](https://pypi.org/project/strix-agent/)
[![PyPI](https://img.shields.io/pypi/v/strix-agent?color=10b981)](https://pypi.org/project/strix-agent/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

[![GitHub Stars](https://img.shields.io/github/stars/usestrix/strix)](https://github.com/usestrix/strix)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?&logo=discord&logoColor=white)](https://discord.gg/YjKFvEZSdZ)
[![Website](https://img.shields.io/badge/Website-strix.ai-2d3748.svg)](https://strix.ai)

<a href="https://trendshift.io/repositories/15362" target="_blank"><img src="https://trendshift.io/api/badge/repositories/15362" alt="usestrix%2Fstrix | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>


[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/usestrix/strix)

</div>

<br>

<div align="center">
  <img src=".github/screenshot.png" alt="Strix Demo" width="800" style="border-radius: 16px;">
</div>

<br>

> [!TIP]
> **New!** Strix now integrates seamlessly with GitHub Actions and CI/CD pipelines. Automatically scan for vulnerabilities on every pull request and block insecure code before it reaches production!

---

## 🦉 Strix Overview

Strix are autonomous AI agents that act just like real hackers - they run your code dynamically, find vulnerabilities, and validate them through actual proof-of-concepts. Built for developers and security teams who need fast, accurate security testing without the overhead of manual pentesting or the false positives of static analysis tools.

**Key Capabilities:**

- 🔧 **Full hacker toolkit** out of the box
- 🤝 **Teams of agents** that collaborate and scale
- ✅ **Real validation** with PoCs, not false positives
- 💻 **Developer‑first** CLI with actionable reports
- 🔄 **Auto‑fix & reporting** to accelerate remediation


## 🎯 Use Cases

- **Application Security Testing** - Detect and validate critical vulnerabilities in your applications
- **Rapid Penetration Testing** - Get penetration tests done in hours, not weeks, with compliance reports
- **Bug Bounty Automation** - Automate bug bounty research and generate PoCs for faster reporting
- **CI/CD Integration** - Run tests in CI/CD to block vulnerabilities before reaching production

---

## 🚀 Quick Start

**Prerequisites:**
- Docker (running)
- An LLM provider key (e.g. [get OpenAI API key](https://platform.openai.com/api-keys) or use a local LLM)

### Installation & First Scan

```bash
# Install Strix
curl -sSL https://strix.ai/install | bash

# Or via pipx
pipx install strix-agent

# Configure your AI provider
export STRIX_LLM="openai/gpt-5"
export LLM_API_KEY="your-api-key"

# Run your first security assessment
strix --target ./app-directory
```

> [!NOTE]
> First run automatically pulls the sandbox Docker image. Results are saved to `strix_runs/<run-name>`

## ☁️ Run Strix in Cloud

Want to skip the local setup, API keys, and unpredictable LLM costs? Run the hosted cloud version of Strix at **[app.strix.ai](https://strix.ai)**.

Launch a scan in just a few minutes—no setup or configuration required—and you’ll get:

- **A full pentest report** with validated findings and clear remediation steps
- **Shareable dashboards** your team can use to track fixes over time
- **CI/CD and GitHub integrations** to block risky changes before production
- **Continuous monitoring** so new vulnerabilities are caught quickly

[**Run your first pentest now →**](https://strix.ai)

---

## ✨ Features

### 🛠️ Agentic Security Tools

Strix agents come equipped with a comprehensive security testing toolkit:

- **Full HTTP Proxy** - Full request/response manipulation and analysis
- **Browser Automation** - Multi-tab browser for testing of XSS, CSRF, auth flows
- **Terminal Environments** - Interactive shells for command execution and testing
- **Python Runtime** - Custom exploit development and validation
- **Reconnaissance** - Automated OSINT and attack surface mapping
- **Code Analysis** - Static and dynamic analysis capabilities
- **Knowledge Management** - Structured findings and attack documentation

### 🎯 Comprehensive Vulnerability Detection

Strix can identify and validate a wide range of security vulnerabilities:

- **Access Control** - IDOR, privilege escalation, auth bypass
- **Injection Attacks** - SQL, NoSQL, command injection
- **Server-Side** - SSRF, XXE, deserialization flaws
- **Client-Side** - XSS, prototype pollution, DOM vulnerabilities
- **Business Logic** - Race conditions, workflow manipulation
- **Authentication** - JWT vulnerabilities, session management
- **Infrastructure** - Misconfigurations, exposed services

### 🕸️ Graph of Agents

Advanced multi-agent orchestration for comprehensive security testing:

- **Distributed Workflows** - Specialized agents for different attacks and assets
- **Scalable Testing** - Parallel execution for fast comprehensive coverage
- **Dynamic Coordination** - Agents collaborate and share discoveries

---

## 💻 Usage Examples

### Basic Usage

```bash
# Scan a local codebase
strix --target ./app-directory

# Security review of a GitHub repository
strix --target https://github.com/org/repo

# Black-box web application assessment
strix --target https://your-app.com
```

### Advanced Testing Scenarios

```bash
# Grey-box authenticated testing
strix --target https://your-app.com --instruction "Perform authenticated testing using credentials: user:pass"

# Multi-target testing (source code + deployed app)
strix -t https://github.com/org/app -t https://your-app.com

# Focused testing with custom instructions
strix --target api.your-app.com --instruction "Focus on business logic flaws and IDOR vulnerabilities"

# Provide detailed instructions through file (e.g., rules of engagement, scope, exclusions)
strix --target api.your-app.com --instruction-file ./instruction.md
```

### 🤖 Headless Mode

Run Strix programmatically without interactive UI using the `-n/--non-interactive` flag—perfect for servers and automated jobs. The CLI prints real-time vulnerability findings, and the final report before exiting. Exits with non-zero code when vulnerabilities are found.

```bash
strix -n --target https://your-app.com
```

### 🔄 CI/CD (GitHub Actions)

Strix can be added to your pipeline to run a security test on pull requests with a lightweight GitHub Actions workflow:

```yaml
name: strix-penetration-test

on:
  pull_request:

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Install Strix
        run: curl -sSL https://strix.ai/install | bash

      - name: Run Strix
        env:
          STRIX_LLM: ${{ secrets.STRIX_LLM }}
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}

        run: strix -n -t ./ --scan-mode quick
```

### ⚙️ Configuration

```bash
export STRIX_LLM="openai/gpt-5"
export LLM_API_KEY="your-api-key"

# Optional
export LLM_API_BASE="your-api-base-url"  # if using a local model, e.g. Ollama, LMStudio
export PERPLEXITY_API_KEY="your-api-key"  # for search capabilities
```

### GitHub Copilot models

We support Copilot-backed models via STRIX_LLM by using model names of the form:

export STRIX_LLM="github-copilot/<model>"

This triggers an interactive OAuth device-flow the first time you run Strix and stores a refresh token at $XDG_CONFIG_HOME/strix/copilot_auth.json (defaults to ~/.config/strix/copilot_auth.json). After login, Strix will automatically refresh tokens and call the Copilot API on your behalf.

Notes:
- First-run is interactive (open browser & enter code). For non-interactive CI you must use a different provider or pre-provision credentials.
- Tokens are stored locally with best-effort 0600 permissions — review the token store if this is a concern.

Example (copyable):
export STRIX_LLM="github-copilot/gpt-copilot-v1"
# Run Strix once and complete the device flow when prompted


[OpenAI's GPT-5](https://openai.com/api/) (`openai/gpt-5`) and [Anthropic's Claude Sonnet 4.5](https://claude.com/platform/api) (`anthropic/claude-sonnet-4-5`) are the recommended models for best results with Strix. See the LLM providers documentation for supported providers including Vertex AI, Bedrock, Azure, and local models.

## 🤝 Contributing

We welcome contributions of code, docs, and new prompt modules - check out our [Contributing Guide](CONTRIBUTING.md) to get started or open a [pull request](https://github.com/usestrix/strix/pulls)/[issue](https://github.com/usestrix/strix/issues).

## 👥 Join Our Community

Have questions? Found a bug? Want to contribute? **[Join our Discord!](https://discord.gg/YjKFvEZSdZ)**

## 🌟 Support the Project

**Love Strix?** Give us a ⭐ on GitHub!
## 🙏 Acknowledgements

Strix builds on the incredible work of open-source projects like [LiteLLM](https://github.com/BerriAI/litellm), [Caido](https://github.com/caido/caido), [ProjectDiscovery](https://github.com/projectdiscovery), [Playwright](https://github.com/microsoft/playwright), and [Textual](https://github.com/Textualize/textual). Huge thanks to their maintainers!


> [!WARNING]
> Only test apps you own or have permission to test. You are responsible for using Strix ethically and legally.

</div>
