const fs = require('fs');
const words = JSON.parse(process.env.ALIGNED_WORDS);
const title = process.env.SONG_TITLE;

const header = "[Script Info]\nScriptType: v4.00+\nPlayResX: 1280\nPlayResY: 720\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\nStyle: Default,Noto Sans CJK SC,48,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,60,60,80,1\nStyle: Prev,Noto Sans CJK SC,32,&H88AAAAAA,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,2,60,60,120,1\nStyle: Next,Noto Sans CJK SC,32,&H88AAAAAA,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,2,60,60,40,1\nStyle: Title,Noto Sans CJK SC,36,&H00C9A96E,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,8,40,40,30,1\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n";

function fmt(s) {
  const h = Math.floor(s/3600);
  const m = Math.floor(s/60)%60;
  const sec = (s%60).toFixed(2).padStart(5,'0');
  return h+':'+String(m).padStart(2,'0')+':'+sec;
}

function cleanWord(w) {
  return (w || '').replace(/\n/g, '').replace(/\\/g, '').trim();
}

// 제목
let lines = ["Dialogue: 0,0:00:00.00,0:00:05.00,Title,,0,0,0,fad(400,400)," + title];

// 각 word가 이미 라인 단위이므로 그대로 사용
for (let i = 0; i < words.length; i++) {
  const w = words[i];
  const text = cleanWord(w.word);
  if (!text) continue;

  const start = w.startS || 0;
  const end = w.endS || (start + 2);
  const prev = i > 0 ? cleanWord(words[i-1].word) : '';
  const next = i < words.length-1 ? cleanWord(words[i+1].word) : '';

  // 이전 줄 (작게, 위)
  if (prev) {
    lines.push("Dialogue: 0," + fmt(start) + "," + fmt(end) + ",Prev,,0,0,0,," + prev);
  }
  // 현재 줄 (크게, 중앙)
  lines.push("Dialogue: 0," + fmt(start) + "," + fmt(end) + ",Default,,0,0,0,," + text);
  // 다음 줄 (작게, 아래)
  if (next) {
    lines.push("Dialogue: 0," + fmt(start) + "," + fmt(end) + ",Next,,0,0,0,," + next);
  }
}

fs.writeFileSync('work/subs.ass', header + lines.join('\n'));
console.log('ASS generated, lines: ' + lines.length);
