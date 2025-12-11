import os
from datetime import datetime
from pathlib import Path

import pandas as pd

from nemo_microservices.data_designer.essentials import (
    CategorySamplerParams,
    DataDesignerConfigBuilder,
    LLMTextColumnConfig,
    NeMoDataDesignerClient,
    SamplerColumnConfig,
    SamplerType,
)


def build_config(topic: str, model_alias: str) -> DataDesignerConfigBuilder:
    """
    Build a NeMo Data Designer configuration that generates one
    data-architecture principle similar to the provided example slide.
    """
    config = DataDesignerConfigBuilder()

    # Seed / categorical metadata columns
    config.add_column(
        SamplerColumnConfig(
            name="principle_name",
            sampler_type=SamplerType.CATEGORY,
            params=CategorySamplerParams(values=[topic]),
        )
    )

    config.add_column(
        SamplerColumnConfig(
            name="classification_area",
            sampler_type=SamplerType.CATEGORY,
            params=CategorySamplerParams(values=["Information Governance"]),
        )
    )

    config.add_column(
        SamplerColumnConfig(
            name="principle_type",
            sampler_type=SamplerType.CATEGORY,
            params=CategorySamplerParams(values=["Data Architecture"]),
        )
    )

    config.add_column(
        SamplerColumnConfig(
            name="source",
            sampler_type=SamplerType.CATEGORY,
            params=CategorySamplerParams(values=["Derived"]),
        )
    )

    # LLM-generated fields using the hosted model alias (e.g. nemotron-nano-v2)

    config.add_column(
        LLMTextColumnConfig(
            name="statement",
            model_alias=model_alias,
            prompt=(
                "You are an enterprise data architect at a regulated financial "
                "services group.\n\n"
                "Write a single, concise principle *statement* (15–30 words) "
                "for the data architecture principle called '{{ principle_name }}'. "
                "Emphasise a loosely coupled data landscape that enables governed, "
                "secure data sharing across the organisation."
            ),
        )
    )

    config.add_column(
        LLMTextColumnConfig(
            name="description",
            model_alias=model_alias,
            prompt=(
                "Write a detailed *description* (80–140 words) for the data "
                "architecture principle '{{ principle_name }}'.\n\n"
                "Explain that:\n"
                "- business units are federated but must share data;\n"
                "- data sharing is enabled through an integrated financial services "
                "data architecture;\n"
                "- the landscape is loosely coupled to minimise technical dependency;\n"
                "- integration, metadata, and semantic layers support data leverage, "
                "aggregation and sharing across the group;\n"
                "- enterprise technologies are used when justified by business cases.\n\n"
                "Write as a single coherent paragraph, neutral, non-marketing tone."
            ),
        )
    )

    config.add_column(
        LLMTextColumnConfig(
            name="rationale",
            model_alias=model_alias,
            prompt=(
                "Write the *rationale* section (80–140 words) for the data "
                "architecture principle '{{ principle_name }}'.\n\n"
                "Cover why data integration and aggregation are needed for regulatory, "
                "risk, and growth purposes in a federated financial-services group. "
                "Mention:\n"
                "- preserving business-unit autonomy;\n"
                "- customer-centric view across products and channels;\n"
                "- avoiding a one-size-fits-all technology mandate while still "
                "standardising integration practices.\n"
                "Write as a single paragraph."
            ),
        )
    )

    config.add_column(
        LLMTextColumnConfig(
            name="implications",
            model_alias=model_alias,
            prompt=(
                "For the data architecture principle '{{ principle_name }}', write an "
                "'Implications' section.\n"
                "Produce 5–8 concise bullet points, each 1–2 sentences, formatted "
                "in Markdown as '- ...'.\n\n"
                "Include points such as:\n"
                "- architecture priorities aligned with business priorities;\n"
                "- risk management and governance for data sharing;\n"
                "- 'one trusted source' and integrated data architecture supporting "
                "information management;\n"
                "- loose coupling, controlled replication, and reduced duplication;\n"
                "- preserving uniqueness and autonomy of systems while enabling "
                "group-wide analytics;\n"
                "- failure isolation: issues in one subsystem should not break the "
                "entire landscape."
            ),
        )
    )

    return config


def generate_principle(topic: str = "Data Integration") -> pd.Series:
    """
    Call the NeMo Data Designer *microservice* using your NVIDIA_API_KEY.
    """
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError(
            "NVIDIA_API_KEY is not set. "
            "Set it in your environment or .env file before running."
        )

    base_url = os.getenv("NEMO_DD_BASE_URL", "https://ai.api.nvidia.com/v1/nemo/dd")
    model_alias = os.getenv("MODEL_ALIAS", "nemotron-nano-v2")

    client = NeMoDataDesignerClient(
        base_url=base_url,
        default_headers={"Authorization": f"Bearer {api_key}"},
    )

    config = build_config(topic=topic, model_alias=model_alias)

    # Hosted NeMo Data Designer uses num_records
    preview = client.preview(config, num_records=1)
    df = preview.dataset
    if df is None or df.empty:
        raise RuntimeError("No data generated by NeMo Data Designer preview()")

    return df.iloc[0]


def render_markdown(record: pd.Series) -> str:
    """
    Render the generated principle into a markdown document
    loosely inspired by the slide layout.
    """
    return f"""# Principle: {record['principle_name']}

**Classification Area:** {record['classification_area']}  
**Principle Type:** {record['principle_type']}  
**Source:** {record['source']}

---

## Statement

{record['statement'].strip()}

---

## Description

{record['description'].strip()}

---

## Rationale

{record['rationale'].strip()}

---

## Implications

{record['implications'].strip()}

---
_Generated with NeMo Data Designer on {datetime.utcnow().isoformat(timespec='seconds')}Z._
"""


def main() -> None:
    topic = os.getenv("PRINCIPLE_TOPIC", "Data Integration")
    record = generate_principle(topic=topic)

    md = render_markdown(record)
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    outfile = output_dir / f"{topic.lower().replace(' ', '_')}_principle.md"
    outfile.write_text(md, encoding="utf-8")

    print(f"✅ Generated principle written to {outfile}")
    print()
    print(md)


if __name__ == "__main__":
    main()
