import React from 'react';
import {AbsoluteFill, Composition, Img, OffthreadVideo, Sequence, interpolate, registerRoot, staticFile, useCurrentFrame} from 'remotion';

const ink = '#f0f2e6';
const muted = '#aebead';
const lime = '#cdf381';
const paper = '#16221c';
const panel = '#26382e';
const accent = '#ffb58b';

function Frame({label, children}) {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{background: paper, color: ink, padding: '40px 58px', fontFamily: 'Arial, sans-serif'}}>
    <div style={{display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #526457', paddingBottom: 13, fontSize: 17, fontWeight: 700, letterSpacing: 2}}>
      <span>PIXEL ASSET WORKSHOP</span><span style={{color: lime}}>{label}</span>
    </div>
    <div style={{opacity, flex: 1, display: 'flex', flexDirection: 'column'}}>{children}</div>
  </AbsoluteFill>;
}

function Headline({children, size = 58}) {
  return <div style={{font: `400 ${size}px/1.02 Georgia, serif`, letterSpacing: '-0.05em'}}>{children}</div>;
}

function Sprite({file, width}) {
  return <Img src={staticFile(file)} style={{width, imageRendering: 'pixelated', display: 'block'}} />;
}

function Opening() {
  return <Frame label="WORKFLOW">
    <div style={{display: 'grid', gridTemplateColumns: '1fr 420px', gap: 32, alignItems: 'center', flex: 1}}>
      <div>
        <Headline size={94}>One clip.<br/><span style={{color: lime}}>Six sprites.</span></Headline>
        <p style={{fontSize: 25, lineHeight: 1.4, color: muted}}>Extract transparent game frames and preview them in Godot.</p>
      </div>
      <div style={{background: panel, minHeight: 385, display: 'grid', placeItems: 'center', borderBottom: `4px solid ${lime}`}}>
        <Sprite file="clean.png" width={360}/>
      </div>
    </div>
  </Frame>;
}

function Source() {
  return <Frame label="01 / MATCH THE INPUTS">
    <div style={{display: 'grid', gridTemplateColumns: '680px 1fr', gap: 48, alignItems: 'center', flex: 1}}>
      <OffthreadVideo muted src={staticFile('source.mp4')} style={{width: '100%', border: '1px solid #526457'}} />
      <div><Headline>Video +<br/>crop layout</Headline>
        <p style={{fontSize: 23, lineHeight: 1.4, color: muted}}>The matching JSON maps a 3 × 2 grid onto the actual clip.</p>
      </div>
    </div>
  </Frame>;
}

function Compare() {
  const frame = useCurrentFrame();
  const position = interpolate(frame, [10, 52], [0, 100], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <Frame label="02 / CLEAN THE EDGES">
    <div style={{marginTop: 38}}><Headline>Remove the magenta fringe</Headline></div>
    <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginTop: 24}}>
      <div style={{background: panel, display: 'grid', placeItems: 'center', padding: 12}}>
        <div style={{fontSize: 17, color: accent, padding: 8}}>STANDARD KEY</div><Sprite file="before.png" width={340}/>
      </div>
      <div style={{background: panel, display: 'grid', placeItems: 'center', padding: 12}}>
        <div style={{fontSize: 17, color: lime, padding: 8}}>KEY + DESPILL</div>
        <div style={{position: 'relative'}}>
          <Sprite file="before.png" width={340}/>
          <div style={{position: 'absolute', inset: 0, background: panel, clipPath: `inset(0 ${100-position}% 0 0)`}}><Sprite file="clean.png" width={340}/></div>
        </div>
      </div>
    </div>
    <div style={{color: muted, fontSize: 18, marginTop: 12}}>Same exported pose · fixed crop and anchor</div>
  </Frame>;
}

function Playback() {
  return <Frame label="03 / PREVIEW IN GODOT">
    <div style={{display: 'grid', gridTemplateColumns: '748px 1fr', alignItems: 'center', gap: 32, flex: 1}}>
      <OffthreadVideo muted src={staticFile('godot.mp4')} style={{width: '100%', border: '1px solid #526457'}} />
      <div><Headline>Ready for<br/>frame review</Headline>
        <p style={{fontSize: 23, lineHeight: 1.45, color: muted}}>Six transparent sequences<br/>50 candidates per unit<br/>Nearest-neighbor playback</p>
      </div>
    </div>
  </Frame>;
}

function Showcase() {
  return <AbsoluteFill style={{background: paper}}>
    <Sequence from={0} durationInFrames={60}><Opening /></Sequence>
    <Sequence from={60} durationInFrames={84}><Source /></Sequence>
    <Sequence from={144} durationInFrames={96}><Compare /></Sequence>
    <Sequence from={240} durationInFrames={150}><Playback /></Sequence>
  </AbsoluteFill>;
}

registerRoot(() => <Composition id="PixelAssetWorkshop" component={Showcase} width={1280} height={720} fps={30} durationInFrames={390} />);
