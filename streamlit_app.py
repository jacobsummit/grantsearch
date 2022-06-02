import streamlit as st
import pandas as pd
from fundNSF import FundNSF
from datetime import date
from datetime import datetime
pd.set_option('display.float_format', lambda x: f'{x:.0f}')
st.set_page_config(layout='wide', page_icon="random", page_title="Ultra Grant Search 2000")


st.image('https://img1.wsimg.com/isteam/ip/ec7b4a1b-11a1-4c5e-8cc9-dfc23171b278/SVS_Logo_Horizontal_White.png/:/rs=w:358,h:75,cg:true,m/cr=w:358,h:75/qt=q:95')

st.title('Ultra Grant Search 2000')
df = pd.DataFrame
with st.sidebar:
    st.write("Use commas to separate values")
    grantSource = st.selectbox("Choose a Grant Database:",["NSF", "NIH - NOT FUNCTIONAL"])
    keywords = st.text_input("Keyword(s)")
    pi = st.text_input("Principal Investigator(s)")
    org = st.text_input("Organization(s)")
    state = st.text_input("State Code(s)")
    sdate = st.date_input("Enter Start Date in Date Range", value= date(2015, 1, 1))
    edate = st.date_input("Enter End Date in Date Range")

def nih_query(keywords, pi, org, state, sdate, edate):
    print()


def nsf_query(keywords, pi, org, state, sdate, edate):
    nsf = FundNSF()
    nsf.reset()
    nsf.set_fields(abstractText = True, perfStateCode = True, piPhone = True,
                   piEmail=True, fundProgramName = True, pdPIName = True, poName=True, 
                   expDate=True, awardeeAddress=True, awardeeZipCode = True, poPhone = True, 
                   fundAgencyCode = True, awardAgencyCode = True, agency=False)
    
    sdate = sdate.strftime("%m/%d/%Y")
    edate = edate.strftime("%m/%d/%Y")
    
    varDict={}
    varDict['awardeeName']=org
    if varDict['awardeeName'] != '':
        varDict['awardeeName']=org
    varDict['awardeeStateCode']=state
    if varDict['awardeeStateCode'] != '':
        varDict['awardeeStateCode']=state
    varDict['pdPIName']=pi
    if varDict['pdPIName'] != '':
        varDict['pdPIName']=pi   
    varDict['dateStart']=sdate
    if varDict['dateStart'] != '':
        varDict['dateStart']=sdate
    varDict['dateEnd']=edate
    if varDict['dateEnd'] != '':
        varDict['dateEnd']=edate
    params = {k: v for k, v in varDict.items() if v}
    # params = [f'{x}={y}' for x, y in varDict.items() if y!='']
    # params = ",".join(map(str, params))
    
    # awardeeName=org, pdPIName=pi
    nsf.set_params(**params)
    commKeywords = keywords.replace(",","|").replace(" ","")
    # commKeywords = ",".join(map(str, commKeywords))
    data = nsf.keyword_search(commKeywords)
    df = pd.DataFrame(data, columns = ['id','title','fundProgramName','date','piFirstName',
                                    'piLastName','perfStateCode','awardeeName','poName','expDate',
                                    'fundsObligatedAmt','pdPIName','piEmail','piPhone','awardeeAddress',
                                    'awardeeCity','awardeeStateCode','awardeeZipCode','abstractText'])
    df.insert(18, 'count', df['abstractText'].str.lower().str.count(commKeywords))
    df = df.sort_values('fundsObligatedAmt').sort_values('count',ascending=False)
    # df['date'] = pd.to_datetime(df['date']).dt.date
    return df, commKeywords


# Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# df = load_data(None)
# df = df[df['abstract'].str.contains(keywords, case=False, na=False)]
# df.insert(24, 'count', df['abstract'].str.lower().str.count(keywords))
# df = df[df['principalinvestigator'].str.contains(pinames, case=False, na=False)]
# df = df[df['organization'].str.contains(orgname, case=False, na=False)]
# df = df[df['state'].str.contains(statecode, case=False, na=False)]
# df = df[df['startdate']>=startdate]
# df = df[df['startdate']<=enddate]
if grantSource == "NSF":
    df, commkeys = nsf_query(keywords, pi, org, state, sdate, edate)
elif grantSource == "NIH":
    nih_query()
    

# df = df.sort_values('awardedamounttodate').sort_values('count',ascending=False)
# Notify the reader that the data was successfully loaded.
# data_load_state.text("Done! (using st.cache)")
st.dataframe(df.head(50).style.format(thousands=""))
st.write(commkeys)
st.download_button(label="Download CSV Output", data=df.to_csv(), file_name="output.csv")
