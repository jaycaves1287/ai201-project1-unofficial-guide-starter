import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from unofficial_guide.answering import answer_question
from unofficial_guide.embeddings import SentenceTransformerEmbedder
from unofficial_guide.generation import GroqAnswerGenerator, format_answer_for_cli
from unofficial_guide.vector_store import ChromaReviewStore, load_chunks_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ask the UCSC CSE professor review guide a grounded question."
    )
    parser.add_argument("query", help="Question to answer from retrieved RMP chunks.")
    parser.add_argument(
        "--chunks",
        type=Path,
        default=ROOT / "data" / "chunks" / "rmp_chunks.jsonl",
        help="JSONL chunk file.",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=ROOT / "chroma_db",
        help="Persistent ChromaDB directory.",
    )
    parser.add_argument(
        "--collection",
        default="ucsc_cse_reviews",
        help="ChromaDB collection name.",
    )
    parser.add_argument("--top-k", type=int, default=None, help="Override top-k.")
    parser.add_argument(
        "--model",
        default="llama-3.3-70b-versatile",
        help="Groq model name.",
    )
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key.strip():
        print("Missing GROQ_API_KEY. Add it to .env or your environment.", file=sys.stderr)
        return 1

    chunks = load_chunks_jsonl(args.chunks)
    embedder = SentenceTransformerEmbedder()
    store = ChromaReviewStore.persistent(args.db_path, args.collection, embedder)
    if store.count() == 0:
        print(
            "No vector records found. Run scripts\\build_vector_store.py first.",
            file=sys.stderr,
        )
        return 1

    generator = GroqAnswerGenerator(api_key=api_key, model=args.model)
    try:
        answer = answer_question(
            args.query,
            store,
            chunks,
            generator,
            top_k=args.top_k,
        )
    except Exception as error:
        print(f"Could not answer question: {error}", file=sys.stderr)
        return 1

    print(format_answer_for_cli(answer))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
