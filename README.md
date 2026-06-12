# The Unofficial Guide to UCSC CSE Professors

This project is a retrieval-augmented generation (RAG) guide built from
student reviews of UCSC computer science professors. A command-line interface
retrieves relevant review chunks from ChromaDB and asks a Groq-hosted language
model to answer only from those chunks.

## Domain

The guide covers student experiences with UCSC computer science professors and
courses. This information is useful because the official course catalog lists
topics and prerequisites, but it does not describe teaching style, workload,
grading, communication, or common student concerns. Those details are spread
across individual Rate My Professors reviews and can be difficult to compare.

The implemented corpus is narrower than the source list originally proposed in
`planning.md`. It contains 58 review chunks from 12 Rate My Professors pages.
The planned Reddit sources were not ingested, which becomes important in the
evaluation and failure analysis below.

## Document Sources

| # | Source | Type | URL |
|---|---|---|---|
| 1 | Alexander Rudnick | Rate My Professors | https://www.ratemyprofessors.com/professor/2762323 |
| 2 | Chen Qian | Rate My Professors | https://www.ratemyprofessors.com/professor/2345038 |
| 3 | Christina Parsa | Rate My Professors | https://www.ratemyprofessors.com/professor/2351640 |
| 4 | Cormac Flanagan | Rate My Professors | https://www.ratemyprofessors.com/professor/454089 |
| 5 | David Harrison | Rate My Professors | https://www.ratemyprofessors.com/professor/2328264 |
| 6 | Kerry Veenstra | Rate My Professors | https://www.ratemyprofessors.com/professor/1883634 |
| 7 | Lindsey Kuper | Rate My Professors | https://www.ratemyprofessors.com/professor/2493257 |
| 8 | Liting Hu | Rate My Professors | https://www.ratemyprofessors.com/professor/2915058 |
| 9 | Matthew Guthaus | Rate My Professors | https://www.ratemyprofessors.com/professor/1073316 |
| 10 | Nikos Tziavelis | Rate My Professors | https://www.ratemyprofessors.com/professor/3086025 |
| 11 | Owen Arden | Rate My Professors | https://www.ratemyprofessors.com/professor/2473496 |
| 12 | Scott Brandt | Rate My Professors | https://www.ratemyprofessors.com/professor/629552 |

## Chunking Strategy

**Chunk size:** One complete review per chunk. A review longer than 400
whitespace-separated tokens is split into 400-token windows.

**Overlap:** Normal reviews have no overlap because each review is already a
complete unit. Long split reviews use 60 tokens of overlap so a sentence or
idea near a boundary is not completely separated from its context.

**Preprocessing:** The ingestion code extracts `Rating` objects from the
page's embedded `window.__RELAY_STORE__` JSON. It decodes HTML entities,
replaces non-breaking spaces, collapses repeated whitespace, and skips empty
comments. Each chunk includes the professor, course, date, ratings, tags, and
review text. Metadata also stores the source URL, rating ID, chunk index, and
chunk part.

**Why this fits the documents:** Rate My Professors data is already organized
as individual reviews. Keeping one review together preserves the relationship
between a student's opinion, the course, and the rating metadata. It also
avoids merging unrelated students' experiences into one embedding.

**Final chunk count:** 58 chunks from 12 professor pages.

## Sample Chunks

### Sample 1: Alexander Rudnick, CSE13

Source: https://www.ratemyprofessors.com/professor/2762323

```text
Professor: Alexander Rudnick
Course: CSE13
Date: 2026-03-09 23:18:25 +0000 UTC
Quality: 5.0
Difficulty: 3.0
Attendance: mandatory
Would Take Again: Yes
Grade: Not sure yet
Tags: Amazing lectures, Caring, Accessible outside class
Review: Honestly great professor. Enthusiastic to teach and takes the time to
go through examples to help you understand things. Homework is somewhat
difficult but manageable and your midterm and final are both take home.
```

### Sample 2: Cormac Flanagan, CSE114A

Source: https://www.ratemyprofessors.com/professor/454089

```text
Professor: Cormac Flanagan
Course: CSE114A
Date: 2025-06-06 05:56:56 +0000 UTC
Quality: 5.0
Difficulty: 3.0
Attendance: non mandatory
Would Take Again: Yes
Grade: B+
Tags: Amazing lectures, Clear grading criteria
Review: really enjoyed his lectures the most at ucsc so far
```

### Sample 3: Lindsey Kuper, CSE114A

Source: https://www.ratemyprofessors.com/professor/2493257

```text
Professor: Lindsey Kuper
Course: CSE114A
Date: 2025-06-18 04:07:06 +0000 UTC
Quality: 4.0
Difficulty: 4.0
Attendance: mandatory
Would Take Again: Yes
Grade: C+
Tags: Tough grader, Caring, Graded by few things
Review: The class was difficult for me but her lectures were great. I think
she cares about her students and if you put in a decent amount of effort you
will pass.
```

### Sample 4: Kerry Veenstra, CSE130

Source: https://www.ratemyprofessors.com/professor/1883634

```text
Professor: Kerry Veenstra
Course: CSE130
Date: 2026-03-26 17:34:17 +0000 UTC
Quality: 5.0
Difficulty: 3.0
Attendance: non mandatory
Would Take Again: N/A
Grade: A
Tags: Amazing lectures, Hilarious
Review: I thought that overall he was a great professor. His quizzes and exams
were fair, and lectures really made sense. I wouldn't take this course again
just because it is generally stressful, but definitely take him if possible.
```

### Sample 5: Nikos Tziavelis, CSE180

Source: https://www.ratemyprofessors.com/professor/3086025

```text
Professor: Nikos Tziavelis
Course: CSE180
Date: 2026-03-13 21:22:07 +0000 UTC
Quality: 4.0
Difficulty: 2.0
Attendance: non mandatory
Would Take Again: Yes
Grade: A
Tags: N/A
Review: Explains topics really well, and cares about teaching well. In class
examples were great, homework and tests weren't too bad.
```

## Embedding Model

**Model used:** `sentence-transformers/all-MiniLM-L6-v2`

The model is free, runs locally, and is fast enough for a small corpus of short
student reviews. It also avoids sending the full review corpus to an embedding
API.

**Production tradeoff reflection:** For a production system, I would compare
retrieval accuracy on informal student language, context length, latency,
privacy, multilingual support, hardware requirements, and API cost. A larger
hosted embedding model or a domain-tuned reranker could improve vague queries
and ranking quality. The tradeoff would be higher cost, added latency, and
sending review text to an external service.

## Retrieval Approach

The system detects known professor names and CSE course numbers in the query.
It then applies ChromaDB metadata filters and dynamic top-k rules:

- General question: 5 chunks.
- Named professor: up to 3 chunks for that professor.
- Named course: up to 3 chunks per professor teaching that course, capped at
  12 chunks.
- Named professor and course: up to 3 chunks matching both fields.

### Retrieval Test 1: Teaching style

Query:

```text
What do students say about Alexander Rudnick's teaching style?
```

Top results:

| Rank | Distance | Course | Relevant content |
|---|---:|---|---|
| 1 | 0.5796 | CSE13 | Enthusiastic, explains examples, manageable homework |
| 2 | 0.6182 | CSE142 | Strong general recommendation |
| 3 | 0.7283 | CSE13 | Caring, answers Discord questions, sometimes sidetracked |

The first and third chunks directly support the question. The second chunk is
about overall approval rather than teaching style, so the set is relevant but
not perfectly ranked. The distances are also above the assignment's preferred
0.5 checkpoint.

### Retrieval Test 2: Workload and assignments

Query:

```text
What do students say about the workload and assignments in Rudnick's classes?
```

Top results:

| Rank | Distance | Course | Relevant content |
|---|---:|---|---|
| 1 | 0.7460 | CSE13 | Homework is difficult but manageable; exams are take-home |
| 2 | 0.7509 | CSE142 | General recommendation with no workload details |
| 3 | 0.9014 | CSE13 | Teaching and Discord comments, no workload details |

Only the first chunk directly answers the question. The professor metadata
filter keeps the results on Rudnick, but semantic ranking still returns two
weak chunks. This makes the retrieval quality partially relevant.

### Retrieval Test 3: Concerns and downsides

Query:

```text
What concerns or downsides do students mention about Alexander Rudnick?
```

Top results:

| Rank | Distance | Course | Relevant content |
|---|---:|---|---|
| 1 | 0.6594 | CSE142 | Positive recommendation, not a downside |
| 2 | 0.6604 | CSE13 | Positive teaching and workload comments |
| 3 | 0.7390 | CSE13 | Silent emails, ungraded extra credit, classroom chaos |

The third result contains the exact evidence needed, but it ranks behind two
positive reviews. The generated answer succeeds because all three chunks are
passed to the model. This is still a retrieval weakness because reducing
top-k would have removed the useful evidence.

### Retrieval Test 4: Missing CSE143 evidence

Query:

```text
What do students say about CSE143 / NLP at UCSC?
```

The detector finds `CSE143`, but ChromaDB returns no matching chunks. The
implemented corpus does not include the planned Reddit discussion or any RMP
review labeled CSE143.

## Grounded Generation

The system prompt says:

```text
Answer only from the provided review chunks. Use citations like [1] or [2]
for claims. Do not invent professors, courses, ratings, grades, or student
opinions. If the chunks do not answer the question, say there is not enough
matching review evidence.
```

Retrieved chunks are formatted as numbered evidence blocks. Each block
includes professor, course, source URL, rating ID, date, and review text. The
model is instructed to cite those block numbers. The CLI also constructs and
prints the complete source list programmatically, so source URLs do not depend
on the model remembering to include them.

If retrieval returns no chunks, `answer_question()` does not call the model.
It returns a fixed no-evidence response instead. This prevents the LLM from
answering an unsupported course question from its general training data.

## Example Responses

### Grounded response 1

```text
Question: What do students say about Alexander Rudnick's teaching style?

Answer:
According to the reviews, students say that Alexander Rudnick's teaching
style is enthusiastic [1], inspirational [2], and caring [1]. He takes the
time to explain examples [1] and answers questions on Discord [3]. Some
students also find him hilarious [2] and nice [3]. However, one student
mentions that he sometimes gets sidetracked in class [3]. Overall, students
have a positive view of his teaching style.
```

### Grounded response 2

```text
Question: What concerns or downsides do students mention about Alexander
Rudnick?

Answer:
Students mention the following concerns or downsides about Alexander Rudnick:
- Being very inaccessible outside of class, with emails sometimes met with
  silence [3]
- Creating extra credit assignments that went ungraded [3]
- Struggling to handle classroom chaos, such as talking [3]
```

### Out-of-scope refusal

```text
Question: What do students say about CSE999 at UCSC?

Answer:
I do not have matching review chunks for that professor/course in the scraped
RMP data.

Sources:
No sources returned.
```

## Query Interface

The interface is a command-line program. Its input is one quoted question. Its
output has an `Answer` section followed by a numbered `Sources` section.

Setup:

```bat
python -m pip install -r requirements.txt
copy .env.example .env
```

Add a Groq API key to `.env`, then build the vector store:

```bat
python scripts\build_vector_store.py
```

Ask a question:

```bat
python scripts\ask_guide.py "What do students say about Alexander Rudnick's teaching style?"
```

Sample interaction:

```text
Answer:
According to the reviews, students say that Alexander Rudnick's teaching
style is enthusiastic [1], inspirational [2], and caring [1]. He takes the
time to explain examples [1] and answers questions on Discord [3].

Sources:
[1] Alexander Rudnick - CSE13 -
https://www.ratemyprofessors.com/professor/2762323
[2] Alexander Rudnick - CSE142 -
https://www.ratemyprofessors.com/professor/2762323
[3] Alexander Rudnick - CSE13 -
https://www.ratemyprofessors.com/professor/2762323
```

Retrieval can be inspected without calling Groq:

```bat
python scripts\query_chunks.py "What concerns or downsides do students mention about Alexander Rudnick?"
```

## Evaluation Report

| # | Question | Expected answer | System response summary | Retrieval quality | Response accuracy |
|---|---|---|---|---|---|
| 1 | What do students say about Alexander Rudnick's teaching style? | Passionate, helpful, good explanations, examples, Discord help, and engaging lectures | Enthusiastic, inspirational, caring, explains examples, answers Discord questions, sometimes sidetracked | Partially relevant | Accurate |
| 2 | What do students say about the workload and assignments in Rudnick's classes? | Usually manageable without procrastination; clear assignments and challenging but fair work | Homework is somewhat difficult but manageable; little detail is available for CSE142 | Partially relevant | Partially accurate |
| 3 | What concerns or downsides do students mention about Alexander Rudnick? | Slow replies and grading, ungraded extra credit, and classroom management issues | Silent emails, ungraded extra credit, and difficulty handling classroom chaos | Partially relevant | Accurate |
| 4 | What do students say about CSE143 / NLP at UCSC? | Fun and interesting for students interested in linguistics, ML, AI, and language | No matching review chunks | Off-target | Inaccurate |
| 5 | Do students think ML or AI experience is needed before taking CSE143? | Helpful but not required | No matching review chunks | Off-target | Inaccurate |

### Exact Recorded Responses

**Question 1**

```text
According to the reviews, students say that Alexander Rudnick's teaching style
is enthusiastic [1], inspirational [2], and caring [1]. He takes the time to
explain examples [1] and answers questions on Discord [3]. Some students also
find him hilarious [2] and nice [3]. However, one student mentions that he
sometimes gets sidetracked in class [3]. Overall, students have a positive view
of his teaching style.
```

**Question 2**

```text
According to the reviews, students say that the homework in Rudnick's CSE13
class is "somewhat difficult but manageable" [1]. There is no detailed
information about the workload and assignments in his CSE142 class [2].
Overall, students find his classes to be of moderate difficulty, with a rating
of 3.0 for CSE13 [1, 3].
```

**Question 3**

```text
Students mention the following concerns or downsides about Alexander Rudnick:
- Being very inaccessible outside of class, with emails sometimes met with
  silence [3]
- Creating extra credit assignments that went ungraded [3]
- Struggling to handle classroom chaos, such as talking [3]
```

**Questions 4 and 5**

```text
I do not have matching review chunks for that professor/course in the scraped
RMP data.
```

## Failure Case Analysis

### Failure 1: CSE143 questions have no evidence

**Questions that failed:** Questions 4 and 5 about CSE143/NLP.

**What the system returned:** It returned the fixed no-evidence response and no
sources.

**Root cause:** This is an ingestion coverage failure. The evaluation plan was
written with Reddit CSE143 discussions in mind, but the implemented ingestion
pipeline only collected 12 Rate My Professors pages. The final chunk file has
no `CSE143` metadata, so the retrieval filter correctly returns zero results.
Generation cannot produce the expected answer because the evidence never
entered the vector store.

**What I would change:** Add a Reddit ingestion path that stores each post or
comment as a chunk with `source_type`, URL, course, author/date when available,
and chunk index metadata. Then rebuild the vector store and rerun questions 4
and 5. I would not weaken the grounding prompt or let the model answer from
general knowledge.

### Failure 2: Negative Rudnick evidence ranks third

**Question affected:** What concerns or downsides do students mention about
Alexander Rudnick?

**What happened:** The exact negative review had distance `0.7390` and ranked
third. Two positive reviews ranked above it at `0.6594` and `0.6604`.

**Root cause:** The professor metadata filter guarantees the correct professor,
but the MiniLM semantic ranking is weak on this small set of short reviews. The
words in the question about "concerns or downsides" did not rank the clearly
negative review first.

**What I would change:** Retrieve a slightly larger candidate set, then apply a
cross-encoder reranker or a lightweight keyword-aware reranking step for terms
such as `concern`, `problem`, `downside`, and `difficult`. I would also test a
stronger embedding model and add a relevance threshold before generation.

## Spec Reflection

**One way the spec helped:** The planning document made the review-level
chunking rule explicit before implementation. That kept each student's course,
ratings, opinion, and source URL together and made source attribution
straightforward. The dynamic top-k plan also led directly to professor and
course metadata filters instead of relying only on vector similarity.

**One way the implementation diverged:** The source plan included RMP, Reddit,
and official course context, but the implemented corpus only includes 12 RMP
pages. This reduced scraping complexity and allowed the full RAG pipeline to be
finished and tested, but it left the two planned CSE143 questions unsupported.
The evaluation keeps those questions and reports the gap instead of changing
the test plan after seeing the results.

## AI Usage

### Instance 1: Ingestion and chunking

- **What I gave the AI:** The Documents, Chunking Strategy, and Architecture
  sections from `planning.md`, including the rule that one complete RMP review
  should normally equal one chunk.
- **What it produced:** Python modules for extracting the embedded RMP relay
  store, converting rating objects into records, cleaning comments, attaching
  metadata, and writing JSONL chunks.
- **What I changed or overrode:** I kept the implementation limited to the 12
  first-pass RMP sources rather than pretending all planned sources were
  ingested. I also required empty reviews to be removed, HTML entities to be
  decoded, source URLs and rating IDs to be stored, and tests to verify the
  exact metadata.

### Instance 2: Retrieval, generation, and CLI

- **What I gave the AI:** The Retrieval Approach, Evaluation Plan, Anticipated
  Challenges, grounding requirements, and the decision to use a CLI.
- **What it produced:** ChromaDB storage, MiniLM embeddings, professor/course
  detection, dynamic top-k retrieval, a Groq prompt, numbered citations, and
  CLI scripts for retrieval inspection and answering.
- **What I changed or overrode:** I required metadata filtering for named
  professors and courses, programmatic source output instead of trusting the
  LLM to write URLs, a fixed refusal when retrieval returns no chunks, and
  environment-based API key loading. I also tested the generated logic with
  fake embeddings and fake generators before running the live model.

## Tests

Run the complete suite:

```bat
pytest -q
```

Run the coverage gate:

```bat
pytest --cov=src\unofficial_guide --cov-report=term-missing -q
```

The final verification result is 24 passing tests with 82% statement coverage.

## Dependency Security

The final dependency review upgrades `python-dotenv` and the
Sentence Transformers/Transformers stack to patched releases. The audit command
is:

```bat
python -m pip_audit -r requirements.txt ^
  --ignore-vuln CVE-2026-45829 ^
  --ignore-vuln CVE-2025-3000
```

The two explicit exceptions do not affect the code paths used by this project:

- `CVE-2026-45829` affects ChromaDB's unauthenticated HTTP server endpoint.
  This project never starts that server and only uses a local
  `PersistentClient`.
- `CVE-2025-3000` affects `torch.jit.script`. The embedding wrapper does not
  call that API, and the advisory currently lists no patched PyTorch release.

## Demo Video Checklist

The separate 3-5 minute submission video should show:

1. The CLI answering evaluation question 1 with citations.
2. Evaluation question 2 with citations and its incomplete evidence.
3. Evaluation question 3 with citations, followed by the retrieval output
   showing the useful negative review ranked third.
4. Evaluation question 4 or the CSE999 query producing the grounded refusal.
5. A walkthrough of the evaluation table and both failure analyses above.
