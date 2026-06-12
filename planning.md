# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

The domain I chose is upper-division computer science professor reviews at the University of California, Santa Cruz.
Right now, a student has to move between the course list, curriculum chart, and Rate My Professors to understand if a
professor or class is worth taking.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors - Dustin Richmond | Reviews connected to upper-division CSE100/CSE125 logic design courses. | https://www.ratemyprofessors.com/professor/2884610 |
| 2 | Rate My Professors - Niloofar Montazeri | Reviews connected to CSE101/CSE101P/CSE140 courses. | https://www.ratemyprofessors.com/professor/3004516 |
| 3 | Rate My Professors - Seshadhri Comandur | Reviews connected to CSE101M/CSE103 theory courses. | https://www.ratemyprofessors.com/professor/2059447 |
| 4 | Rate My Professors - Daniel Fremont | Reviews connected to CSE101M/CSE103 theory courses. | https://www.ratemyprofessors.com/professor/2556351 |
| 5 | Rate My Professors - Vaggos Chatziafratis | Reviews connected to CSE101M/CSE105 algorithms courses. | https://www.ratemyprofessors.com/professor/2844430 |
| 6 | Rate My Professors - Sungjin Im | Reviews connected to CSE101M and algorithms-related student feedback. | https://www.ratemyprofessors.com/professor/3082669 |
| 7 | Rate My Professors - Delbert Bailey | Reviews connected to CSE102 and CSE103. | https://www.ratemyprofessors.com/professor/604377 |
| 8 | Rate My Professors - Ioannis Demertzis | Reviews connected to CSE108/CSE108C cryptography courses. | https://www.ratemyprofessors.com/professor/2846734 |
| 9 | Rate My Professors - Alexandra Kolla | Reviews connected to CSE109 and theory/math-heavy CSE courses. | https://www.ratemyprofessors.com/professor/2842154 |
| 10 | Rate My Professors - Tyler Sorensen | Reviews connected to CSE110A/CSE110B compiler design. | https://www.ratemyprofessors.com/professor/2696492 |
| 11 | Rate My Professors - Mohsen Lesani | Reviews connected to CSE113 parallel and concurrent programming. | https://www.ratemyprofessors.com/professor/3014180 |
| 12 | Rate My Professors - Cormac Flanagan | Reviews connected to CSE114A programming languages. | https://www.ratemyprofessors.com/professor/454089 |
| 13 | Rate My Professors - Owen Arden | Reviews connected to CSE114A and related CSE teaching. | https://www.ratemyprofessors.com/professor/2473496 |
| 14 | Rate My Professors - Lindsey Kuper | Reviews connected to CSE114A programming languages. | https://www.ratemyprofessors.com/professor/2493257 |
| 15 | Rate My Professors - Richard Jullig | Reviews connected to CSE115A/CSE115B/CSE115C software engineering project courses. | https://www.ratemyprofessors.com/professor/2056294 |
| 16 | Rate My Professors - David Harrison | Reviews connected to CSE118/CSE123A/CSE123B/CSE186/CSE187 project and web development courses. | https://www.ratemyprofessors.com/professor/2328264 |
| 17 | Rate My Professors - Yuanchao Xu | Reviews connected to CSE120 and CSE130 systems courses. | https://www.ratemyprofessors.com/professor/2989121 |
| 18 | Rate My Professors - Marcelo Siero | Reviews connected to CSE120 and other CSE courses. | https://www.ratemyprofessors.com/professor/2883501 |
| 19 | Rate My Professors - Sagnik Nath | Reviews connected to CSE120 and systems-related course feedback. | https://www.ratemyprofessors.com/professor/2624718 |
| 20 | Rate My Professors - Cedric Westphal | Reviews connected to CSE121 embedded system design. | https://www.ratemyprofessors.com/professor/3103126 |
| 21 | Rate My Professors - Matthew Guthaus | Reviews connected to CSE122/CSE127A/CSE127B chip design courses. | https://www.ratemyprofessors.com/professor/1073316 |
| 22 | Rate My Professors - Kerry Veenstra | Reviews connected to CSE130 systems design. | https://www.ratemyprofessors.com/professor/1883634 |
| 23 | Rate My Professors - Scott Brandt | Reviews connected to CSE130 and systems courses. | https://www.ratemyprofessors.com/professor/629552 |
| 24 | Rate My Professors - Liting Hu | Reviews connected to CSE130/CSE134 systems courses. | https://www.ratemyprofessors.com/professor/2915058 |
| 25 | Rate My Professors - Alexander Rudnick | Reviews connected to CSE142/CSE143 AI and NLP courses. | https://www.ratemyprofessors.com/professor/2762323 |
| 26 | Rate My Professors - Yuyin Zhou | Reviews connected to CSE144 deep learning. | https://www.ratemyprofessors.com/professor/2796250 |
| 27 | Rate My Professors - Cihang Xie | Reviews connected to CSE144 deep learning. | https://www.ratemyprofessors.com/professor/2691936 |
| 28 | Rate My Professors - Leilani Gilpin | Reviews connected to CSE146 and AI-related courses. | https://www.ratemyprofessors.com/professor/2803006 |
| 29 | Rate My Professors - Christina Parsa | Reviews connected to CSE150 computer networks. | https://www.ratemyprofessors.com/professor/2351640 |
| 30 | Rate My Professors - Chen Qian | Reviews connected to CSE150 computer networks. | https://www.ratemyprofessors.com/professor/2345038 |
| 31 | Rate My Professors - Rick Graziani | Reviews connected to CSE151/CSE151L advanced networks. | https://www.ratemyprofessors.com/professor/2472228 |
| 32 | Rate My Professors - Ram Raman | Reviews connected to CSE153/CSE156/CSE156L network security and network programming. | https://www.ratemyprofessors.com/professor/3078773 |
| 33 | Rate My Professors - Mike Parsa | Reviews connected to CSE156/CSE156L network programming. | https://www.ratemyprofessors.com/professor/2770176 |
| 34 | Rate My Professors - Katia Obraczka | Reviews connected to CSE157 and networking-related courses. | https://www.ratemyprofessors.com/professor/1429633 |
| 35 | Rate My Professors - James Davis | Reviews connected to CSE160 computer graphics. | https://www.ratemyprofessors.com/professor/625138 |
| 36 | Rate My Professors - Nikos Tziavelis | Reviews connected to CSE180/CSE182 database systems. | https://www.ratemyprofessors.com/professor/3086025 |
| 37 | Rate My Professors - Massimo Di Pierro | Reviews connected to CSE183 web applications. | https://www.ratemyprofessors.com/professor/3018932 |
| 38 | Rate My Professors - Gerald Moulds | Reviews connected to CSE185E/CSE185S technical writing courses. | https://www.ratemyprofessors.com/professor/355999 |
| 39 | UCSC Engineering CSE 2026 Course Catalog | Official course catalog used for course titles, numbers, and upper-division CSE scope. This is metadata/context, not student review evidence. | https://courses.engineering.ucsc.edu/courses/cse/2026 |
| 40 | Reddit - CSE101 w/ Ishtiyaque Ahmad? | Covers Ahmad, who did not have a verified UCSC Rate My Professors page. | https://www.reddit.com/r/UCSC/comments/1iv4uqe/cse101_w_ishtiyaque_ahmad/ |
| 41 | Reddit - Is anyone taking CSE101 with Ishtiyaque Ahmad? | Adds more Ahmad/CSE101 student context. | https://www.reddit.com/r/UCSC/comments/1jxanb0/is_anyone_taking_cse101_with_ishtiyaque_ahmad/ |
| 42 | Reddit - CSE 120, CSE 101, and CSE107? | Mentions CSE120 with Abel Souza, another professor without a verified RMP page. | https://www.reddit.com/r/UCSC/comments/1rgl6yl/cse_120_cse_101_and_cse107/ |
| 43 | Reddit - CSE 130 Hu vs Veenstra | Direct professor/course comparison for CSE130. | https://www.reddit.com/r/UCSC/comments/18iq8x3/cse_130_hu_vs_veenstra/ |
| 44 | Reddit - CSE 130 Preparation | Workload and preparation advice for a major required class. | https://www.reddit.com/r/UCSC/comments/vfkmpa/cse_130_preparation/ |
| 45 | Reddit - How hard was CSE 130 really | Captures difficulty perception and survival advice for CSE130. | https://www.reddit.com/r/UCSC/comments/18kqi31/how_hard_was_cse_130_really/ |
| 46 | Reddit - CSE 110A (Siero) or CSE 186 (Harrison)? | Elective comparison and workload source for CSE110A and CSE186. | https://www.reddit.com/r/UCSC/comments/1pq3jli/cse_110a_siero_or_cse_186_harrison/ |
| 47 | Reddit - CSE 150 with Parsa | Adds course-specific info beyond Christina Parsa's RMP page. | https://www.reddit.com/r/UCSC/comments/1djp9fj/cse_150_with_parsa/ |
| 48 | Reddit - CMPE/CSE 150/L with Parsa? | Older but useful networking-course feedback. | https://www.reddit.com/r/UCSC/comments/dvdvuv/cmpecse_150l_with_parsa/ |
| 49 | Reddit - Thoughts on CSE 182 and CSE 150? | Covers Nikos Tziavelis and Chen Qian together. | https://www.reddit.com/r/UCSC/comments/1itgxzk/thoughts_on_cse_182_and_cse_150/ |
| 50 | Reddit - CSE Students, favorite CSE courses/professors | Broader student opinions across upper-division CSE. | https://www.reddit.com/r/UCSC/comments/n5cvlh/cse_students_what_are_some_of_your_favorite_cse/ |
| 51 | Reddit - CSE 143? | Student comments about CSE143/NLP, including class interest level and whether ML or AI background is needed. | https://www.reddit.com/r/UCSC/comments/sndywa/cse_143/ |


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
Each Chunk will be one complete review or one complete reddit comment.If a Reddit post/comment is
  unusually long, split it by paragraph or sentence around roughly 300-400 tokens.
**Overlap:**
No overlap for RMP the idea is that the whole review stays together. Use about 40-60 tokens of overlap only when
  splitting a long Reddit comment, so an idea that spans a boundary does not get cut off.
**Reasoning:**
The docs are already divided in a meaningful way. One review has enough context needed so it makes sense for that to be
all that is needed for a chunk. 
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2 through sentence-transformers, free and local.
**Top-k:**
Use dynamic top-k. For normal questions, retrieve the top 5 chunks. If the question names a specific professor,
retrieve up to 3 chunks for that professor. If the question asks about a class or compares professors for a class,
retrieve up to 3 chunks per relevant professor, with a cap of about 12 chunks total so the answer has enough context
without pulling in too much noise.

**Production tradeoff reflection:**
For this project, I want an embedding model that works well on short, casual student reviews and is easy to run locally.
If this were for real users, I would compare accuracy, speed, cost, privacy, and context length. A bigger API model might
understand vague or messy student wording better, but a local model is cheaper, faster to test, and does not require
sending all review text to an outside service.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Alexander Rudnick's teaching style? | Students mostly describe Rudnick as passionate, helpful, and good at explaining concepts. Reviews also mention examples, demos, Discord help, and lectures that feel engaging. |
| 2 | What do students say about the workload and assignments in Rudnick's classes? | Students say the workload is usually manageable if you do not procrastinate. Some reviews mention clear assignment instructions, helpful demos, and homework that can be challenging but fair. |
| 3 | What concerns or downsides do students mention about Alexander Rudnick? | Most feedback is positive, but some students mention slow email replies, slow grading, ungraded extra credit, and occasional classroom management issues. |
| 4 | What do students say about CSE143 / NLP at UCSC? | Students describe CSE143/NLP as fun and interesting, especially for people interested in linguistics, machine learning, AI, and language-related topics. |
| 5 | Do students think ML or AI experience is needed before taking CSE143? | Students say ML or AI experience can help, but it is not required. People without that background can still do fine if they are interested and keep up with the class. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Retrieval might pull noisy or weakly related chunks. A query like "best professor for CSE143" could retrieve reviews that
mention Rudnick or NLP but do not actually answer the comparison part of the question.

2. Source attribution could be wrong if chunk metadata is attached incorrectly. Since each review/comment needs its own
professor, course, URL, and chunk position, a metadata bug could make the system cite the wrong review or source.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```text
Raw Sources
  - Rate My Professors copied reviews
  - Reddit copied posts/comments
  - UCSC CSE catalog notes
        |
        v
[1] Document Ingestion
    Tool: Python + pathlib
    Output: loaded text with source file and source URL
        |
        v
[2] Cleaning / Preprocessing
    Tool: Python string cleanup + regex
    Removes: nav text, repeated labels, empty lines, HTML leftovers
    Keeps: review text, ratings, course names, professor names, tags
        |
        v
[3] Chunking
    Tool: custom Python chunk_text function
    RMP: one complete review = one chunk
    Reddit: one post/comment = one chunk
    Long Reddit comments: split around 300-400 tokens with 40-60 token overlap
        |
        v
[4] Embedding + Vector Store
    Embedding tool: sentence-transformers
    Embedding model: all-MiniLM-L6-v2
    Vector store: ChromaDB
    Stored metadata: professor, course, source URL, source type, chunk index
        |
        v
[5] Retrieval
    Tool: ChromaDB similarity search
    Query logic: detect professor/course names when possible
    Top-k: top 5 normally, up to 3 chunks per professor, cap around 12 total
        |
        v
[6] Grounded Generation
    Tool: Groq API with llama-3.3-70b-versatile
    Prompt rule: answer only from retrieved chunks
    Output: plain-language answer with source citations
        |
        v
Query Interface
    Tool: Gradio or CLI
    User sees: answer + cited source chunks
```

This follows the outline's required pipeline: ingestion, chunking, embedding/vector store, retrieval, and generation.
The main design choice is that reviews and comments stay whole because they are already meaningful student statements.
Metadata is important because the final answer needs to cite which professor, course, and source each chunk came from.
Retrieval uses semantic search, but the query step also checks for professor or course names so comparison questions can
pull a few reviews per relevant professor instead of only returning one overall top-k list.

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I will give the AI my Documents, Chunking Strategy, and Architecture sections and ask it to help build the RMP ingestion
and chunking pipeline. I expect it to help write Python code that live-scrapes the selected Rate My Professors pages,
extracts the embedded review data, cleans the text, and turns each non-empty review into one chunk with professor,
course, URL, rating, and chunk index metadata. I will verify the output by running pytest, running the chunk-building
script, checking the total chunk count, and reading at least 5 printed sample chunks to make sure they are readable and
cited to the right professor/source.

**Milestone 4 — Embedding and retrieval:**
I will give the AI my Retrieval Approach, Architecture, and Anticipated Challenges sections and ask it to build the
embedding and retrieval layer around my existing review chunks. I expect it to help write code that loads
`data/chunks/rmp_chunks.jsonl`, embeds each chunk with `all-MiniLM-L6-v2`, stores the chunks in ChromaDB, and keeps
metadata like professor, course, source URL, and chunk index attached to every stored review.

I will also ask the AI to implement the query logic from my top-k plan. A normal question should retrieve about 5 chunks,
a professor question should retrieve up to 3 chunks for that professor, and a course comparison question should retrieve
about 3 chunks per professor for that course. The retrieval code should detect professor names and CSE course numbers,
then use metadata filters so unrelated chunks do not crowd out the useful ones.

I will verify this by running pytest, rebuilding the vector store, and testing real queries from my Evaluation Plan. For
example, I will check that a Rudnick question returns Rudnick chunks, a CSE130 question returns only CSE130 chunks across
multiple professors, and a Rudnick + CSE143 question returns no chunks if the scraped data does not actually contain a
matching Rudnick CSE143 review.

**Milestone 5 — Generation and interface:**
I will give the AI my Retrieval Approach, Evaluation Plan, Anticipated Challenges, and Architecture sections and ask it
to build the final grounded answer layer. I expect it to help write code that takes the retrieved ChromaDB chunks,
formats them into numbered evidence blocks, sends them to Groq with a strict prompt, and returns a short answer with
citations like `[1]` and `[2]`.

I will also ask the AI to build a CLI interface instead of a web app for this milestone. The CLI should load the chunk
file, connect to the existing ChromaDB collection, use `GROQ_API_KEY` from `.env`, call the answer pipeline, and print
an answer plus a sources list. It should not hardcode secrets, and it should give a clear error if the API key or vector
store is missing.

I will verify this by running pytest and then testing the CLI with my evaluation questions. I will check that Rudnick
questions return Rudnick citations, CSE130 questions only cite CSE130 chunks, and questions without matching evidence
say there is not enough review data instead of making up an answer.
