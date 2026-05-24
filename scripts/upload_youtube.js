const { google } = require('googleapis');
const fs = require('fs');

const oauth2 = new google.auth.OAuth2(
  process.env.YT_CLIENT_ID,
  process.env.YT_CLIENT_SECRET
);
oauth2.setCredentials({ refresh_token: process.env.YT_REFRESH_TOKEN });
const yt = google.youtube({ version: 'v3', auth: oauth2 });

function buildLrc(alignedWords) {
  if (!alignedWords || alignedWords.length === 0) return '';
  return alignedWords.map(w => {
    const totalSec = w.startS || 0;
    const min = Math.floor(totalSec / 60);
    const sec = (totalSec % 60).toFixed(2).padStart(5, '0');
    const word = (w.word || '').replace(/\n/g, ' ').trim();
    return `[${String(min).padStart(2,'0')}:${sec}] ${word}`;
  }).join('\n');
}

async function main() {
  const songTitle = process.env.SONG_TITLE || 'AI 노래';
  
  let alignedWords = [];
  try {
    alignedWords = JSON.parse(process.env.ALIGNED_WORDS || '[]');
  } catch(e) {}

  const lrc = buildLrc(alignedWords);
  
  const description = `Generated with 멜로디 클래스 AI Lyric Video Studio

${lrc}

#멜로디클래스 #AI노래 #한국어학습 #중국어학습 #lyricvideo #aimusic`;

  const res = await yt.videos.insert({
    part: ['snippet', 'status'],
    requestBody: {
      snippet: {
        title: `${songTitle} | 멜로디 클래스 AI 노래`,
        description,
        tags: ['멜로디클래스', 'AI노래', '한국어학습', '중국어학습', 'lyric video', 'AI music'],
        categoryId: '10',
      },
      status: {
        privacyStatus: 'public',
        selfDeclaredMadeForKids: false,
      },
    },
    media: { body: fs.createReadStream('work/out.mp4') },
  });

  const videoId = res.data.id;
  const url = 'https://youtu.be/' + videoId;
  console.log('VIDEO_ID=' + videoId);
  console.log('VIDEO_URL=' + url);
  fs.writeFileSync('work/result.json', JSON.stringify({ videoId, url }));
}

main().catch(e => { console.error(e); process.exit(1); });
