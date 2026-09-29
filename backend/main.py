from pathlib import Path
from typing import Optional
import math
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE = Path(__file__).resolve().parent
DATA = BASE / 'data' / 'cyber_risk_dataset.csv'
app = FastAPI(title='DIGISAT Cyber Risk API', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

def load():
    return pd.read_csv(DATA)

def money(n):
    return f"₹{n/10_000_000:.2f}Cr"

@app.get('/api/health')
def health():
    return {'status':'ok','service':'DIGISAT Cyber Risk API'}

@app.get('/api/assets')
def assets(status: Optional[str]=Query(None), q: Optional[str]=Query(None)):
    df=load()
    if status and status.lower()!='all': df=df[df['status'].str.lower()==status.lower()]
    if q: df=df[df.astype(str).apply(lambda row: row.str.contains(q, case=False, na=False).any(), axis=1)]
    return df.to_dict(orient='records')

@app.get('/api/summary')
def summary():
    df=load(); exposure=float(df.eal.sum()); avg=int(round(df.risk.mean()))
    return {'risk_score':avg,'financial_exposure':exposure,'financial_exposure_display':money(exposure),'critical_risks':int((df.status=='Critical').sum()),'asset_count':len(df),'posture':68}

class Scenario(BaseModel):
    mfa: bool=False
    patch: bool=False
    edr: bool=False
    segment: bool=False

@app.post('/api/simulate')
def simulate(s: Scenario):
    base=67; reductions={'mfa':8,'patch':12,'edr':6,'segment':5}
    risk=max(18,base-sum(reductions[k] for k,v in s.model_dump().items() if v))
    exposure=2.34*(risk/base)
    return {'base_risk':base,'projected_risk':risk,'risk_reduction_pct':round((1-risk/base)*100,1),'exposure_crore':round(exposure,2)}

@app.get('/api/optimize')
def optimize(budget: float=10_000_000):
    options=[
      ('Critical Vulnerability Remediation',4500000,18,'Highest concentration of critical findings'),
      ('MFA Expansion',2800000,12,'Reduces identity compromise exposure'),
      ('EDR Coverage',3600000,9,'Improves endpoint detection and response'),
      ('Network Segmentation',5200000,8,'Limits lateral movement'),
      ('Cloud Security Controls',4100000,7,'Hardens internet-facing cloud assets')]
    remaining=budget; chosen=[]
    for name,cost,impact,reason in sorted(options,key=lambda x:x[2]/x[1],reverse=True):
        allocation=min(cost,max(0,remaining)); remaining-=allocation
        if allocation>0: chosen.append({'name':name,'cost':cost,'allocation':allocation,'impact':round(impact*allocation/cost,1),'reason':reason})
    return {'budget':budget,'remaining':remaining,'allocations':chosen,'modeled_reduction':round(sum(x['impact'] for x in chosen),1)}

@app.post('/api/ai')
def ai(question: str):
    q=question.lower();
    if 'mfa' in q: answer='Enabling MFA on the Employee VPN and Admin Console is modeled to reduce risk by 8 points and lower identity-compromise exposure.'
    elif 'budget' in q: answer='For a ₹1Cr budget, the baseline optimizer prioritizes vulnerability remediation, MFA expansion and EDR coverage because they address the largest modeled risk contributors.'
    elif 'fix' in q or 'first' in q: answer='Patch Customer API and Cloud Storage first, then enable MFA on Employee VPN and Admin Console.'
    else: answer='Risk is driven mainly by internet exposure, critical vulnerabilities, patch age and missing MFA. Customer API and Cloud Storage are the largest individual contributors.'
    return {'answer':answer}
