"""Deterministic counterpart of src/engine.ts. No employment predictions."""
def adjusted(cat, role, month, scenario):
    out={}
    for sid,w in role['weights'].items():
        links=[t for t in cat['tasks'] if sid in t['skills']]
        d=1 if sid in ['ai_verification','critical_thinking','risk_controls','exception_handling','data_validation'] else -1 if sid in ['excel','recordkeeping','reconciliation','payment_followup','reporting'] else 0
        factors=[]
        for t in links:
            a=t['observations'].get(month,{}).get('automation')
            factor=(1+.1*d*(a/100))*(1+.2*d if scenario=='fast' else 1) if a is not None else 1
            factors.append(factor)
        out[sid]=w*(sum(factors)/len(factors) if factors else 1)
    total=sum(out.values());return {s:w/total for s,w in out.items()}
def calculate(cat,profile,month,scenario):
    coverage=[]
    for role in cat['roles']:
        links=[t for t in cat['tasks'] if any(s in role['weights'] for s in t['skills'])]
        coverage.append(sum(t['observations'].get(month,{}).get('automation') is not None for t in links)/len(links) if links else 0)
    usable=all(c>=.5 for c in coverage);results=[]
    for idx,role in enumerate(cat['roles']):
        base=sum(w*profile['mastery'].get(s,0) for s,w in role['weights'].items())/sum(role['weights'].values())
        weights=adjusted(cat,role,month,scenario);trend=sum(w*profile['mastery'].get(s,0) for s,w in weights.items())
        interest=sum(i in profile['interests'] for i in role['interests'])/len(role['interests']) if profile['interests'] else .5
        score=100*(.7*base+.1*trend+.2*interest) if usable else 100*(.7*base+.2*interest)/.9
        gaps=[{'skill':next(x for x in cat['skills'] if x['id']==s),'priority':w*(1-profile['mastery'].get(s,0)),'mastery':profile['mastery'].get(s,0)} for s,w in weights.items()]
        gaps=sorted([g for g in gaps if g['priority']>.001],key=lambda g:(-g['priority'],g['skill']['id']))
        results.append({'role':role,'score':round(score,1),'baseline':round(base*100,1),'trend':round(trend*100,1),'interest':round(interest*100,1),'coverage':coverage[idx],'hasTrend':usable,'gaps':gaps,'weights':weights})
    return sorted(results,key=lambda r:(-r['score'],r['role']['id']))

def current_role(cat,profile,month,scenario):
    tasks=[t for t in cat['tasks'] if t['id'] in profile['tasks']]
    ids=list(dict.fromkeys(s for t in tasks for s in t['skills'])) if tasks else list(profile['mastery'])
    weights={s:max(1,sum(s in t['skills'] for t in tasks)) for s in ids}
    total=sum(weights.values()) or 1;weights={s:w/total for s,w in weights.items()}
    role={'weights':weights}
    values=adjusted({**cat,'tasks':tasks or cat['tasks']},role,month,scenario) if weights else {}
    gaps=sorted([{'id':s,'priority':w*(1-profile['mastery'].get(s,0))} for s,w in values.items() if w*(1-profile['mastery'].get(s,0))>.001],key=lambda g:(-g['priority'],g['id']))
    return {'weights':values,'gaps':gaps}
