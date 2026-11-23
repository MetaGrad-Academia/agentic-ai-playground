# agentic-ai-playground

## Project Setup

uv init --no-package --python 3.13 --vcs none .

uv add langchain langchain-google-genai python-dotenv requests urllib3 black isort fastmcp

## MCP server workshop

Start the server from an MCP client using this command and stdio transport:

```powershell
uv run python src\workshop-21\08-mcp\server.py
```

The `generate_password` tool uses cryptographically secure randomness and accepts
a length from 8 to 128 (default 16). The `get_time` tool returns the current UTC
date and time in ISO 8601 format. Generated passwords are returned to the MCP
client, so use a trusted client and avoid logging them.

The included client starts the server automatically over stdio:

```powershell
uv run python src\workshop-21\08-mcp\client.py generate_password --length 20
uv run python src\workshop-21\08-mcp\client.py get_time
```

Omit `--length` to use the default. Passwords are printed to the terminal;
avoid redirecting them to logs or sharing terminal output.

## Hallucination workshop

Install and start [Ollama](https://ollama.com), then run:

```powershell
ollama pull qwen3.5:4b
uv run python src\workshop\00-hallunicnation.py
```

The demo uses LangChain's `PromptTemplate | ChatOllama` pattern with
`temperature=0.9` and loads environment variables with `load_dotenv()`.
It asks about an invented research-paper reference, requesting a journal, DOI,
findings, and an exact quotation, then reveals that the reference was invented.
The higher temperature allows more varied output, not guaranteed hallucinations.
A model may correctly say it cannot verify the paper.
Ask students to identify invented claims and discuss why answers need verification.

## Agent tool-selection workshop

With Ollama running and `qwen3.5:4b` downloaded, run:

```powershell
uv run python src\workshop\04-agent-tool-selection.py
```

Enter a question about an order, a product price, the refund policy, or sending
support an email. LangChain's `create_agent` lets the model choose among four
tools and use their results to answer. The program prints the selected tools,
their arguments, their results, and the final answer.

All store data is fictional, and the email tool only simulates sending: no real
email is sent. Try `Where is order ORD-1001?`, `What is the price of a mouse?`,
or `Send support an email from student@example.com about my damaged keyboard.`
You can also ask for both an order status and the refund policy in one question.
Use an Ollama model that supports tool calling.

### Traditional Python comparison

```powershell
python src\workshop\04-traditional-tool-selection.py
```

This standalone version uses only Python's standard library: keyword rules and
regular expressions select ordinary functions instead of an LLM selecting tools.
It uses the same demo order data, product prices, refund policy, and simulated
email result. No Ollama server or LangChain is needed.

Try the same questions above, or combine order status and refund policy in one
question. For email requests, include an address and put the issue after `about`.
Missing details and unsupported wording produce explicit messages; unlike an
LLM, these fixed rules only recognize the patterns written in the program.

## Transcript RAG workshop

Save a YouTube transcript as a UTF-8 `.txt` file. With Ollama running:

```powershell
ollama pull qwen3.5:4b
ollama pull nomic-embed-text
uv run python src\workshop\04-rag-pipeline.py "C:\path\to\transcript.txt"
```

The program splits the transcript into 200-word chunks with 40-word overlap,
embeds them using local Ollama, and stores the vectors in memory. For each
question, it retrieves up to four passages and asks the model to answer from
those passages with chunk citations. Retrieved source previews are displayed.

Ask standalone questions; previous questions are not included in the context.
Type `exit` to quit. The index is rebuilt each time the program starts.
This accepts transcript files, not YouTube URLs, and requires no additional
Python dependencies beyond the project's existing packages.

The model is instructed to acknowledge insufficient evidence, but retrieval can
miss relevant passages and the model can still hallucinate. Check answers and
citations against the original transcript.
