# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all placeholders in this file.

## SUBMISSION DETAILS

Name: **<YOUR_NAME>** \
SUNet ID: **<YOUR_SUNET_ID>** \
Citations: **Ollama Structured Outputs docs (https://ollama.com/blog/structured-outputs), Ollama library docs (https://ollama.com/library)**

This assignment took me about **<FILL_HOURS>** hours to do.


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Implement an Ollama-based `extract_action_items_llm(text)` in `week2/app/services/extract.py`.
Requirements:
- Structured output parsing (JSON array of strings) with validation
- Model selection from `OLLAMA_MODEL` with local fallback model
- Return clean, deduplicated action items
- Raise a clear service-layer exception when Ollama fails or returns malformed output
``` 

Generated Code Snippets:
```
week2/app/services/extract.py:21
week2/app/services/extract.py:34
week2/app/services/extract.py:104
week2/app/routers/action_items.py:49
```

### Exercise 2: Add Unit Tests
Prompt: 
```
Add unit tests for `extract_action_items_llm()` in `week2/tests/test_extract.py`.
Cover:
- bullet-list style notes
- keyword-prefixed lines
- empty input behavior
- malformed LLM JSON response path
Use monkeypatch/mocks so tests do not depend on a running Ollama daemon.
``` 

Generated Code Snippets:
```
week2/tests/test_extract.py:26
week2/tests/test_extract.py:43
week2/tests/test_extract.py:55
week2/tests/test_extract.py:63
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
Refactor week2 backend for clarity:
- define explicit request/response Pydantic schemas
- clean up DB layer and lifecycle initialization
- improve route-level error handling
- keep existing endpoint behavior backward-compatible where possible
```

Generated/Modified Code Snippets:
```
week2/app/schemas.py:6
week2/app/schemas.py:21
week2/app/db.py:15
week2/app/db.py:106
week2/app/main.py:15
week2/app/routers/action_items.py:25
week2/app/routers/notes.py:11
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
Add:
1) a new endpoint `POST /action-items/extract-llm` and wire it to the frontend as an `Extract LLM` button.
2) a notes list endpoint `GET /notes` and wire it to the frontend as a `List Notes` button.
Keep UI feedback clear for success and error cases.
``` 

Generated Code Snippets:
```
week2/app/routers/action_items.py:49
week2/app/routers/notes.py:23
week2/frontend/index.html:29
week2/frontend/index.html:30
week2/frontend/index.html:97
week2/frontend/index.html:122
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Generate `week2/README.md` from the current codebase.
Include:
- project overview
- setup and run instructions
- API endpoints and behavior
- test instructions
- Ollama dependency notes for the LLM endpoint
``` 

Generated Code Snippets:
```
week2/README.md:1
week2/README.md:13
week2/README.md:43
week2/README.md:107
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `<...>` placeholders in this file and fill personal details.
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 
