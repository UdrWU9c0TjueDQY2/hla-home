'use strict';
function model(n,p){if(!Number.isInteger(n)||n<0||n>9999||![10,100].includes(p))return null;const lo=Math.floor(n/p)*p,hi=lo+p,a=n-lo,b=hi-n;return{n,p,lo,hi,mid:lo+p/2,a,b,answer:a<b?lo:hi,pct:a/p*100};}
const $=id=>document.getElementById(id),cards=[[42,10],[78,10],[65,10],[350,100],[400,100],[999,100]];
let state=null,card=-1,answered=false;
function setAnswerLock(locked) {
  for (const id of ['lower', 'upper']) $(id).setAttribute('aria-disabled', String(locked));
}
function draw(){setAnswerLock(false);const raw=$('number').value.trim();state=raw===''?null:model(Number(raw),Number($('place').value));$('error').textContent=state?'':'Enter a whole number from 0 to 9,999.';$('workspace').hidden=!state;$('feedback').textContent='';$('next').hidden=true;answered=false;if(!state)return;const s=state;$('mode').textContent=card<0?'EXPLORE YOUR OWN NUMBER':'PRACTICE CARD '+(card+1)+' OF 6';$('prompt').textContent='Round '+s.n+' to the nearest '+s.p+'.';$('lower-label').textContent=s.lo;$('upper-label').textContent=s.hi;$('middle-label').textContent=s.mid+' halfway';$('lower').textContent=s.lo;$('upper').textContent=s.hi;$('marker').style.left=s.pct+'%';$('line').setAttribute('aria-label','Number line from '+s.lo+' to '+s.hi+', midpoint '+s.mid+', number '+s.n);$('distances').textContent=s.n+' is '+s.a+' away from '+s.lo+' and '+s.b+' away from '+s.hi+'.';}
function choose(which){if(!state || (card >= 0 && answered))return;const s=state,v=which==='lower'?s.lo:s.hi;const reason=s.a===0?'It is already a multiple of '+s.p+', so it stays the same.':s.a===s.b?'The distances are equal. At halfway, this lab rounds to the higher multiple.':'It is closer to '+s.answer+'.';if(v!==s.answer){$('feedback').textContent='Take another look. '+reason+' Try the other answer.';return;}$('feedback').textContent=s.n+' rounds to '+s.answer+'. '+reason;answered=true;if(card>=0){setAnswerLock(true);$('next').hidden=card===5;$('progress').textContent=card===5?'Six cards complete. Explain one answer in your own words, or start again.':'Card '+(card+1)+' complete. Continue when ready.';}}
$('lower').addEventListener('click',()=>choose('lower'));$('upper').addEventListener('click',()=>choose('upper'));
function explore(){card=-1;$('progress').textContent='';draw();}
$('show').addEventListener('click',explore);
['number','place'].forEach(id=>$(id).addEventListener('input',explore));
function setCard(){const c=cards[card];$('number').value=c[0];$('place').value=c[1];draw();$('progress').textContent='Card '+(card+1)+' of 6. No timer; use the distances.';$('lower').focus();}
$('practice').addEventListener('click',()=>{card=0;setCard();});
$('next').addEventListener('click',()=>{if(answered&&card>=0&&card<5){card++;setCard();}});
$('reset').addEventListener('click',()=>{$('number').value=47;$('place').value=10;explore();});draw();
