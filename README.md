# NeMo Data Designer – Data Architecture Principle Generator (Microservice)

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-informational.svg)](https://www.docker.com/)
[![NVIDIA NeMo](https://img.shields.io/badge/NVIDIA-NeMo_Data_Designer-brightgreen.svg)](https://build.nvidia.com/nvidia-nemo)
[![Synthetic Data](https://img.shields.io/badge/Synthetic_Data-LLM--generated-success.svg)](#)
[![GitHub Repo](https://img.shields.io/badge/GitHub-nemo--principles--microservice-black.svg)](https://github.com/hlosukwakha/nemo-principles-microservice)

---

## Overview

This project is a **Dockerized NeMo Data Designer microservice client** that generates
**data architecture principles** as Markdown documents.

It uses the **NVIDIA NeMo Data Designer** service under the hood to produce enterprise‑style
principles such as _Data Integration_, with sections like:

- Statement  
- Description  
- Rationale  
- Implications  
- Classification Area / Principle Type / Source metadata  

The generated Markdown files can be:

- preserved as architectural reference documents,  
- version‑controlled in Git (e.g., in this repository), and  
- iterated on quickly as your data architecture evolves.

This makes the project particularly useful for **data architects**, **enterprise architects**
and **data governance teams** who want a repeatable, scriptable way to create and refine
their architecture principles.

Repository URL:  
https://github.com/hlosukwakha/nemo-principles-microservice

---

## What the project does

At a high level, the container:

1. Calls the **NeMo Data Designer microservice** using your NVIDIA API key.
2. Sends a configuration that describes the structure of a “Data Architecture Principle”
   (columns for Statement, Description, Rationale, Implications, etc.).
3. Asks NeMo to generate a small preview dataset with a single record.
4. Renders that record into a **Markdown file** that looks and reads like a well‑formed
   architectural principle.
5. Writes the result into the `output/` directory of the repository.

Because the output is plain Markdown, you can:

- commit it to Git for **version control**,  
- drop it into Confluence, PowerPoint or any documentation tool, and  
- track the history of how your principles have evolved over time.

---

## Architecture & technologies

This project combines:

- **Python 3.11** – orchestration logic and Markdown rendering.  
- **NVIDIA NeMo Data Designer (hosted microservice)** – synthetic data and text generation
  for the principle content.  
- **Docker & Docker Compose** – containerized runtime for easy, reproducible execution.  
- **Markdown** – human‑readable, version‑controllable artefacts representing your
  data architecture principles.  

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/hlosukwakha/nemo-principles-microservice
cd nemo-principles-microservice
```

### 2. Configure your NVIDIA API key

You **must** generate your API key from the **NVIDIA AI platform settings** page:

> https://build.nvidia.com/settings/api-keys

Do **not** use keys from:

> https://org.ngc.nvidia.com/setup/api-key

Those NGC keys are not valid for the NeMo Data Designer microservice used here.

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Then edit `.env` and set:

```env
NVIDIA_API_KEY=nvapi-your-key-from-build-nvidia
```

Make sure you:

- paste only the raw key value (no `Bearer ` prefix, no quotes), and  
- keep this file out of version control (it is already ignored via `.gitignore`).

### 3. Build and run the container

```bash
docker compose build
docker compose up
```

The service will:

- connect to the NeMo Data Designer microservice,  
- generate a single principle (by default: **Data Integration**), and  
- write a Markdown file under:

```text
output/data_integration_principle.md
```

You will also see the same content logged to the console.

### 4. Generate principles for other topics

You can override the topic using an environment variable:

```bash
PRINCIPLE_TOPIC="Data Quality" docker compose run --rm   -e PRINCIPLE_TOPIC="Data Quality" nemo-principle-generator
```

This will create a file like:

```text
output/data_quality_principle.md
```

---

## How this helps data architects

This project is designed to fit naturally into a **data architecture practice**:

- **Rapid drafting**  
  Quickly generate first‑cut principles (e.g., _Data Integration_, _Data Quality_,
  _Data Lineage_, _Metadata Management_) in a consistent structure.

- **Consistency & standardization**  
  The prompts and configuration encode your preferred “template” for principles,
  helping you keep wording and sections aligned across domains.

- **Preservation & version control**  
  Because outputs are Markdown files, they can be kept in Git alongside the rest
  of your architecture artefacts, with full history and diffing.

- **Collaboration**  
  Teammates can review, comment, and propose pull requests to refine principles,
  just like any other code or documentation.

Over time, you can evolve the prompts and layout in `generate_principle.py` to reflect
your organisation’s style, governance requirements, and domain‑specific language.

---

## Project structure

```text
.
├─ Dockerfile             # Container definition
├─ docker-compose.yml     # Compose service for the generator
├─ requirements.txt       # Python dependencies (NeMo microservices client, pandas, etc.)
├─ .env.example           # Template for NVIDIA_API_KEY configuration
├─ app/
│  ├─ __init__.py
│  └─ generate_principle.py  # Core logic: build config, call NeMo DD, render Markdown
└─ output/                # Generated principles (git-versionable artefacts)
```

---

## References & credits

This project stands on the shoulders of the excellent work done by the **NVIDIA NeMo Data Designer** team.

- 💻 **NeMo Data Designer example code**  
  `https://lnkd.in/eJdAG7qG`

- 📗 **NeMo Data Designer documentation**  
  `https://lnkd.in/eUAXnjxf`

Please refer to the official NVIDIA resources above for full details on:

- NeMo Data Designer concepts and configuration,
- model support and limits, and
- best practices for generating and working with synthetic data.

---

## License

Apache 2.0

