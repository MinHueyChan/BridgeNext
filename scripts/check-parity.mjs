import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {matches,currentRole,pathway} from '../src/engine.ts';
const cat=JSON.parse(readFileSync(new URL('../data/catalogue.json',import.meta.url),'utf8'));
const cases=[];
for(const name of ['mei','aaron'])for(const month of ['2026-04','2026-05'])for(const scenario of ['moderate','fast'])cases.push({cat,profile:cat.personas[name],month,scenario});
const missing=structuredClone(cat);for(const t of missing.tasks)for(const o of Object.values(t.observations))o.automation=null;
cases.push({cat:missing,profile:cat.personas.mei,month:'2026-05',scenario:'fast'});
const code="import json,sys;from backend.engine import calculate;print(json.dumps([calculate(x['cat'],x['profile'],x['month'],x['scenario']) for x in json.load(sys.stdin)]))";
const result=spawnSync(process.env.BRIDGENEXT_PYTHON||'python',['-c',code],{input:JSON.stringify(cases),encoding:'utf8'});
if(result.status!==0)throw Error(result.stderr);
const expected=JSON.parse(result.stdout);
for(let i=0;i<cases.length;i++){const c=cases[i],actual=matches(c.cat,c.profile,c.month,c.scenario);for(let j=0;j<actual.length;j++){const a=actual[j],b=expected[i][j];if(a.role.id!==b.role.id||Math.abs(a.score-b.score)>.0001||a.hasTrend!==b.hasTrend)throw Error(`Score mismatch at case ${i}`);for(const k in a.weights)if(Math.abs(a.weights[k]-b.weights[k])>1e-10)throw Error(`Weight mismatch at ${i}/${k}`)}}
console.log(`Browser/Python parity passed: ${cases.length} cases.`);

const growthCases=[...cases,{...cases[0],profile:{...cat.personas.mei,title:'Custom role',avatarId:0,tasks:[],mastery:{excel:.4}}},{...cases[0],profile:{...cat.personas.mei,tasks:['invoices']}}];
const growth=growthCases.map(c=>currentRole(c.cat,c.profile,c.month,c.scenario));
const codeGrowth="import json,sys;from backend.engine import current_role;print(json.dumps([current_role(x['cat'],x['profile'],x['month'],x['scenario']) for x in json.load(sys.stdin)]))";
const resultGrowth=spawnSync(process.env.BRIDGENEXT_PYTHON||'python',['-c',codeGrowth],{input:JSON.stringify(growthCases),encoding:'utf8'});
if(resultGrowth.status!==0)throw Error(resultGrowth.stderr);
const expectedGrowth=JSON.parse(resultGrowth.stdout);
for(let i=0;i<growth.length;i++){for(const [id,value] of Object.entries(growth[i].weights))if(Math.abs(value-expectedGrowth[i].weights[id])>1e-10)throw Error(`Current-role weight mismatch ${i}/${id}`);if(growth[i].gaps.map(g=>g.skill.id).join(',')!==expectedGrowth[i].gaps.map(g=>g.id).join(','))throw Error(`Current-role priority mismatch ${i}`)}
console.log(`Current-role parity passed: ${growth.length} cases.`);

if('esg_basics' in growth.at(-1).weights)throw Error('Unrelated assessed skills must not become current-task priorities');

const plans=[...cases.map(c=>({...c,goal:'future',selected:matches(c.cat,c.profile,c.month,c.scenario)[0].role.id})),...growthCases.map(c=>({...c,goal:'current',selected:'financial'}))];
const resourceCode="import json,sys;from backend.achievements import resources_for;print(json.dumps([[r['id'] for r in resources_for(c['cat'],c['profile'],c['selected'],c['month'],c['scenario'],c['goal'])] for c in json.load(sys.stdin)]))";
const resourceResult=spawnSync(process.env.BRIDGENEXT_PYTHON||'python',['-c',resourceCode],{input:JSON.stringify(plans),encoding:'utf8'});if(resourceResult.status!==0)throw Error(resourceResult.stderr);
const resourceExpected=JSON.parse(resourceResult.stdout);
for(let i=0;i<plans.length;i++){const c=plans[i];const match=c.goal==='current'?currentRole(c.cat,c.profile,c.month,c.scenario):matches(c.cat,c.profile,c.month,c.scenario).find(m=>m.role.id===c.selected);const actual=pathway(c.cat,c.profile,match).map(r=>r.id);if(JSON.stringify(actual)!==JSON.stringify(resourceExpected[i]))throw Error(`Pathway completion parity mismatch ${i}`)}
console.log(`Pathway completion parity passed: ${plans.length} cases.`);
