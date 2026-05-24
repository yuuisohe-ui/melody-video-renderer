const fs = require('fs');
const words = JSON.parse(process.env.ALIGNED_WORDS);

const header = "[Script Info]\nScriptType: v4.00+\nPlayResX: 1280\nPlayResY: 720\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\nStyle: Default,Noto Sans CJK SC,58,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,5,0,0,0,1\nStyle: Prev,Noto Sans CJK SC,38,&H88AAAAAA,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,5,0,0,0,1\nStyle: Next,Noto Sans CJK SC,38,&H88AAAAAA,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,5,0,0,0,1\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n";

function fmt(s) {
  const h = Math.floor(s/3600);
  const m = Math.floor(s/60)%60;
  const sec = (s%60).toFixed(2).padStart(5,'0');
  return h+':'+String(m).padStart(2,'0')+':'+sec;
}

function cleanWord(w) {
  return (w || '').replace(/\n/g, '').replace(/\\/g, '').trim();
}

let lines = [];

for (let i = 0; i < words.length; i++) {
  const w = words[i];
  const text = cleanWord(w.word);
  if (!text) continue;

  const start = w.startS || 0;
  const end = w.endS || (start + 2);
  const prev = i > 0 ? cleanWord(words[i-1].word) : '';
  const next = i < words.length-1 ? cleanWord(words[i+1].word) : '';

  // 上一行（灰色，上方）
  if (prev) {
    lines.push("Dialogue: 0," + fmt(start) + "," + fmt(end) + ",Prev,,0,0,0,{\\pos(900,260)}," + prev);
  }
  // 当前行（白色大字，中间）
  lines.push("Dialogue: 0," + fmt(start) + "," + fmt(end) + ",Default,,0,0,0,{\\pos(900,370)}," + text);
  // 下一行（灰色，下方）
  if (next) {
    lines.push("Dialogue: 0," + fmt(start) + "," + fmt(end) + ",Next,,0,0,0,{\\pos(900,480)}," + next);
  }
}

fs.writeFileSync('work/subs.ass', header + lines.join('\n'));
console.log('ASS generated, lines: ' + lines.length);
