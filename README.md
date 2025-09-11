# DETOEX - DEtection of  TOxic and hateful speech with EXplanations

DETOEX is a multilingual hate speech detection system that combines Large Language Models (LLMs) with a curated vocabulary of derogatory language and traditional Natural Language Processing (NLP) techniques. It also leverages LLMs to provide contextualized explanations for why a certain piece of text was labeled as toxic.

## Features

- Multilingual support for English, French, and Greek
- Combined detection approach using both term matching and direct LLM analysis
- Detailed explanations of detected toxic content

## Architecture

DETOEX uses a two-pipeline approach for toxicity detection:

1. **Term-based pipeline**: Matches specific terms from curated vocabularies
2. **Non-term pipeline**: Analyzes text directly using LLMs
3. **Fusion**: Combines results from both pipelines for comprehensive analysis

## Requirements

- Python 3.12+
- Docker (for containerized deployment)
- An LLM API endpoint that supports OpenAI-compatible API format

## Access
You can freely access the deployed tool at [https://detoex.ails.ece.ntua.gr/](https://detoex.ails.ece.ntua.gr/)

## Quick Start with Docker

The easiest way to run DETOEX locally is using Docker with the provided Dockerfile.local:

```bash
# Build the Docker image
docker build -t detoex-local -f Dockerfile.local .

# Run the container
docker run -p 8000:8000 detoex-local
```

The API will be available at http://localhost:8000.

## LLM Endpoint Configuration

DETOEX supports configuring different LLM endpoints for each language. By default, the Dockerfile.local is configured to use the Docker host's IP (`172.17.0.1:8080`) for all languages, but you can modify these settings:

```
# In Dockerfile.local
ENV LLM_URL_EN=http://172.17.0.1:8080/v1
ENV LLM_URL_FR=http://172.17.0.1:8080/v1
ENV LLM_URL_EL=http://172.17.0.1:8080/v1
```

You can update these variables before building the image, or override them at runtime:

```bash
docker run -p 8000:8000 \
  -e LLM_URL_EN=http://your-custom-endpoint/v1 \
  detoex-local
```

## Development Setup

For development with hot-reloading of code changes:

```bash
docker run -p 8000:8000 \
  -v $(pwd)/detoex:/app/detoex \
  detoex-local
```

This will mount your local `detoex` directory into the container, allowing changes to be reflected immediately.

## API Usage

### Request

```json
POST /
{
  "language": "en",
  "texts": ["text to analyze for toxicity"]
}
```

### Response

```json
{
  "results": ["Explanation of toxicity if detected"]
}
```

## Data Resources

The Docker image includes:

- Prompt templates for all supported languages
- Vocabularies of potentially toxic terms
- Stanza NLP models (downloaded during image build)

## Acknowledgements

This project is funded as part of an FSTP call from the EU project UTTER (Unified Transcription and Translation for Extended Reality), supported by the European Union's Horizon Europe programme under grant agreement No. 101070631.