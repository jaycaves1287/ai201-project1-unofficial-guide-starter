import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from unofficial_guide.embeddings import SentenceTransformerEmbedder
from unofficial_guide.retrieval import plan_retrieval, retrieve
from unofficial_guide.vector_store import ChromaReviewStore, load_chunks_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query the ChromaDB review chunks and print retrieval results."
    )
    parser.add_argument("query", help="Question to search for.")
    parser.add_argument(
        "--chunks",
        type=Path,
        default=ROOT / "data" / "chunks" / "rmp_chunks.jsonl",
        help="JSONL chunks used to detect professor/course names.",
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
    args = parser.parse_args()

    chunks = load_chunks_jsonl(args.chunks)
    embedder = SentenceTransformerEmbedder()
    store = ChromaReviewStore.persistent(args.db_path, args.collection, embedder)
    plan = plan_retrieval(args.query, chunks, args.top_k)
    results = retrieve(args.query, store, chunks, args.top_k)

    print(f"Query: {args.query}")
    print(f"Top-k: {plan.top_k}")
    print(f"Professor targets: {', '.join(plan.targets.professors) or 'none'}")
    print(f"Course targets: {', '.join(plan.targets.courses) or 'none'}")
    print()
    if not results:
        print("No matching review chunks found.")
        return 0
    for index, result in enumerate(results, start=1):
        print(f"[{index}] distance={result.distance:.4f}")
        print(f"Professor: {result.metadata.get('professor', 'N/A')}")
        print(f"Course: {result.metadata.get('course', 'N/A')}")
        print(f"Source: {result.metadata.get('source_url', 'N/A')}")
        print(result.text)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
