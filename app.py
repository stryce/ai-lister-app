from flask import Flask, render_template_string, request
import openai
import base64
import os

# === CONFIG ===
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <title>AI Listing Generator</title>
  <style>
    body { font-family: sans-serif; margin: 40px; background: #f8f9fa; }
    h2 { color: #333; }
    form { margin-bottom: 20px; }
    pre { background: #eee; padding: 10px; border-radius: 5px; white-space: pre-wrap; }
    input[type="submit"] { padding: 10px 20px; }
  </style>
</head>
<body>
  <h2>Upload your item photo</h2>
  <form method="post" enctype="multipart/form-data">
    <input type="file" name="file" required>
    <input type="submit" value="Generate Listing">
  </form>
  {% if result %}
    <h3>Generated Listing:</h3>
    <pre>{{ result }}</pre>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            img_bytes = file.read()
            base64_img = base64.b64encode(img_bytes).decode('utf-8')
            image_data_url = f"data:image/jpeg;base64,{base64_img}"

            chat_response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "You are an expert at writing online marketplace listings. "
                                    "Given this image, generate the following:\\n"
                                    "- A clear, SEO-friendly title (under 80 characters)\\n"
                                    "- A detailed description that covers brand, color, style, material, condition, and any unique features\\n"
                                    "- 5-10 relevant keywords (comma-separated)\\n\\n"
                                    "Do not make up details that are not visible in the image."
                                )
                            },
                            { "type": "image_url", "image_url": image_data_url }
                        ]
                    }
                ],
                max_tokens=500
            )
            result = chat_response.choices[0].message.content

    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
