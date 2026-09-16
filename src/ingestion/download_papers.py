import os
import arxiv
import requests
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "data", "raw_papers")

def download_papers(query: str, max_results: int, output_dir: str) -> list[dict]:
    """
    Downloads papers from arXiv based on the given query and saves them to the specified output directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    downloaded_papers = []

    for result in client.results(search):
        paper_id = result.get_short_id()
        pdf_path = os.path.join(output_dir, f"{paper_id}.pdf")

        response = requests.get(result.pdf_url)
        response.raise_for_status()
        with open(pdf_path, 'wb') as f:
            f.write(response.content)

        downloaded_papers.append({
            "id": paper_id,
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "summary": result.summary,
            "published": str(result.published),
            "pdf_path": pdf_path
        })

    return downloaded_papers


if __name__ == "__main__":
    papers = download_papers("retrieval augmented generation", 5, OUTPUT_DIR)
    with open(os.path.join(OUTPUT_DIR, "downloaded_papers.json"), "w") as f:
        json.dump(papers, f, indent=4)
    print(f"Descargados {len(papers)} papers")
    for p in papers:
        print(p["id"], "-", p["title"])

