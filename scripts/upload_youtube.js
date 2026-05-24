const { google } = require('googleapis');
const fs = require('fs');

const oauth2 = new google.auth.OAuth2(
  process.env.YT_CLIENT_ID,
  process.env.YT_CLIENT_SECRET
);
oauth2.setCredentials({ refresh_token: process.env.YT_REFRESH_TOKEN });
const yt = google.youtube({ version: 'v3', auth: oauth2 });

async function main() {
  const res = await yt.videos.insert({
    part: ['snippet','status'],
    requestBody: {
      snippet: {
        title: process.env.SONG_TITLE + ' (Lyric Video)',
        description: process.env.SONG_TITLE + '\n\nAI generated lyric video\n\n#lyricvideo #music #aimusic',
        tags: ['lyric video','music','AI music'],
        categoryId: '10',
      },
      status: {
        privacyStatus: 'unlisted',
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
