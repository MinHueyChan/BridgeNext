"""Discover public releases; activate only compatible, validated task observations."""
import copy,csv,io,json,math,re,time,urllib.request
from datetime import date,datetime,timezone
REPO='https://huggingface.co/datasets/Anthropic/EconomicIndex'
API='https://huggingface.co/api/datasets/Anthropic/EconomicIndex'
METRICS={'collaboration_bucket_automation_pct':'automation','collaboration_bucket_augmentation_pct':'augmentation','pct':'usage'}
REQUIRED={'date_start','date_end','geo_id','geo_level','category_name','hierarchy_level','metric_id','value','node_external_id','node_name'}

def now():return datetime.now(timezone.utc).isoformat()
def discover():
    with urllib.request.urlopen(API,timeout=25) as response:
        payload=response.read(8_000_001)
    if len(payload)>8_000_000:raise ValueError('Discovery response too large')
    info=json.loads(payload);revision=info.get('sha','')
    if not re.fullmatch(r'[a-f0-9]{40}',revision):raise ValueError('Missing immutable revision')
    releases={}
    for item in info.get('siblings',[]):
        path=item.get('rfilename','');match=re.match(r'^release_(\d{4})_(\d{2})_(\d{2})/',path)
        if match:
            release=date(*map(int,match.groups())).isoformat()
            if release<=date.today().isoformat():releases.setdefault(release,[]).append(path)
    return revision,releases

def parse_stream(stream,cat,release,url,revision):
    reader=csv.DictReader(stream)
    if not REQUIRED<=set(reader.fieldnames or []):raise ValueError('Unreviewed CSV schema')
    nodes={t['node_id'] for t in cat['tasks']};observations={};seen=set();started=time.monotonic()
    for n,row in enumerate(reader):
        if n>2_000_000 or time.monotonic()-started>180:raise ValueError('Source exceeded processing limit')
        if row['geo_id']!='GLOBAL' or row['geo_level']!='global' or row['category_name']!='onet' or row['hierarchy_level']!='0' or row['node_external_id'] not in nodes or row['metric_id'] not in METRICS:continue
        start=date.fromisoformat(row['date_start']);end=date.fromisoformat(row['date_end'])
        following=date(start.year+(start.month==12),start.month%12+1,1)
        if start.day!=1 or end!=following or end>date.fromisoformat(release):raise ValueError('Invalid observation period')
        value=float(row['value'])
        if not math.isfinite(value) or not 0<=value<=100:raise ValueError('Invalid percentage')
        key=(row['node_external_id'],start.strftime('%Y-%m'),METRICS[row['metric_id']])
        if key in seen:raise ValueError('Duplicate task metric')
        seen.add(key);observations.setdefault(key[0],{}).setdefault(key[1],{})[key[2]]=value
    periods=sorted({month for obs in observations.values() for month in obs})
    if not periods:raise ValueError('No compatible task observations')
    for month in periods:
        valid=0
        for node in nodes:
            values=observations.get(node,{}).get(month,{})
            if 'automation' in values:
                if 'augmentation' not in values or abs(values['automation']+values['augmentation']-100)>.2:raise ValueError('Incomplete collaboration metrics')
                valid+=1
        if valid/max(1,len(nodes))<.5:raise ValueError('Insufficient task coverage')
        for role in cat['roles']:
            links=[t for t in cat['tasks'] if any(s in role['weights'] for s in t['skills'])]
            old=sum(t['observations'].get(month,{}).get('automation') is not None for t in links)
            current=sum('automation' in observations.get(t['node_id'],{}).get(month,{}) for t in links)
            if not links or current/len(links)<.5 or current<old:raise ValueError('Role evidence coverage regressed')
    updated=copy.deepcopy(cat);changes=[]
    for task in updated['tasks']:
        for month in periods:
            values={field:observations.get(task['node_id'],{}).get(month,{}).get(field) for field in METRICS.values()}
            before=task['observations'].get(month,{})
            for field,value in values.items():
                if before.get(field)!=value:changes.append({'task':task['id'],'month':month,'metric':field,'before':before.get(field),'after':value})
            task['observations'][month]=values
    evidence=updated['evidence'];evidence['months']=sorted(set(evidence['months'])|set(periods));evidence.update(source_url=url,release=release,retrieved_at=now(),revision=revision)
    evidence['period_sources']={**cat['evidence'].get('period_sources',{m:{'url':cat['evidence']['source_url'],'release':cat['evidence']['release']} for m in cat['evidence']['months']}),**{m:{'url':url,'release':release} for m in periods}}
    return updated,changes

def download(cat,release,revision):
    folder='release_'+release.replace('-','_');url=f'{REPO}/resolve/{revision}/{folder}/data/aei_claude_ai_{release}.csv'
    with urllib.request.urlopen(url,timeout=45) as response:
        # Streaming avoids retaining the complete global dataset in memory.
        return parse_stream(io.TextIOWrapper(response,encoding='utf-8-sig'),cat,release,url,revision)

def refresh_catalogue(cat):
    revision,releases=discover();rejected=[]
    candidates=sorted((r for r in releases if r>=cat['evidence']['release']),reverse=True)[:3]
    for release in candidates:
        expected=f"release_{release.replace('-','_')}/data/aei_claude_ai_{release}.csv"
        if expected not in releases[release]:rejected.append({'release':release,'reason':'Unsupported file layout; review required'});continue
        try:updated,changes=download(cat,release,revision)
        except (ValueError,KeyError,csv.Error) as error:rejected.append({'release':release,'reason':str(error)});continue
        report={'checked_at':now(),'status':'updated' if changes or release!=cat['evidence']['release'] else 'unchanged','previous_release':cat['evidence']['release'],'active_release':release,'discovered_releases':sorted(releases,reverse=True),'revision':revision,'changes':changes,'review_required':rejected,'source_url':updated['evidence']['source_url']}
        return updated,report
    return cat,{'checked_at':now(),'status':'review_required','active_release':cat['evidence']['release'],'discovered_releases':sorted(releases,reverse=True),'changes':[],'review_required':rejected,'source_url':cat['evidence']['source_url']}
