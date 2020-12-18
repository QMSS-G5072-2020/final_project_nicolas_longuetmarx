from legis_easy_download import __version__
from legis_easy_download import legis_easy_download

def test_version():
    assert __version__ == '0.1.0'

import pytest

# I want to make sure my function returns the same output as what I would get from the direct command:
def test_package():
    mylink2="https://api.legiscan.com/?key="+api_key+"&op=getMasterList&id=1644"
    r = requests.get(mylink2)
    json_response=r.json()
    mydata=pd.DataFrame.from_dict(json_response['masterlist'])
    mynewdata=mydata.loc[  'title' ,:]
    mytitlelist=mynewdata.to_frame()
    mytitlelist=mytitlelist.dropna(subset=['title'])
    mydico = {
    "environment" : ".environment|energy|tree|river|forest|animal|insect|fertilizer|dam|agricult|water|land|water|owner|control|site|air|solid|gas|tenant|oil|park|airport|coal|plant|prevent|underground|power|soil|portion|landlord|condition.",
    "courts" : ".court|judgment|attorney|case|appeal|civil|petition|sheriff|trial|circuit court|district court|such_person|complaint|counsel|brought|circuit|warrant|paid",
    "pensions": ".paid|benefit|rate|payment|equal|death|age|credit|pay|total|life|pension|premium|calendar year|loss|account|case|per cent|event|membership|excess|maximum.",
    "local_projects": ".development|local|project|budget|government|cost|grant|research|center|local government|data|transfer|governor|is the intent|develop|urban|review|biennium.",
    "procurement":".director|contract|work|review|civil|labor|contractor|attorney general|bureau|final|perform|audit|receipt|status|exempt|panel|government|firm|bid|prepared.",
    "elections":".district|town|petition|charter|special|ballot|mayor|voter|township|precinct|cast|referendum|census|elector|case|town council|said district|such district.",
    "banking":".loan|trust|bank|agent|partnership|institution|foreign|stock|mortgage|deposit|surplus|interest|merger|credit union|partner|case|credit|gift|branch|transact.",
    "licensing":".license|fee|dealer|sale|food|sold|holder|sell|valid|fish|agent|distributor|milk|liquor|product|such license|livestock|game|card|retail|misdemeanor|fine.",
    "real_estate":".real|interest|sale|owner|contract|claim|lien|payment|transfer|instrument|seller|holder|issuer|debtor|claimant|buyer|pay|broker|settlement|receipt|money.",
    "bonds":".interest|bond|payment|commonwealth|cost|sale|paid|pay|project|power|thereon|sold|debt|pledge|local law|event|hereof|proper|said board|real|port|sell|therefrom.",
    "expenditures":".fund|account|money|paid|special|pay|tile|payment|transfer|for the fiscal year|excess|trust fund|so much thereof|deposit|state general fund|auditor|tie.",
    "bureaucracy":".governor|council|government|chief|fire|appoint|personnel|compact|conflict|perform|shall consist|invalid|parish|successor|volunteer|membership|head|travel.",
    "healthcare":".health|care|treatment|health care|physician|home|human|patient|mental|mental health|drug|social|condition|public health|medicaid|dental|client|review|institution.",
    "child_custody":".child|court|minor|children|parent|age|probation|crime|victim|parole|guardian|adult|petition|placement|youth|case|social|legal|child support|obligor|home.",
    "taxes":".tax|paid|gross|credit|return|net|rate|exempt|assessor|case|refund|equal|sale|total|calendar year|payment|fuel|portion|sold|price|retail|zone|pay|such tax.",
    "education":".school|school district|state board|district|student|institution|higher|teacher|special|aid|pupil|children|school year|tuition|high school|school board.",
    "traffic1":".motor|highway|driver|owner|traffic|plate|test|vessel|accident|weight|special|sect|trailer|railroad|state highway|stricken|feet|fine|alcohol|aircraft|carrier.",
    "traffic2":".street|road|feet|island|river|run|tract|team|great|highway|township|cent."
    }
    type_to_id = {key : value for key,value in enumerate(mydico.keys())}
    i=0
    for key, value in mydico.items():
        mytitlelist.loc[mytitlelist.title.str.contains(value), 'type']=key
        i=i+1
        mytitlelist.loc[mytitlelist.title.str.contains(value), 'typenum']=i
    expected=mytitlelist[mytitlelist.typenum==18.0].count()
    expected=expected['title']
    overall_request('NY', year=2019)
    predicted=mytitlelist[mytitlelist.typenum==18.0].count()
    predicted=predicted['title']
    assert predicted == expected 