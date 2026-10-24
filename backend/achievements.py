"""Self-reported pathway milestones, not certificates or skill verification."""
import hashlib,json,re
from .engine import calculate,current_role

def resources_for(cat,profile,selected,month,scenario,goal):
    if goal=='current':
        result=current_role(cat,profile,month,scenario)
        gaps=[{'id':g['id'],'mastery':profile['mastery'].get(g['id'],0)} for g in result['gaps']]
    else:
        result=next(m for m in calculate(cat,profile,month,scenario) if m['role']['id']==selected)
        gaps=[{'id':g['skill']['id'],'mastery':g['mastery']} for g in result['gaps']]
    chosen=[];covered=set()
    for gap in [g for g in gaps if g['mastery']<.8][:5]:
        if gap['id'] in covered:continue
        resource=next((r for r in cat['resources'] if gap['id'] in r['skills']),None)
        if resource and resource['id'] not in {r['id'] for r in chosen}:chosen.append(resource);covered.update(resource['skills'])
    ordered=[];visited=set();dependencies={'powerbi':['excel'],'sustainability':['excel'],'controls':['verification']}
    def visit(resource):
        if resource['id'] in visited:return
        visited.add(resource['id'])
        for rid in dependencies.get(resource['id'],[]):
            dep=next((r for r in cat['resources'] if r['id']==rid),None)
            if dep and any(profile['mastery'].get(s,0)<.6 for s in dep['skills']):visit(dep)
        ordered.append(resource)
    for resource in chosen:visit(resource)
    return ordered

def make_record(cat,profile,selected,month,scenario,goal,resources,reflection,completed_at):
    role=next(r for r in cat['roles'] if r['id']==selected)
    target=profile['title'] if goal=='current' else role['name']
    target_key=re.sub(r'\s+',' ',profile['title'].strip()).lower() if goal=='current' else selected
    path_key=json.dumps([goal,target_key,sorted(r['id'] for r in resources)],ensure_ascii=False,separators=(',',':'))
    return {'id':hashlib.sha256(path_key.encode()).hexdigest(),'pathKey':path_key,'goal':goal,'target':target,'completedAt':completed_at,'reflection':reflection.strip(),'estimatedHours':sum(r['hours'] for r in resources),'resourceIds':[r['id'] for r in resources],'skillIds':sorted({s for r in resources for s in r['skills']}),'resources':[{k:r[k] for k in ['id','name','url','provider','hours']} for r in resources],'sdg':['4.4','8.2'] if goal=='current' else role['sdg'],'source':cat['evidence'].get('period_sources',{}).get(month,{}).get('url',cat['evidence']['source_url']) if goal=='current' else role['source'],'evidenceRelease':cat['evidence'].get('period_sources',{}).get(month,{}).get('release',cat['evidence']['release']),'selfReported':True}
