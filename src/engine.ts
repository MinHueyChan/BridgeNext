export interface Skill {id:string;name:string;group:string;description:string;sdg:string;sdg_reason:string}
export interface Task {id:string;name:string;description:string;skills:string[];node_id:string;source_task:string;observations:Record<string,{automation:number|null;augmentation:number|null;usage:number|null}>;mapping_note:string}
export interface Role {id:string;name:string;subtitle:string;code:string;family:string;icon:string;sdg:string[];sdg_reason:string;interests:string[];qualification:string;weights:Record<string,number>;source:string}
export interface Resource {id:string;name:string;provider:string;url:string|null;skills:string[];hours:number;cost:number;access:string;note:string}
export interface Profile {name:string;title:string;experience:string;hours:number;interests:string[];tasks:string[];mastery:Record<string,number>;confirmed:boolean;avatarId?:number}
export interface Catalogue {skills:Skill[];tasks:Task[];roles:Role[];resources:Resource[];personas:Record<string,Profile>;evidence:{source_url:string;release:string;retrieved_at:string;geography:string;kind:string;months:string[];caveat:string;metric:string;mapping:string;revision?:string;period_sources?:Record<string,{url:string;release:string}>}}
export interface Match {role:Role;score:number;baseline:number;trend:number;interest:number;coverage:number;hasTrend:boolean;gaps:{skill:Skill;priority:number;mastery:number}[];weights:Record<string,number>}
const round=(n:number)=>Math.round(n*10)/10;
export function adjusted(cat:Catalogue,role:Role,month:string,scenario:string){
 const out:Record<string,number>={};
 for(const [id,w] of Object.entries(role.weights)){
  const links=cat.tasks.filter(t=>t.skills.includes(id));
  const ds=['ai_verification','critical_thinking','risk_controls','exception_handling','data_validation'].includes(id)?1:['excel','recordkeeping','reconciliation','payment_followup','reporting'].includes(id)?-1:0;
  const factors=links.map(t=>{const a=t.observations[month]?.automation;if(a===null||a===undefined)return 1;const evidenceFactor=1+.1*ds*(a/100);return evidenceFactor*(scenario==='fast'?1+.2*ds:1)});
  out[id]=w*(factors.length?factors.reduce((a,b)=>a+b,0)/factors.length:1);
 }
 const total=Object.values(out).reduce((a,b)=>a+b,0);for(const id in out)out[id]/=total;return out;
}
export function matches(cat:Catalogue,p:Profile,month:string,scenario:string):Match[]{
 const covers=cat.roles.map(r=>{const links=cat.tasks.filter(t=>t.skills.some(s=>s in r.weights));return links.length?links.filter(t=>t.observations[month]?.automation!=null).length/links.length:0});
 const usable=covers.every(c=>c>=.5);
 return cat.roles.map((role,idx)=>{
  const sum=Object.values(role.weights).reduce((a,b)=>a+b,0);const baseline=Object.entries(role.weights).reduce((v,[s,w])=>v+w*(p.mastery[s]||0),0)/sum;
  const weights=adjusted(cat,role,month,scenario);const trend=Object.entries(weights).reduce((v,[s,w])=>v+w*(p.mastery[s]||0),0);
  const interest=p.interests.length?role.interests.filter(i=>p.interests.includes(i)).length/role.interests.length:.5;
  const gaps=Object.entries(weights).map(([id,w])=>({skill:cat.skills.find(s=>s.id===id)!,priority:w*(1-(p.mastery[id]||0)),mastery:p.mastery[id]||0})).filter(x=>x.priority>.001).sort((a,b)=>b.priority-a.priority||a.skill.id.localeCompare(b.skill.id));
  return {role,score:round(100*(usable?.7*baseline+.1*trend+.2*interest:(.7*baseline+.2*interest)/.9)),baseline:round(baseline*100),trend:round(trend*100),interest:round(interest*100),coverage:covers[idx],hasTrend:usable,gaps,weights};
 }).sort((a,b)=>b.score-a.score||a.role.id.localeCompare(b.role.id));
}
export function prioritySkills(cat:Catalogue,p:Profile,roleId:string,month:string){
 const a=matches(cat,p,month,'moderate').find(x=>x.role.id===roleId)!;const b=matches(cat,p,month,'fast').find(x=>x.role.id===roleId)!;
 if(!a.hasTrend||!b.hasTrend)return [];
 const ids=new Set(b.gaps.slice(0,3).map(x=>x.skill.id));return a.gaps.slice(0,3).filter(x=>ids.has(x.skill.id));
}
export function pathway(cat:Catalogue,p:Profile,m:Match){
 const chosen:Resource[]=[];const covered=new Set<string>();
 for(const gap of m.gaps.filter(g=>g.mastery<.8).slice(0,5)){
  if(covered.has(gap.skill.id))continue;
  const resource=cat.resources.find(r=>r.skills.includes(gap.skill.id));
  if(resource&&!chosen.some(r=>r.id===resource.id)){chosen.push(resource);resource.skills.forEach(s=>covered.add(s));}
 }
 const ordered:Resource[]=[];const visited=new Set<string>();
 const dependencies:Record<string,string[]>={powerbi:['excel'],sustainability:['excel'],controls:['verification']};
 function visit(r:Resource){if(visited.has(r.id))return;visited.add(r.id);for(const id of dependencies[r.id]||[]){const dep=cat.resources.find(x=>x.id===id);if(dep&&dep.skills.some(s=>(p.mastery[s]||0)<.6))visit(dep)}ordered.push(r)}
 chosen.forEach(visit);
 const weekly=Math.max(1,p.hours);let hours=0;return ordered.map(r=>{const start=Math.floor(hours/weekly)+1;hours+=r.hours;return {...r,startWeek:start,endWeek:Math.ceil(hours/weekly)}});
}
export function keywordSuggestions(cat:Catalogue,text:string){
 const words:Record<string,string[]>={excel:['excel','spreadsheet','vlookup','pivot'],reporting:['report','reporting','monthly'],reconciliation:['reconcile','reconciliation','balance'],data_validation:['check','invoice','accuracy','validate'],stakeholder:['client','customer','communicate','liaise'],sql:['sql','query','database'],powerbi:['power bi','dashboard'],payment_followup:['payment','follow up','collection'],recordkeeping:['record','document'],esg_basics:['esg','sustainab'],payroll_rules:['payroll','salary'],risk_controls:['compliance','risk','control']};
 const aliases:Record<string,string[]>={excel:['电子表格','透视表','hamparan','jadual pangsi'],reporting:['财务报告','编制报告','laporan','pelaporan'],reconciliation:['对账','penyesuaian akaun'],data_validation:['发票','数据校验','核对','invois','pengesahan data','semak data'],stakeholder:['客户沟通','pelanggan','komunikasi'],sql:['数据库查询','pangkalan data'],powerbi:['仪表板','papan pemuka'],payment_followup:['付款','款项跟进','bayaran','susulan'],recordkeeping:['记录管理','rekod','dokumen'],esg_basics:['可持续','kelestarian'],payroll_rules:['薪资','薪酬','penggajian','gaji'],risk_controls:['合规','风险','内部控制','pematuhan','risiko','kawalan'],ai_verification:['核验ai','ai输出','pengesahan ai'],critical_thinking:['批判性思维','pemikiran kritis'],privacy:['隐私','数据保护','privasi'],process_mapping:['流程','proses'],data_storytelling:['数据叙事','penceritaan data'],exception_handling:['异常','pengecualian']};
 const lower=text.toLowerCase();return cat.skills.filter(s=>[...(words[s.id]||[s.name.toLowerCase()]),...(aliases[s.id]||[])].some(w=>lower.includes(w)));
}

/** Current-role growth is task/skill based, never a future-role match probability. */
export function currentRole(cat:Catalogue,p:Profile,month:string,scenario:string):Match{
 const tasks=cat.tasks.filter(t=>p.tasks.includes(t.id));
 const ids=tasks.length?[...new Set(tasks.flatMap(t=>t.skills))]:Object.keys(p.mastery);
 const weights=Object.fromEntries(ids.map(id=>[id,Math.max(1,tasks.filter(t=>t.skills.includes(id)).length)]));
 const total=Object.values(weights).reduce((a,b)=>a+b,0)||1;for(const id in weights)weights[id]/=total;
 const role:Role={id:'current',name:p.title,subtitle:'Strengthen the work you do today.',code:'current',family:'Current-role growth',icon:'growth',sdg:['4.4','8.2'],sdg_reason:'Build relevant work skills and use technology with better checks, judgement and responsible practice.',interests:[],qualification:'Priorities are prototype assumptions, not a certification or an employer requirement.',weights,source:cat.evidence.period_sources?.[month]?.url||cat.evidence.source_url};
 const adjustedWeights=adjusted({...cat,tasks:tasks.length?tasks:cat.tasks},role,month,scenario);
 const gaps=Object.entries(adjustedWeights).map(([id,weight])=>({skill:cat.skills.find(s=>s.id===id)!,priority:weight*(1-(p.mastery[id]||0)),mastery:p.mastery[id]||0})).filter(g=>g.skill&&g.priority>.001).sort((a,b)=>b.priority-a.priority||a.skill.id.localeCompare(b.skill.id));
 return {role,weights:adjustedWeights,gaps,score:0,baseline:0,trend:0,interest:0,coverage:tasks.length?tasks.filter(t=>t.observations[month]?.automation!=null).length/tasks.length:0,hasTrend:tasks.length>0&&tasks.filter(t=>t.observations[month]?.automation!=null).length/tasks.length>=.5};
}
