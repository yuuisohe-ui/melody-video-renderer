import os, sys, json, urllib.request

api_key = os.environ.get('OPENAI_API_KEY', '')
song_title = os.environ.get('SONG_TITLE', '')
keywords = os.environ.get('VIDEO_KEYWORDS', '') or song_title or 'music'
lyrics_text = os.environ.get('LYRICS_TEXT', '').strip()


def openai_post(endpoint, payload):
    req = urllib.request.Request(
        f"https://api.openai.com/v1/{endpoint}",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


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
                            "write a vivid DALL-E image generation prompt (English, under 200 characters) "
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
        "model": "dall-e-2",
        "prompt": prompt,
        "n": 1,
        "size": "512x512",
        "response_format": "url",
    })
    print(result["data"][0]["url"])
except Exception as e:
    print(f"[get_cover] DALL-E error: {e}", file=sys.stderr)
    print("")
