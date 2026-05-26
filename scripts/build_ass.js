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

const sentences = [];
let cur = [];

for (let i = 0; i < words.length; i++) {
  const w = words[i];
  w.startS = w.startS ?? w.start_s ?? 0;
  w.endS = w.endS ?? w.end_s ?? 0;
  if (w.word === ' ') continue;
  if (!w.success && w.success !== undefined) continue;
  const text = cleanWord(w.word);
  if (!text) continue;
  cur.push(w);
  if (w.word.includes('\n')) {
    sentences.push(cur);
    cur = [];
  }
}
if (cur.length > 0) sentences.push(cur);

let lines = [];

for (let i = 0; i < sentences.length; i++) {
  const sent = sentences[i];
  const start = i === 0 ? 0 : sent[0].startS;
  const end = i < sentences.length-1
    ? (sentences[i+1][0].startS || sentences[i+1][0].start_s || sent[sent.length-1].endS)
    : sent[sent.length-1].endS;
  const text = sent.map(w => cleanWord(w.word)).join(' ');
  const prev = i > 0 ? sentences[i-1].map(w => cleanWord(w.word)).join(' ') : '';
  const next = i < sentences.length-1 ? sentences[i+1].map(w => cleanWord(w.word)).join(' ') : '';

  if (prev) lines.push(`Dialogue: 0,${fmt(start)},${fmt(end)},Prv,,0,0,0,,{\\an5\\pos(950,260)}${prev}`);
  lines.push(`Dialogue: 0,${fmt(start)},${fmt(end)},Cur,,0,0,0,,{\\an5\\pos(950,360)}${text}`);
  if (next) lines.push(`Dialogue: 0,${fmt(start)},${fmt(end)},Nxt,,0,0,0,,{\\an5\\pos(950,460)}${next}`);
}

fs.writeFileSync('work/subs.ass', header + lines.join('\n'));
console.log('ASS generated: ' + lines.length);
