const fs = require('fs');
const words = JSON.parse(process.env.ALIGNED_WORDS);

function fmt(s) {
  const h = Math.floor(s/3600);
  const m = Math.floor(s/60)%60;
  const sec = (s%60).toFixed(2).padStart(5,'0');
  return h+':'+String(m).padStart(2,'0')+':'+sec;
}

function cleanWord(w) {
  return (w || '').replace(/\n/g, '').replace(/\\/g, '').trim();
}

const header = `[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cur,Noto Sans CJK SC,64,&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,1,5,0,0,0,1
Style: Prv,Noto Sans CJK SC,42,&H88AAAAAA,&H0000FFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,1,5,0,0,0,1
Style: Nxt,Noto Sans CJK SC,42,&H88AAAAAA,&H0000FFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,1,5,0,0,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
`;

let lines = [];

for (let i = 0; i < words.length; i++) {
  const text = cleanWord(words[i].word);
  if (!text) continue;
  const start = i === 0 ? 0 : (words[i].startS || 0);
  const end = i < words.length-1 ? (words[i+1].startS || words[i].endS) : words[i].endS;
  const prev = i > 0 ? cleanWord(words[i-1].word) : '';
  const next = i < words.length-1 ? cleanWord(words[i+1].word) : '';

  if (prev) lines.push(`Dialogue: 0,${fmt(start)},${fmt(end)},Prv,,0,0,0,,{\\an5\\pos(950,260)}${prev}`);
  lines.push(`Dialogue: 0,${fmt(start)},${fmt(end)},Cur,,0,0,0,,{\\an5\\pos(950,360)}${text}`);
  if (next) lines.push(`Dialogue: 0,${fmt(start)},${fmt(end)},Nxt,,0,0,0,,{\\an5\\pos(950,460)}${next}`);
}

fs.writeFileSync('work/subs.ass', header + lines.join('\n'));
console.log('ASS generated: ' + lines.length);
