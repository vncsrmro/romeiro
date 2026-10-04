import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg','.ttf':'font/ttf','.mp4':'video/mp4','.webm':'video/webm'};
http.createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');let file=path.resolve(root,'.'+decodeURIComponent(url.pathname));if(file!==root&&!file.startsWith(root+path.sep))throw Error();const stat=await fs.stat(file);if(stat.isDirectory())file=path.join(file,'index.html');const body=await fs.readFile(file);const type=types[path.extname(file)];if(!type)throw Error();res.writeHead(200,{'content-type':type,'cache-control':'no-cache'});res.end(body)}catch{res.writeHead(404,{'content-type':'text/plain; charset=utf-8'});res.end('Página não encontrada.')}}).listen(4390,'127.0.0.1',()=>console.log('Romeiro v2: http://127.0.0.1:4390'));
