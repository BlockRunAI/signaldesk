const timeline=window.__timelines['signaldesk-flow'];
const viewport=document.querySelector('.player-viewport');
const scale=document.querySelector('.player-scale');
const toggle=document.querySelector('#play');
const progress=document.querySelector('#seek');
const music=document.querySelector('#browser-music');
const sound=document.querySelector('#sound');
const duration=Number(progress.max);
let hasStarted=false;
const resize=()=>{scale.style.transform=`scale(${viewport.clientWidth/1920})`;};
new ResizeObserver(resize).observe(viewport);resize();
function sync(){progress.value=timeline.time();toggle.textContent=timeline.paused()?'Play with sound':'Pause';}
function play(){if(!hasStarted||timeline.time()>=duration-.1)timeline.time(0);hasStarted=true;music.currentTime=timeline.time();timeline.play();music.play().catch(()=>{sound.textContent='Enable sound';});sync();}
timeline.eventCallback('onUpdate',sync);
timeline.eventCallback('onComplete',()=>{timeline.pause();music.pause();sync();});
toggle.addEventListener('click',()=>{if(timeline.paused())play();else{timeline.pause();music.pause();sync();}});
document.querySelector('#replay').addEventListener('click',()=>{timeline.time(0);play();});
progress.addEventListener('input',()=>{hasStarted=true;timeline.pause().time(Number(progress.value));music.pause();music.currentTime=timeline.time();sync();});
sound.addEventListener('click',()=>{music.muted=!music.muted;sound.textContent=music.muted?'Sound off':'Sound on';if(!timeline.paused()&&!music.muted)music.play().catch(()=>{});});
timeline.time(matchMedia('(prefers-reduced-motion: reduce)').matches?duration-.1:.85).pause();
sync();
