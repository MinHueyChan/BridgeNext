"""Account-owned pathway snapshots, independent of current profile and achievements."""
import copy
from .achievements import resources_for,make_record

def snapshot(cat,body,at):
    profile=body['profile'];goal=body.get('learningGoal','future')
    if not profile['confirmed']:raise ValueError('Confirm the planning profile first')
    resources=resources_for(cat,profile,body['selected'],body['month'],body['scenario'],goal)
    if not resources:raise ValueError('No learning resources to save')
    base=make_record(cat,profile,body['selected'],body['month'],body['scenario'],goal,resources,'',at)
    role=next(r for r in cat['roles'] if r['id']==body['selected'])
    plan={k:copy.deepcopy(body[k]) for k in ['profile','selected','month','scenario','completed']};plan['learningGoal']=goal
    plan['completed']=[r['id'] for r in resources if r['id'] in plan['completed']]
    return {'id':base['id'],'pathKey':base['pathKey'],'target':base['target'],'goal':goal,'savedAt':at,'updatedAt':at,'plan':plan,'resources':copy.deepcopy(resources),'estimatedHours':base['estimatedHours'],'skillIds':base['skillIds'],'sdg':base['sdg'],'source':base['source'],'evidenceRelease':base['evidenceRelease'],'description':'Strengthen the work you do today.' if goal=='current' else role['subtitle'],'sdgReason':'Build relevant work skills and use technology with better checks, judgement and responsible practice.' if goal=='current' else role['sdg_reason']}
