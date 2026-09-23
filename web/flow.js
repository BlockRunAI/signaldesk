(function(){
const tl=gsap.timeline({paused:true,defaults:{ease:'power3.out',duration:.7}});
const show=(s,t,d=.65)=>tl.fromTo(s,{opacity:0,y:14},{opacity:1,y:0,duration:d},t);
show('.product',.25);show('.run-tag',.5);show('.column-title',.6);show('.feed-window',1);show('.engine',1.3);show('.output-shell',1.5);show('.waiting',1.6);
tl.fromTo('.feed',{y:0},{y:-744,duration:6.4,ease:'sine.inOut'},1.5);
tl.fromTo('.winner-outline',{opacity:0},{opacity:1,duration:.5},7.6);
tl.fromTo('.post.match',{backgroundColor:'#ffffff'},{backgroundColor:getComputedStyle(document.documentElement).getPropertyValue('--blue-soft').trim(),duration:.6},7.7);
show('.feed-foot',3);show('.classification',8.6);
for(let i=0;i<5;i++){tl.fromTo('.one .packet',{x:0,opacity:0},{x:48,opacity:1,duration:.6,ease:'none'},4+i*.65);tl.to('.one .packet',{opacity:0,duration:.12},4.6+i*.65);}
show('.checks',9.5);tl.fromTo('.fill.intent',{scaleX:0},{scaleX:.92,duration:1.1,ease:'power2.inOut'},9);
tl.fromTo('.fill.fit',{scaleX:0},{scaleX:.85,duration:1.1,ease:'power2.inOut'},9.55);
tl.fromTo('.fill.confidence',{scaleX:0},{scaleX:.94,duration:1.1,ease:'power2.inOut'},10.1);
show('.check-value',9.3);show('.scoreline',11.1);show('.model-result',11.5);show('.engine-note',11.7);
tl.fromTo('.flight',{opacity:0,x:0,y:0,scale:.88},{opacity:1,x:0,y:0,scale:1,duration:.3},8);
tl.to('.flight',{x:642,y:-235,duration:1.15,ease:'power2.inOut'},8.3);
tl.to('.flight',{opacity:0,duration:.3},9.25);
tl.fromTo('.two .packet',{x:0,opacity:0},{x:55,opacity:1,duration:.7,ease:'none'},12);
tl.to('.two .packet',{opacity:0,duration:.2},12.7);
tl.to('.waiting',{opacity:0,y:-8,duration:.35},12.3);
tl.fromTo('.result',{opacity:0,x:-40,y:0,scale:.97},{opacity:1,x:0,y:0,scale:1,duration:1,ease:'power3.out'},12.5);
show('.quote',12.9);show('.context',13.3);show('.source',13.7);
tl.fromTo('.draft',{opacity:0,y:20,clipPath:'inset(0 0 100% 0)'},{opacity:1,y:0,clipPath:'inset(0 0 0% 0)',duration:1.2,ease:'power2.inOut'},15);
show('.output-note',16.1);show('.bottom strong',17);
tl.fromTo('.headline',{opacity:1,y:0},{opacity:0,y:-20,duration:.6},18);
tl.fromTo('.title-summary',{opacity:0,y:20},{opacity:1,y:0,duration:.8},18.35);
['.phase-a','.phase-b','.phase-c','.phase-d'].forEach((s,i)=>{const t=[0,3,8.3,12.5][i];tl.fromTo(s,{opacity:0,y:7},{opacity:1,y:0,duration:.4},t);if(i<3)tl.to(s,{opacity:0,y:-7,duration:.3},[2.7,8,12.2][i]);});
tl.fromTo('.journey-fill',{scaleX:0},{scaleX:1,duration:24,ease:'none'},0);
// Keep the approved 24-second main animation intact; add brand bookends.
tl.paused(false);
const launch=gsap.timeline({paused:true,defaults:{ease:'power3.out'}});
launch.add(tl,4);
launch.fromTo('.main-stage',{opacity:0},{opacity:1,duration:.8},4);
launch.fromTo('.launch-kicker',{opacity:0,y:14},{opacity:1,y:0,duration:.6},.1);
launch.fromTo('.launch-partners',{opacity:0,y:24,scale:.94},{opacity:1,y:0,scale:1,duration:.9},.2);
launch.to('.launch-partners',{y:-130,scale:.62,duration:.8,ease:'power2.inOut'},1.65);
launch.to('.launch-kicker',{opacity:0,duration:.4},1.55);
launch.fromTo('.launch-product',{opacity:0,y:30},{opacity:1,y:0,duration:.8},1.9);
launch.fromTo('.launch-line',{opacity:0,y:15},{opacity:1,y:0,duration:.6},2.5);
launch.to('.launch-cover',{opacity:0,y:-24,duration:.7,ease:'power2.inOut'},3.7);
launch.set('.launch-cover',{pointerEvents:'none'},4.4);
launch.to('.main-stage',{opacity:0,duration:.4},27.1);
launch.fromTo('.closing-cover',{opacity:0,pointerEvents:'none'},{opacity:1,duration:.7},27.6);
launch.set('.closing-cover',{pointerEvents:'auto'},28.3);
launch.fromTo('.closing-inner',{y:22},{y:0,duration:.9},27.7);
launch.to('.closing-inner',{opacity:1,duration:3.4,ease:'none'},28.6);
window.__timelines=window.__timelines||{};window.__timelines['signaldesk-flow']=launch;

})();
