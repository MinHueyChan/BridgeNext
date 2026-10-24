/** Client-side extraction only. Files are never posted to the application API. */
async function deadline<T>(work:Promise<T>,ms:number):Promise<T>{let timer:ReturnType<typeof setTimeout>|undefined;try{return await Promise.race([work,new Promise<T>((_,reject)=>{timer=setTimeout(()=>reject(new Error('Reading took too long. Paste the CV text or continue manually.')),ms)})])}finally{if(timer)clearTimeout(timer)}}
export async function extractCV(file:File,progress:(s:string)=>void):Promise<string>{
 if(file.size>8*1024*1024)throw Error('Please choose a file smaller than 8 MB.');
 async function ocr(images:(File|HTMLCanvasElement)[]){progress('Loading English OCR…');const {createWorker}=await import('tesseract.js');const creation=createWorker('eng');let worker:Awaited<typeof creation>|undefined;try{worker=await deadline(creation,60000);let text='';for(let i=0;i<images.length;i++){progress(`Reading page image ${i+1} of ${images.length}…`);text+=(await deadline(worker.recognize(images[i]),60000)).data.text+'\n'}return text}finally{if(worker)await worker.terminate();else creation.then(w=>w.terminate()).catch(()=>{})}}
 let text='';
 if(file.type==='application/pdf'||file.name.toLowerCase().endsWith('.pdf')){
  progress('Reading PDF text…');const pdfjs=await import('pdfjs-dist');pdfjs.GlobalWorkerOptions.workerSrc=new URL('pdfjs-dist/build/pdf.worker.min.mjs',import.meta.url).href;
  const loading=pdfjs.getDocument({data:await file.arrayBuffer()});let doc:Awaited<typeof loading.promise>|undefined;
  try{doc=await deadline(loading.promise,45000);for(let n=1;n<=Math.min(doc.numPages,3);n++){const page=await doc.getPage(n);const content=await deadline(page.getTextContent(),20000);text+=content.items.map(i=>'str' in i?i.str:'').join(' ')+'\n'}if(text.trim().length<30){const images:HTMLCanvasElement[]=[];for(let n=1;n<=Math.min(doc.numPages,2);n++){const page=await doc.getPage(n);const viewport=page.getViewport({scale:1.5});const canvas=document.createElement('canvas');canvas.width=viewport.width;canvas.height=viewport.height;await page.render({canvas,viewport}).promise;images.push(canvas)}text=await ocr(images)}}finally{await loading.destroy()}
 }else if(file.type.startsWith('image/'))text=await ocr([file]);else text=await file.text();
 if(text.trim().length<10)throw Error('No readable text found. Paste the text or continue manually.');
 return text.slice(0,6000);
}
