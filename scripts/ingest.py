#!/usr/bin/env python3
"""Fetch verified public Greenhouse/Lever boards; deduplicate and report source failures."""
import json,re,hashlib,datetime,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/jobs.json'
UA='HealthcareJobRadar/1.0 (+public career feed aggregator)'
# Verified public board(s). Add a company only after confirming its live ATS board token.
GREENHOUSE=[('Maven Clinic','mavenclinic'),('Cohere Health','CohereHealth'),('Truveta','truveta'),('Ophelia','ophelia'),('eClinical Solutions','eclinicalsolutions'),('GHX','globalhealthcareexchangeinc')]
LEVER=[]
KEYWORDS=re.compile(r'health|medical|clinical|medicine|patient|pharma|research|biotech|doctor|physician|mbbs|nurs|hospital|diagnostic|pharmacovigilance|health.?tech|regulatory|care|AI|product',re.I)
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':UA})
 with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read().decode())
def striphtml(s):return re.sub(r'<[^>]+>',' ',s or '').replace('&nbsp;',' ').replace('&amp;','&').strip()
def parse_dt(v):
 try:return datetime.datetime.fromisoformat(str(v).replace('Z','+00:00')).isoformat() if v else None
 except:return None
def norm(source,company,j):
 title=j.get('title') or j.get('text') or 'Untitled';desc=striphtml(j.get('content') or j.get('descriptionPlain') or j.get('description') or '')
 if not KEYWORDS.search(title+' '+desc[:6000]):return None
 loc=j.get('location') or {}
 if isinstance(loc,dict):loc=loc.get('name','')
 if not loc:loc=', '.join(x.get('name','') for x in j.get('locations',[]) if isinstance(x,dict))
 url=j.get('absolute_url') or j.get('hostedUrl') or j.get('url') or '';ext=str(j.get('id') or j.get('requisitionId') or url)
 fp=hashlib.sha256('|'.join([source,ext,url,title.lower(),company.lower()]).encode()).hexdigest()
 return {'fingerprint':fp,'source':source,'source_job_id':ext,'url':url,'title':title[:250],'company':company,'location':str(loc)[:350],'description':desc[:7000],'posted_at':parse_dt(j.get('updated_at') or j.get('created_at') or j.get('publication_date'))}
def main():
 old=json.loads(OUT.read_text()) if OUT.exists() else {'jobs':[]};by={j['fingerprint']:j for j in old.get('jobs',[])};errors=[];count=0;success_sources=0
 for company,slug in GREENHOUSE:
  try:
   payload=get(f'https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true');success_sources+=1
   for j in payload.get('jobs',[]):
    n=norm('Greenhouse',company,j)
    if n:by.setdefault(n['fingerprint'],n);count+=1
  except Exception as e:errors.append(f'Greenhouse/{company}: {e}')
 for company,slug in LEVER:
  try:
   postings=get(f'https://api.lever.co/v0/postings/{slug}?mode=json');success_sources+=1
   for j in postings:
    j['location']=(j.get('categories') or {}).get('location','');n=norm('Lever',company,j)
    if n:by.setdefault(n['fingerprint'],n);count+=1
  except Exception as e:errors.append(f'Lever/{company}: {e}')
 jobs=list(by.values());jobs.sort(key=lambda x:x.get('posted_at') or '',reverse=True)
 OUT.write_text(json.dumps({'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'jobs':jobs,'ingestion':{'fetched_relevant':count,'sources_succeeded':success_sources,'sources_configured':len(GREENHOUSE)+len(LEVER),'errors':errors}},indent=2,ensure_ascii=False))
 print(f'Fetched {count} relevant; dataset now {len(jobs)}; sources={success_sources}/{len(GREENHOUSE)+len(LEVER)}; errors={errors}')
 if success_sources==0:raise RuntimeError('All configured job sources failed; refusing a green workflow.')
if __name__=='__main__':main()
