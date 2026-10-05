import {bundle} from '@remotion/bundler';
import {selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const browserExecutable=path.resolve(root,'../../node_modules/.remotion/chrome-headless-shell/win64/chrome-headless-shell-win64/chrome-headless-shell.exe');
const serveUrl=await bundle({entryPoint:path.join(root,'index.tsx'),publicDir:path.join(root,'public')});
for(const id of ['paperx','stival','marcen','recebidos','cuqui','tidle']){const composition=await selectComposition({serveUrl,id:'V2-'+id,browserExecutable});await renderMedia({composition,serveUrl,codec:'h264',outputLocation:path.resolve(root,`../assets/cases/${id}-v2.mp4`),browserExecutable,concurrency:3,crf:20});await renderStill({composition,serveUrl,frame:30,output:path.resolve(root,`../assets/cases/${id}-v2.jpg`),imageFormat:'jpeg',browserExecutable});console.log('DONE '+id)}
