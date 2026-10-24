import {useEffect,useRef,useState} from 'react';
import {Sparkles} from 'lucide-react';
import type {Catalogue,Profile} from './engine';
import {localize,usePreferences} from './i18n';
import {aiFailure,aiRequest} from './ai';
type Result={mode:'gemini'|'template';reason?:string;summary:string;skill_notes:{skill_id:string;explanation:string}[];resource_note:{resource_id:string;explanation:string}|null};
export default function AIExplanation({profile,cat,selected,month,scenario,goal='future'}:{profile:Profile;cat:Catalogue;selected:string;month:string;scenario:string;goal?:'current'|'future'}){
 const {locale}=usePreferences();const api=import.meta.env.VITE_BACKEND_ENABLED==='true';
 // The provider never needs a name, custom occupation, experience text or CV.
 const input={profile:{mastery:profile.mastery,tasks:profile.tasks,interests:profile.interests,hours:profile.hours,confirmed:profile.confirmed},selected,month,scenario,goal,locale,consent:true};
 const key=JSON.stringify({...input,revision:cat.evidence.retrieved_at});const request=useRef<AbortController|null>(null);
 const [output,setOutput]=useState<{key:string;result:Result}|null>(null),[pending,setPending]=useState(''),[failure,setFailure]=useState<{key:string;reason:string}|null>(null);
 useEffect(()=>{request.current?.abort();setOutput(null);setFailure(null);setPending('');return()=>request.current?.abort()},[key]);
 const result=output?.key===key?output.result:null;const busy=pending===key;
 async function explain(){
  request.current?.abort();const controller=new AbortController();request.current=controller;setPending(key);setFailure(null);setOutput(null);const timer=setTimeout(()=>controller.abort('timeout'),17000);
  try{
   const data=await aiRequest('/api/explanations',input,controller.signal);
   if(!['gemini','template'].includes(data.mode)||typeof data.summary!=='string'||!Array.isArray(data.skill_notes)||data.skill_notes.some((n:Result['skill_notes'][number])=>!cat.skills.some(s=>s.id===n.skill_id)||typeof n.explanation!=='string')||data.resource_note&&(!cat.resources.some(r=>r.id===data.resource_note.resource_id)||typeof data.resource_note.explanation!=='string'))throw Error('invalid_response');
   if(request.current===controller&&!controller.signal.aborted)setOutput({key,result:data});
  }catch(error){if(request.current===controller&&(!controller.signal.aborted||controller.signal.reason==='timeout'))setFailure({key,reason:controller.signal.aborted?'timeout':error instanceof Error?error.message:'unavailable'})}
  finally{clearTimeout(timer);if(request.current===controller)setPending('')}
 }
 return localize(<details className="ai-explanation"><summary><Sparkles size={15}/>Understand this recommendation</summary>
  <p className="hint">Gemini can explain the calculated results. Only skill ratings, interests, selected tasks and learning settings are shared; your name and CV are excluded.</p>
  <button className="button soft small" disabled={!api||!profile.confirmed||busy} onClick={explain}>{busy?'Preparing explanation…':result?'Ask Gemini again':'Ask Gemini to explain'}</button>
  {!api&&<p className="hint">AI explanations require the connected backend. The scores, priorities and learning steps shown here remain available.</p>}
  {(result||failure?.key===key)&&<div className="ai-explanation-result" role="status"><span className="tag green">{result?.mode==='gemini'?'AI explanation · Gemini':'Standard explanation'}</span>
   {(failure?.key===key||result?.reason)&&<p className="hint">{aiFailure(failure?.key===key?failure.reason:result?.reason)}</p>}
   {result?<><p translate="no">{result.summary}</p>{result.skill_notes.length>0&&<ul>{result.skill_notes.map(note=><li key={note.skill_id}><strong>{cat.skills.find(s=>s.id===note.skill_id)?.name}</strong><p translate="no">{note.explanation}</p></li>)}</ul>}{result.resource_note&&<p><strong>{cat.resources.find(r=>r.id===result.resource_note?.resource_id)?.name}</strong><br/><span translate="no">{result.resource_note.explanation}</span></p>}</>:<p>The existing scores, priorities and learning steps are the standard explanation. You can continue planning.</p>}
   <p className="hint">{result?.mode==='gemini'?'AI wording can be imperfect. Check it against the scores and sources. It does not change your profile or recommendations.':'This is standard guidance, not a generated AI response.'}</p>
  </div>}
 </details>,locale);
}
