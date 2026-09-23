const timeline=window.__timelines['signaldesk-flow'];
const viewport=document.querySelector('.player-viewport');
const scale=document.querySelector('.player-scale');
const toggle=document.querySelector('#play');
const progress=document.querySelector('#seek');
const resize=()=>{scale.style.transform=`scale(${viewport.clientWidth/1920})`;};
new ResizeObserver(resize).observe(viewport);resize();
function sync(){progress.value=timeline.time();toggle.textContent=timeline.paused()?'Play':'Pause';}
timeline.eventCallback('onUpdate',sync);
timeline.eventCallback('onComplete',()=>{timeline.pause();sync();});
toggle.addEventListener('click',()=>{if(timeline.time()>=24)timeline.restart();else timeline.paused(!timeline.paused());sync();});
document.querySelector('#replay').addEventListener('click',()=>{timeline.restart();sync();});
progress.addEventListener('input',()=>{timeline.pause().time(Number(progress.value));sync();});
if(matchMedia('(prefers-reduced-motion: reduce)').matches){timeline.time(23.9).pause();sync();}else timeline.play();
