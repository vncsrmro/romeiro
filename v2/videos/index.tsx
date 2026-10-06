import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Composition,Img,continueRender,delayRender,interpolate,registerRoot,staticFile,useCurrentFrame,Easing} from 'remotion';
const projects=[
{id:'paperx',name:'PaperX',label:'IDENTIDADE / PRODUTO / IA',title:'O trabalho em campo, conectado.',main:'paperx.webp',detail:'paperx-app.webp',bg:'#d4deca'},
{id:'stival',name:'Stival',label:'ESTRATÉGIA / IDENTIDADE / WEBSITE',title:'Precisão com sensibilidade.',main:'stival.webp',detail:'brand/stival-10.png',bg:'#d7d9cb'},
{id:'marcen',name:'Marcen',label:'IDENTIDADE / WEBSITE / ERP',title:'Da oficina à entrega.',main:'marcen.webp',detail:'brand/marcen-aplicacoes.png',bg:'#d1d8c0'},
{id:'recebidos',name:'Recebidos do Bem',label:'IDENTIDADE / CAMPANHA / SISTEMA',title:'Um gesto que vira identidade.',main:'recebidos.webp',detail:'recebidos-aplicacoes.webp',bg:'#ddd2bf'},
{id:'cuqui',name:'CUQUI',label:'DIREÇÃO VISUAL / EXPERIÊNCIA DIGITAL',title:'Personalidade em cada detalhe.',main:'cuqui.webp',detail:'brand/cuqui-cookie-assorted.jpg',bg:'#d3cec0'},
{id:'tidle',name:'TIDLE',label:'IDENTIDADE / UNIVERSO DIGITAL',title:'Um universo para explorar.',main:'brand/tidle-cinematic.png',detail:'brand/tidle-hunt-amazon.png',bg:'#c9cebd'}
];
type Project=typeof projects[number];
const Film:React.FC<{project:Project}>=({project:p})=>{
  const frame=useCurrentFrame();
  const mix=interpolate(frame,[0,72,94,153,179],[0,0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.ease)});
  const drift=Math.sin(frame/180*Math.PI*2)*8;
  return (
    <AbsoluteFill style={{background:p.bg,overflow:'hidden'}}>
      <div style={{position:'absolute',inset:0,opacity:1-mix,display:'flex',alignItems:'center',justifyContent:'center',padding:'30px 90px',transform:`translateY(${drift}px)`}}>
        <Img src={staticFile('cases/'+p.main)} style={{width:'100%',height:'100%',objectFit:'contain',filter:'drop-shadow(0 15px 40px #0000001a)'}}/>
      </div>
      <div style={{position:'absolute',inset:0,opacity:mix,display:'flex',alignItems:'center',justifyContent:'center',gap:30,padding:30,transform:`translateY(${-drift}px)`}}>
        <Img src={staticFile('cases/'+p.main)} style={{width:'48%',height:'100%',objectFit:'contain',filter:'drop-shadow(0 15px 40px #0000001a)'}}/>
        <Img src={staticFile('cases/'+p.detail)} style={{width:'48%',height:'100%',objectFit:'contain',filter:'drop-shadow(0 15px 40px #0000001a)'}}/>
      </div>
    </AbsoluteFill>
  );
};
registerRoot(()=> <>{projects.map(project=><Composition key={project.id} id={`V2-${project.id}`} component={Film} defaultProps={{project}} durationInFrames={180} fps={30} width={1280} height={800}/>)}</>);
