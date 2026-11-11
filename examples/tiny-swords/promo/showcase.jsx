import React from 'react';
import {
  AbsoluteFill, Composition, Easing, Img, OffthreadVideo, Sequence, interpolate,
  registerRoot, staticFile, useCurrentFrame,
} from 'remotion';
import exportManifest from '../preview/exports/manifest.json';

const fps = 30;
const ink = '#f4f5ec';
const muted = '#becfc1';
const accent = '#cef28e';
const paper = '#15241d';
const surface = '#20352a';
const rule = '#4b6353';
const easing = Easing.bezier(0.22, 1, 0.36, 1);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
const checker = 'repeating-conic-gradient(#2a4033 0% 25%, #263a2f 0% 50%) 0 0 / 24px 24px';
const editorial = 'Georgia, serif';

function reveal(frame, start = 0, length = 14) {
  return interpolate(frame, [start, start + length], [0, 1], {...clamp, easing});
}

function Stage({label, children, footer}) {
  const frame = useCurrentFrame();
  const entrance = reveal(frame, 0, 12);
  return <AbsoluteFill style={{
    color: ink, background: 'radial-gradient(ellipse at 82% 18%, #294336, #15241d 66%)',
    fontFamily: 'Arial, sans-serif',
  }}>
    <div style={{
      position: 'absolute', left: 52, right: 52, top: 30, height: 41, display: 'flex',
      justifyContent: 'space-between', borderBottom: `1px solid ${rule}`,
      fontSize: 16, fontWeight: 700, letterSpacing: 2,
    }}>
      <span>PIXEL ASSET WORKSHOP</span><span style={{color: accent}}>{label}</span>
    </div>
    <AbsoluteFill style={{opacity: entrance, transform: `translateY(${(1 - entrance) * 10}px)`}}>
      {children}
    </AbsoluteFill>
    <div style={{
      position: 'absolute', left: 52, right: 52, bottom: 28, borderTop: `1px solid ${rule}`,
      paddingTop: 13, color: muted, fontSize: 22,
    }}>{footer}</div>
  </AbsoluteFill>;
}

function Heading({children, size = 58}) {
  return <div style={{font: `400 ${size}px/1.03 ${editorial}`, letterSpacing: '-0.055em'}}>
    {children}
  </div>;
}

function Caption({children, style}) {
  return <div style={{fontSize: 24, lineHeight: 1.38, color: muted, ...style}}>{children}</div>;
}

function At({x, y, width, height, style, children}) {
  return <div style={{position: 'absolute', left: x, top: y, width, height, ...style}}>{children}</div>;
}

function Outline({rect: [x, y, width, height], start = 0, color = accent, radius = 8}) {
  const frame = useCurrentFrame();
  return <At x={x} y={y} width={width} height={height} style={{
    border: `3px solid ${color}`, borderRadius: radius, boxSizing: 'border-box',
    opacity: reveal(frame, start, 10), boxShadow: '0 0 0 1px #15241d80',
  }}/>;
}

function Click({x, y, at}) {
  const frame = useCurrentFrame();
  const approach = reveal(frame, at - 16, 16);
  const ring = interpolate(frame, [at, at + 19], [0, 1], clamp);
  const opacity = approach * (1 - reveal(frame, at + 15, 10));
  const pointer = {position: 'absolute', inset: 0, clipPath: 'polygon(0 0, 0 100%, 32% 72%, 54% 100%, 69% 91%, 50% 65%, 100% 59%)'};
  return <At x={x} y={y} width={0} height={0} style={{opacity}}>
    <div style={{
      position: 'absolute', width: 54, height: 54, left: -27, top: -27,
      borderRadius: '50%', border: '4px solid #54e794', boxSizing: 'border-box',
      transform: `scale(${0.3 + ring})`, opacity: frame >= at ? 1 - ring : 0,
    }}/>
    <div style={{
      position: 'absolute', width: 23, height: 29, left: 18 * (1 - approach), top: 21 * (1 - approach),
      filter: 'drop-shadow(0 2px 2px #17251e80)',
    }}>
      <div style={{...pointer, background: '#16221c'}}/>
      <div style={{...pointer, inset: 3, background: '#fff'}}/>
    </div>
  </At>;
}

// The camera and annotations share the screenshot's 1440 × 1040 coordinate space.
function Workbench({file, rect, camera, children}) {
  const [x, y, width, height] = rect;
  const {left, top, scale} = camera;
  return <At x={x} y={y} width={width} height={height} style={{
    overflow: 'hidden', borderRadius: 10, outline: `1px solid ${rule}`, background: '#f3f5f7',
    boxShadow: '0 16px 44px #0a160f90',
  }}>
    <div style={{
      position: 'absolute', width: 1440, height: 1040, transformOrigin: 'top left',
      transform: `translate(${-left * scale}px, ${-top * scale}px) scale(${scale})`,
    }}>
      <Img src={staticFile(file)} style={{display: 'block', width: 1440, height: 1040}}/>
      {children}
    </div>
  </At>;
}

function Opening() {
  const frame = useCurrentFrame();
  const zoom = 1 + reveal(frame, 12, 96) * 0.035;
  return <Stage label="VIDEO TO SPRITE FRAMES" footer="One batch · six units · a five-second source clip">
    <At x={52} y={195} width={487}>
      <Heading size={74}>Turn a clip into<br/><span style={{color: accent}}>game sprites.</span></Heading>
      <Caption style={{marginTop: 28, maxWidth: 438}}>
        Animate a pixel-art roster and extract transparent frames for each unit.
      </Caption>
    </At>
    <At x={548} y={153} width={680} height={385} style={{
      overflow: 'hidden', borderRadius: 10, outline: `1px solid ${rule}`,
    }}>
      <OffthreadVideo muted src={staticFile('source.mp4')} style={{
        width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`,
      }}/>
    </At>
    <At x={548} y={552} width={680} style={{fontSize: 17, color: muted}}>Actual Wan video · 3 × 2 character grid</At>
  </Stage>;
}

function Inputs() {
  const frame = useCurrentFrame();
  const pan = reveal(frame, 12, 38);
  return <Stage label="PREPARE INPUTS" footer="Compose a first frame and a motion prompt, then generate one clip for the batch.">
    <At x={52} y={91}><Heading>Load the MP4 and its crop layout</Heading></At>
    <Workbench file="extract.png" rect={[52, 168, 1176, 452]} camera={{
      left: 8 + 7 * pan, top: 207 + 16 * pan, scale: 0.825 + 0.055 * pan,
    }}>
      <Outline rect={[42, 373, 146, 45]} start={12} color="#22a667"/>
      <Click x={110} y={394} at={39}/>
      <Outline rect={[305, 282, 805, 456]} start={46} color="#22a667" radius={3}/>
    </Workbench>
    <At x={71} y={565} style={{
      background: '#15241df5', borderRadius: 6, padding: '10px 14px', color: accent,
      fontSize: 21, fontWeight: 700, opacity: reveal(frame, 32),
    }}>Import crop layout</At>
  </Stage>;
}

function Extract() {
  const frame = useCurrentFrame();
  const clean = reveal(frame, 22, 16);
  const cameraShift = reveal(frame, 46, 21);
  return <Stage label="EXTRACT FRAMES" footer="Remove the magenta background and clean up color spill along the sprite edges.">
    <At x={52} y={91}><Heading>Key out the background</Heading></At>
    <Workbench file="extract.png" rect={[52, 177, 567, 420]} camera={{
      left: 1126, top: 268 + cameraShift * 486, scale: 1.92,
    }}>
      <Outline rect={[1144, 450, 253, 35]} start={8} color="#22a667"/>
      <Click x={1158} y={467} at={22}/>
      <Outline rect={[1146, 912, 251, 52]} start={65} color="#22a667"/>
      <Click x={1271} y={936} at={79}/>
    </Workbench>
    <At x={647} y={177} width={581} height={420} style={{
      background: checker, borderRadius: 10, outline: `1px solid ${rule}`, display: 'grid', placeItems: 'center',
    }}>
      <div style={{position: 'relative', width: 420}}>
        <Img src={staticFile('before.png')} style={{width: '100%', display: 'block', imageRendering: 'pixelated'}}/>
        <div style={{position: 'absolute', inset: 0, background: checker, clipPath: `inset(0 ${100 - clean * 100}% 0 0)`}}>
          <Img src={staticFile('clean.png')} style={{width: '100%', display: 'block', imageRendering: 'pixelated'}}/>
        </div>
      </div>
      <At x={18} y={16} style={{padding: '7px 10px', borderRadius: 5, background: paper, fontSize: 17}}>
        {frame < 36 ? 'Standard key' : 'With color spill cleanup'}
      </At>
    </At>
  </Stage>;
}

function Curate() {
  const frame = useCurrentFrame();
  const pan = reveal(frame, 22, 44);
  return <Stage label="CHOOSE POSES" footer="Step through the preview, then download the selected transparent PNGs.">
    <At x={52} y={91}><Heading>Choose and reorder the poses</Heading></At>
    <Workbench file="curate.png" rect={[52, 168, 1176, 452]} camera={{
      left: 375 + 21 * pan, top: 441 + 12 * pan, scale: 1.105 + 0.025 * pan,
    }}>
      <Outline rect={[398, 541, 782, 274]} start={7} color="#22a667"/>
      <Outline rect={[1193, 540, 178, 242]} start={27} color="#22a667"/>
      <Click x={1287} y={763} at={46}/>
      <Outline rect={[1298, 507, 78, 34]} start={57} color="#22a667"/>
      <Click x={1337} y={524} at={74}/>
    </Workbench>
  </Stage>;
}

const sample = exportManifest.sequences.find((unit) => unit.name === 'Warhammer Infantry');
const [cellWidth, cellHeight] = sample.cell_size;
const sheetWidth = cellWidth * exportManifest.columns;
const sheetHeight = cellHeight * exportManifest.rows;

function Exports() {
  const frame = useCurrentFrame();
  const frameLength = sample.frames[0].duration_ms * fps / 1000;
  const index = Math.floor(frame / frameLength) % sample.frames.length;
  const [x, y] = sample.frames[index].rect_xywh;
  const sheetScale = 802 / sheetWidth;
  const previewScale = 1.4;
  return <Stage label="EXPORT GAME ASSETS" footer="The manifest records each frame's coordinates, duration and foot anchor.">
    <At x={52} y={91}><Heading>Pack a sprite sheet and a GIF</Heading></At>
    <At x={52} y={180} width={830} height={405} style={{borderRadius: 10, background: surface, outline: `1px solid ${rule}`}}>
      <At x={14} y={15} style={{fontSize: 20, fontWeight: 700}}>Transparent PNG sprite sheet</At>
      <At x={14} y={59} width={802} height={sheetHeight * sheetScale} style={{background: checker}}>
        <Img src={staticFile(sample.sheet)} style={{width: '100%', display: 'block', imageRendering: 'pixelated'}}/>
        <Outline rect={[x * sheetScale, y * sheetScale, cellWidth * sheetScale, cellHeight * sheetScale]} radius={0}/>
      </At>
      <At x={14} y={300} width={785}>
        <Caption>12 action poses · 6 × 2 cells<br/>Read left to right, then top to bottom.</Caption>
      </At>
    </At>
    <At x={900} y={180} width={328} height={405} style={{borderRadius: 10, background: surface, outline: `1px solid ${rule}`, overflow: 'hidden'}}>
      <At x={14} y={15} style={{fontSize: 20, fontWeight: 700}}>GIF playback</At>
      <At x={0} y={59} width={328} height={264} style={{background: checker, overflow: 'hidden'}}>
        <At x={(328 - cellWidth * previewScale) / 2} y={(264 - cellHeight * previewScale) / 2}
          width={cellWidth * previewScale} height={cellHeight * previewScale} style={{overflow: 'hidden'}}>
          <Img src={staticFile(sample.sheet)} style={{
            display: 'block', position: 'absolute', left: -x * previewScale, top: -y * previewScale,
            width: sheetWidth * previewScale, imageRendering: 'pixelated',
          }}/>
        </At>
      </At>
      <At x={14} y={345} style={{fontSize: 20, color: muted}}>200 ms per frame</At>
    </At>
  </Stage>;
}

function Godot() {
  const frame = useCurrentFrame();
  const captureScale = 1 + 0.02 * reveal(frame, 3, 105);
  return <Stage label="CHECK IN ENGINE" footer="Try the included MP4 and layout in the repository.">
    <At x={52} y={175} width={327}>
      <Heading size={64}>Compare<br/>in Godot</Heading>
      <Caption style={{marginTop: 30}}>Original Tiny Swords units on top.<br/><br/>Generated units below.</Caption>
      <Caption style={{marginTop: 23, fontSize: 16}}>Tiny Swords art by Pixel Frog</Caption>
    </At>
    <At x={390} y={99} width={838} height={533} style={{
      overflow: 'hidden', borderRadius: 10, outline: `1px solid ${rule}`,
    }}>
      <div style={{position: 'relative', width: '100%', height: '100%', transform: `scale(${captureScale})`}}>
        <OffthreadVideo muted src={staticFile('training-ground.mp4')} style={{width: '100%', height: '100%'}}/>
        <Outline rect={[39, 142, 760, 119]} start={14} radius={4}/>
        <Outline rect={[39, 278, 760, 144]} start={42} radius={4}/>
      </div>
    </At>
  </Stage>;
}

const cuts = [
  [0, Opening],
  [99, Inputs],
  [216, Extract],
  [315, Curate],
  [408, Exports],
  [510, Godot],
];
const duration = 645;

function Showcase() {
  return <AbsoluteFill style={{background: paper}}>
    {cuts.map(([from, Shot], index) => (
      <Sequence key={from} from={from} durationInFrames={(cuts[index + 1]?.[0] ?? duration) - from}>
        <Shot/>
      </Sequence>
    ))}
  </AbsoluteFill>;
}

registerRoot(() => (
  <Composition id="PixelAssetWorkshop" component={Showcase} width={1280} height={720} fps={fps} durationInFrames={duration}/>
));
