const fs = require('fs');
const words = JSON.parse(process.env.ALIGNED_WORDS);
const title = process.env.SONG_TITLE;
const header = "[Script Info]\nScriptType: v4.00+\nPlayResX: 1280\nPlayResY: 720\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\nStyle: Default,Noto Sans CJK SC,48,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,60,60,80,1\nStyle: Title,Noto Sans CJK SC,36,&H00C9A96E,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,8,40,40,30,1\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n";

function fmt(s) {
  const h = Math.floor(s/3600);
  const m = Math.floor(s/60)%60;
  const sec = (s%60).toFixed(2).padStart(5,'0');
  return h+':'+String(m).padStart(2,'0')+':'+sec;
}

let lines = ["Dialogue: 0,0:00:00.00,0:00:05.00,Title,,0,0,0,fad(400,400)," + title];
let cur = [], i = 0;
while(i < words.length) {
  cur.push(words[i]);
  const next = words[i+1];
  if(!next || next.startS - words[i].endS > 1.2 || cur.length >= 10) {
    const start = cur[0].startS;
    const end = cur[cur.length-1].endS;
    const text = cur.map(w => {
      const cs = Math.max(1, Math.round((w.endS - w.startS)*100));
      return "{\\kf" + cs + "}" + w.word + " ";
    }).join('');
    lines.push("Dialogue: 0," + fmt(start) + "," + fmt(end) + ",Default,,0,0,0,," + text.trim());
    cur = [];
  }
  i++;
}
fs.writeFileSync('work/subs.ass', header + lines.join('\n'));
console.log('ASS generated');
