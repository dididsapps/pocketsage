// Extrait toutes les phrases du Coach Sportif depuis index.html (pour gen_sport_mp3.py).
// Usage : node tools/sport_texts.js  → JSON (liste de phrases) sur la sortie standard.
const fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const {allTexts}=require(path.join(root,'js','coach-voix.js'));
function block(re,name){const m=html.match(re);if(!m)throw new Error('introuvable : '+name);return (new Function('return '+m[1]))();}
const defis=block(/\ndefis:(\[[\s\S]*?\n\]),?/,'defis');
const plans=block(/const COACH_PLANS = (\{[\s\S]*?\n\});/,'COACH_PLANS');
const phases=block(/const COACH_PHASE_NAMES = (\{[\s\S]*?\n\});/,'COACH_PHASE_NAMES');
const msgs=block(/const COACH_MSGS = (\{[\s\S]*?\n\});/,'COACH_MSGS');
process.stdout.write(JSON.stringify(allTexts(defis,plans,phases,msgs)));
