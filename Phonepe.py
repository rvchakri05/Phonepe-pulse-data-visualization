import os
import json
import pandas as pd
from sqlalchemy import create_engine
#Create Dataset for push to SQL
Aggregated_insurance={"State":[],"Year":[],"Quater":[],"Tranaction_type":[],"Trans_count":[],"Trans_amount":[]}
Aggregated_transaction={"State":[],"Year":[],"Quater":[],"Tranaction_type":[],"Trans_count":[],"Trans_amount":[]}
Aggregated_user={"State":[],"Year":[],"Quater":[],"Brand":[],"User":[]}
Aggregated_user_All={"State":[],"Year":[],"Quater":[],"Registered_User":[],"Apps_open":[]}
map_transacion={"State":[],"Year":[],"Quater":[],"District":[],"Trans_count":[],"Trans_amount":[]}
map_insurance={"State":[],"Year":[],"Quater":[],"District":[],"Trans_count":[],"Trans_amount":[]}
map_user    ={"State":[],"Year":[],"Quater":[],"District":[],"Registered_User":[],"Apps_Opens":[]}
top_insurance={"State":[],"Year":[],"Quater":[],"Pincodes":[],"Trans_count":[],"Trans_Amount":[]}
top_transaction={"State":[],"Year":[],"Quater":[],"Pincodes":[],"Trans_count":[],"Trans_Amount":[]}
top_user={"State":[],"Year":[],"Quater":[],"Pincodes":[],"Registered_User":[]}
path_agrinsu= "data/aggregated/insurance/country/india/state/"
#Insurance data bring from Json file
Agg_insu_list=os.listdir(path_agrinsu)
for i in Agg_insu_list:
    path1=path_agrinsu+i+'/'
    dir_path1=os.listdir(path1)
    for j in dir_path1:
        path2=path1+j+"/"
        dir_path2=os.listdir(path2)
        for k in dir_path2:
            path_data=path2+k
            dat=open(path_data,"r")
            data=json.load(dat)
            for l in data['data']['transactionData']:
                Aggregated_insurance["State"].append(i)
                Aggregated_insurance["Year"].append(j)
                Aggregated_insurance["Quater"].append(int(k.strip(".json")))
                Aggregated_insurance["Tranaction_type"].append(l["name"])
                Aggregated_insurance["Trans_count"].append(l["paymentInstruments"][0]["count"])
                Aggregated_insurance["Trans_amount"].append(l["paymentInstruments"][0]["amount"])
# Get tranaction data from Josn file
trans_path="data/aggregated/transaction/country/india/state/"
Agg_trans_list=os.listdir(trans_path)
for i in Agg_trans_list:
    path1=trans_path+i+'/'
    dir_path1=os.listdir(path1)
    for j in dir_path1:
        path2=path1+j+"/"
        dir_path2=os.listdir(path2)
        for k in dir_path2:
            path_data=path2+k
            dat=open(path_data,"r")
            data=json.load(dat)
            for l in data['data']['transactionData']:
                Aggregated_transaction["State"].append(i)
                Aggregated_transaction["Year"].append(j)
                Aggregated_transaction["Quater"].append(int(k.strip(".json")))
                Aggregated_transaction["Tranaction_type"].append(l["name"])
                Aggregated_transaction["Trans_count"].append(l["paymentInstruments"][0]["count"])
                Aggregated_transaction["Trans_amount"].append(l["paymentInstruments"][0]["amount"])
#Get user data from Json file
User_path="data/aggregated/user/country/india/state/"
Agg_User_list=os.listdir(User_path)
for c in Agg_User_list:
    path1=User_path+c+'/'
    dir_path1=os.listdir(path1)
    for d in dir_path1:
        path2=path1+d+"/"
        dir_path2=os.listdir(path2)
        for e in dir_path2:
            path_data=path2+e
            dat=open(path_data,"r")
            data=json.load(dat)
            Aggregated_user_All["State"].append(c)
            Aggregated_user_All["Year"].append(d)
            Aggregated_user_All["Quater"].append(int(e.strip(".json")))
            Aggregated_user_All["Registered_User"].append(data["data"]["aggregated"]["registeredUsers"])
            Aggregated_user_All["Apps_open"].append(data["data"]["aggregated"]["appOpens"])
            try:
                for f in data["data"]["usersByDevice"]:
                    Aggregated_user["State"].append(c)
                    Aggregated_user["Year"].append(d)
                    Aggregated_user["Quater"].append(int(e.strip(".json")))
                    Aggregated_user["Brand"].append(f["brand"])
                    Aggregated_user["User"].append(f["count"])
            except:
                pass
#Get District wise tranaction data
map_transpath="data/map/transaction/hover/country/india/state/"
agr=os.listdir(map_transpath)
for i in agr:
  path1=map_transpath+i+"/"
  agr2=os.listdir(path1)
  for l in agr2:
    path2=path1+l+"/"
    agr3=os.listdir(path2)
    for j in agr3:
      dat=open(path2+j,"r")
      data=json.load(dat)
      kt=data["data"]["hoverDataList"]
      for k in kt:
        dis=k["name"]
        t_count=k["metric"][0]["count"]
        t_amount=k["metric"][0]["amount"]
        map_transacion["State"].append(i)
        map_transacion["Year"].append(l)
        map_transacion["Quater"].append(int(j.strip(".json")))
        map_transacion["District"].append(dis)
        map_transacion["Trans_count"].append(t_count)
        map_transacion["Trans_amount"].append(t_amount)
#Get District wise User data
map_userpath="data/map/user/hover/country/india/state/"
agr=os.listdir(map_userpath)
for i in agr:
  path1=map_userpath+i+"/"
  agr2=os.listdir(path1)
  for l in agr2:
    path2=path1+l+"/"
    agr3=os.listdir(path2)
    for j in agr3:
      dat=open(path2+j,"r")
      data=json.load(dat)
      kt=data["data"]["hoverData"]
      for k in kt.keys():
        dis=k.replace("district","")
        Registered_User=kt[k]["registeredUsers"]
        Apps_Opens=kt[k]["appOpens"]
        map_user["State"].append(i)
        map_user["Year"].append(l)
        map_user["Quater"].append(int(j.strip(".json")))
        map_user["District"].append(dis)
        map_user["Registered_User"].append(Registered_User)
        map_user["Apps_Opens"].append(Apps_Opens)
#Get District wise insurance tranaction data
map_insurancepath="data/map/insurance/hover/country/india/state/"
agr=os.listdir(map_insurancepath)
for i in agr:
  path1=map_insurancepath+i+"/"
  agr2=os.listdir(path1)
  for l in agr2:
    path2=path1+l+"/"
    agr3=os.listdir(path2)
    for j in agr3:
      dat=open(path2+j,"r")
      data=json.load(dat)
      kt=data["data"]["hoverDataList"]
      for k in kt:
        dis=k["name"]
        t_count=k["metric"][0]["count"]
        t_amount=k["metric"][0]["amount"]
        map_insurance["State"].append(i)
        map_insurance["Year"].append(l)
        map_insurance["Quater"].append(int(j.strip(".json")))
        map_insurance["District"].append(dis)
        map_insurance["Trans_count"].append(t_count)
        map_insurance["Trans_amount"].append(t_amount)
#Get pincodet wise insurance tranaction data
top_inspath="data/top/insurance/country/india/state/"
top=os.listdir(top_inspath)
for i in top:
    path1=top_inspath+i+"/"
    top1=os.listdir(path1)
    for j in top1:
        path2=path1+j+"/"
        top2=os.listdir(path2)
        for k in top2:
          path3=path2+k
          topins=open(path3,'r')
          topinsdata=json.load(topins)
          pincode=topinsdata["data"]["pincodes"]
          for l in pincode:
            pin_code=l["entityName"]
            count=l["metric"]["count"]
            amount=l["metric"]["amount"]
            top_insurance["State"].append(i)
            top_insurance["Year"].append(j)
            top_insurance["Quater"].append(int(k.strip(".json")))
            top_insurance["Pincodes"].append(pin_code)
            top_insurance["Trans_count"].append(count)
            top_insurance["Trans_Amount"].append(amount)
#Get Pincode wise tranaction data
top_trapath="data/top/transaction/country/india/state/"
top=os.listdir(top_trapath)
for i in top:
    path1=top_trapath+i+"/"
    top1=os.listdir(path1)
    for j in top1:
        path2=path1+j+"/"
        top2=os.listdir(path2)
        for k in top2:
          path3=path2+k
          topins=open(path3,'r')
          topinsdata=json.load(topins)
          pincode=topinsdata["data"]["pincodes"]
          for l in pincode:
            pin_code=l["entityName"]
            count=l["metric"]["count"]
            amount=l["metric"]["amount"]
            top_transaction["State"].append(i)
            top_transaction["Year"].append(j)
            top_transaction["Quater"].append(int(k.strip(".json")))
            top_transaction["Pincodes"].append(pin_code)
            top_transaction["Trans_count"].append(count)
            top_transaction["Trans_Amount"].append(amount)
#Get Pincode wise User data
top_trapath="data/top/user/country/india/state/"
top=os.listdir(top_trapath)
for i in top:
    path1=top_trapath+i+"/"
    top1=os.listdir(path1)
    for j in top1:
        path2=path1+j+"/"
        top2=os.listdir(path2)
        for k in top2:
          path3=path2+k
          topins=open(path3,'r')
          topinsdata=json.load(topins)
          pincode=topinsdata["data"]["pincodes"]
          for l in pincode:
            pin_code=l["name"]
            count=l["registeredUsers"]
            top_user["State"].append(i)
            top_user["Year"].append(j)
            top_user["Quater"].append(int(k.strip(".json")))
            top_user["Pincodes"].append(pin_code)
            top_user["Registered_User"].append(count)
            
url="mysql+mysqlconnector://root:Vinay0511@127.0.0.1:3306/phonepe"
engine=create_engine(url,echo=True)
            
pd.DataFrame(Aggregated_insurance).to_sql("Aggregated_insurance",engine,if_exists="replace",index=False)
pd.DataFrame(Aggregated_transaction).to_sql("Aggregated_transaction",engine,if_exists="replace",index=False)
pd.DataFrame(Aggregated_user).to_sql("Aggregated_user",engine,if_exists="replace",index=False)
pd.DataFrame(Aggregated_user_All).to_sql("Aggregated_user_All",engine,if_exists="replace",index=False)
pd.DataFrame(map_insurance).to_sql("map_insurance",engine,if_exists="replace",index=False)
pd.DataFrame(map_transacion).to_sql("map_transacion",engine,if_exists="replace",index=False)
pd.DataFrame(map_user).to_sql("map_user",engine,if_exists="replace",index=False)
pd.DataFrame(top_insurance).to_sql("top_insurance",engine,if_exists="replace",index=False)
pd.DataFrame(top_transaction).to_sql("top_transaction",engine,if_exists="replace",index=False)
pd.DataFrame(top_user).to_sql("top_user",engine,if_exists="replace",index=False)


"""pd.DataFrame(Aggregated_insurance).to_csv("Aggregated_insurance.csv")
pd.DataFrame(Aggregated_transaction).to_csv("Aggregated_transaction.csv")
pd.DataFrame(Aggregated_user).to_csv("Aggregated_user.csv")
pd.DataFrame(Aggregated_user_All).to_csv("Aggregated_user_All.csv")
pd.DataFrame(map_insurance).to_csv("map_insurance.csv")
pd.DataFrame(map_transacion).to_csv("map_transacion.csv")
pd.DataFrame(map_user).to_csv("map_user.csv")
pd.DataFrame(top_insurance).to_csv("top_insurance.csv")
pd.DataFrame(top_transaction).to_csv("top_transaction.csv")
pd.DataFrame(top_user).to_csv("top_user.csv")    """    



        
        
        
    
