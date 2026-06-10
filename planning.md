# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? 
The domain I chose is Upper Division Computer Science Professor Reviews at the University of California, Santa Cruz. Right now a student has to maneuvar between the course list, curriculum chart, 
rate my professor to understand if a professor/class is worth to take.-->

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


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
