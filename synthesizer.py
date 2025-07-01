import os
import requests

def generate_meta_review(summary_folder="summaries", output_file="report.txt"):
    summaries = []

    # Collect all summaries
    for file in sorted(os.listdir(summary_folder)):
        if file.endswith(".txt"):
            path = os.path.join(summary_folder, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            summaries.append(f"Review from {file.replace('.txt', '')}:\n{content.strip()}\n")

    # Combine summaries
    combined_input = "\n\n".join(summaries)

    # Meta-review prompt
    prompt = f"""
You are an expert product analyst. Based on the following summarized reviews of a product, perform a meta-analysis.

1. Identify the **Top 5–6 key features** discussed (e.g., Battery, Display, Performance).
2. For each feature, explain:
   - What multiple reviewers agreed on
   - Any disagreements or differing opinions
3. Create a final section:
   - ✅ **Consolidated Pros**
   - ❌ **Consolidated Cons**
   - 💡 **Unique Comments** (said by only one reviewer)

Use clear markdown-style formatting.

Summaries:
{combined_input}
"""

    # Call your FastAPI backend
    try:
        response = requests.post(
            "https://ai-review-backend-0iek.onrender.com/generate",
            json={"prompt": prompt},
            timeout=60  # avoid hanging forever
        )
        response.raise_for_status()
        result = response.json()["response"]

        # Save to file + print
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(result)
        print(f"\n\n📄 Saved file: {output_file}")

    except requests.exceptions.RequestException as e:
        print("❌ Error communicating with backend:", e)

