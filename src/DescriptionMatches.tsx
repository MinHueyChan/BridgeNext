import {useEffect,useRef,useState} from 'react';
import {Check,Plus,Sparkles} from 'lucide-react';
import {keywordSuggestions,type Catalogue,type Profile} from './engine';
import {aiFailure,aiRequest} from './ai';
import {localize,usePreferences} from './i18n';
export default function DescriptionMatches({cat,profile,onAdd,onUnmatched}:{cat:Catalogue;profile:Profile;onAdd:(id:string)=>void;onUnmatched:(text:string)=>void}){
 const {locale}=usePreferences();const api=import.meta.env.VITE_BACKEND_ENABLED==='true';
 const [text,setText]=useState(''),[useAI,setUseAI]=useState(false),[busy,setBusy]=useState(false),[ids,setIds]=useState<string[]>([]),[mode,setMode]=useState(''),[notice,setNotice]=useState('');
 const request=useRef<AbortController|null>(null);
 useEffect(()=>()=>request.current?.abort(),[]);
 function reset(){request.current?.abort();setBusy(false);setIds([]);setMode('');setNotice('')}
 async function suggest(){
  const description=text.trim();if(!description)return;
  request.current?.abort();const controller=new AbortController();request.current=controller;setBusy(true);setIds([]);setMode('');setNotice('');const timer=setTimeout(()=>controller.abort('timeout'),17000);
  let found:string[]=[];let source='Catalogue keyword matches';let message='';
  try{
   if(useAI&&api){
    const result=await aiRequest('/api/profile/extract',{description,consent:true},controller.signal);
    if(result.mode==='gemini'){
     if(!Array.isArray(result.skill_ids)||result.skill_ids.length>8||result.skill_ids.some((id:unknown)=>typeof id!=='string'||!cat.skills.some(s=>s.id===id)))throw Error('invalid_response');
     found=[...new Set(result.skill_ids as string[])];source='Gemini suggestions — review before adding';
    }else{message=aiFailure(result.reason);found=keywordSuggestions(cat,description).map(s=>s.id)}
   }else found=keywordSuggestions(cat,description).map(s=>s.id);
  }catch(error){
   if(controller.signal.aborted&&controller.signal.reason!=='timeout')return;
   message=aiFailure(controller.signal.aborted?'timeout':error instanceof Error?error.message:undefined);found=keywordSuggestions(cat,description).map(s=>s.id);
  }finally{clearTimeout(timer)}
  if(request.current!==controller||controller.signal.aborted&&controller.signal.reason!=='timeout')return;
  setIds(found);setMode(source);setNotice(message);setBusy(false);
  if(!found.length)onUnmatched(description);
 }
 return localize(<div className="description-matches">
  <label className="ai-consent"><input type="checkbox" checked={useAI} disabled={!api} onChange={e=>{reset();setUseAI(e.target.checked)}}/>Use Gemini for this description</label>
  <p className="hint">{api?'If selected, only this description is sent to Gemini. Avoid names or contact details. Review suggestions before adding them.':'AI suggestions require the connected backend. Catalogue keyword matching is available.'}</p>
  <div className="other-input"><input aria-label="Other skill or task" maxLength={2000} placeholder="Something else? Describe a tool, skill or task…" value={text} onChange={e=>{reset();setText(e.target.value)}}/><button className="button small soft" disabled={busy||!text.trim()} onClick={suggest}>{busy?'Finding…':'Find matches'}<Sparkles size={14}/></button></div>
  {mode&&<div className="suggestion-box" role="status">{notice&&<p>{notice}</p>}<span>{mode}</span>{ids.length?<div className="small-chips">{ids.map(id=><button key={id} onClick={()=>onAdd(id)}>{cat.skills.find(s=>s.id===id)?.name}{id in profile.mastery?<Check size={12}/>:<Plus size={12}/>}</button>)}</div>:<p>No supported skills found. Your note is not included in matching.</p>}</div>}
 </div>,locale);
}
