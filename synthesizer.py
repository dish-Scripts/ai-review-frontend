import os
import requests

def generate_meta_review(summary_folder="summaries", output_file="report.txt"):
    summaries = []

    for file in sorted(os.listdir(summary_folder)):
        if file.endswith(".txt"):
            path = os.path.join(summary_folder, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            summaries.append(f"Review from {file.replace('.txt', '')}:\n{content.strip()}\n")

    combined_input = "\n\n".join(summaries)

    # Call the backend API (Render backend URL)
    backend_url = "https://ai-review-backend-0iek.onrender.com/generate-review"
    try:
        response = requests.post(backend_url, json={"input_text": combined_input})
        response.raise_for_status()  # raise error if not 2xx
    except Exception as e:
        print(f"❌ Error calling backend: {e}")
        return

    result = response.json().get("review", "")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)

    print("✅ Meta-review saved:", output_file)

