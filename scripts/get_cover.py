import os, sys, json, base64, urllib.request, urllib.error

api_key = os.environ.get('OPENAI_API_KEY', '')
song_title = os.environ.get('SONG_TITLE', '')
keywords = os.environ.get('VIDEO_KEYWORDS', '') or song_title or 'music'
lyrics_text = os.environ.get('LYRICS_TEXT', '').strip()


def openai_post(endpoint, payload):
    req = urllib.request.Request(
        f"https://api.openai.com/v1/{endpoint}",
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        print(f"[get_cover] HTTP {e.code} from {endpoint}: {body}", file=sys.stderr)
        raise


def generate_prompt():
    if lyrics_text:
        try:
            resp = openai_post("chat/completions", {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are an art director. Given a song title and lyrics, "
                            "write a vivid image generation prompt (English, under 200 characters) "
                            "for an album cover illustration. Cinematic, artistic style. No text or typography in the image."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Song: {song_title}\nLyrics: {lyrics_text[:400]}",
                    },
                ],
                "max_tokens": 200,
                "temperature": 0.8,
            })
            return resp["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[get_cover] GPT prompt generation failed: {e}", file=sys.stderr)

    return (
        f"Album cover art for a song called '{song_title}'. "
        f"Theme: {keywords}. "
        "Vivid, artistic, cinematic illustration style. No text or typography. Square format."
    )


try:
    prompt = generate_prompt()
    print(f"[get_cover] Using prompt: {prompt}", file=sys.stderr)

    result = openai_post("images/generations", {
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "low",
    })

    b64 = result["data"][0]["b64_json"]
    os.makedirs("work", exist_ok=True)
    with open("work/cover_raw.jpg", "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"[get_cover] Image saved to work/cover_raw.jpg", file=sys.stderr)
    print("ok")

except Exception as e:
    print(f"[get_cover] error: {e}", file=sys.stderr)
    print("")
