import requests
import urllib3
import stdiomask



urllib3.disable_warnings()



def checkssid():
   try:
      szip = input("\nEnter the IP of Controller: ")
      szuser = input("Username: ")
      szpass = stdiomask.getpass(prompt = 'Password: ')

      login = f'https://{szip}:8443/wsg/api/public/v8_2/session'
      logout  = f'https://{szip}:8443/wsg/api/public/v8_2/session'
      baseurl = f'https://{szip}:8443/wsg/api/public/'


      session = requests.session()
      response = session.post(login, json={"username": f"{szuser}", "password": f"{szpass}", "timeZoneUtcOffset": "+08:00"}
                         , verify=False)
      headers = {'Content-Type': 'application/json'}

      if response.status_code == 200:
         getallzones = session.get(baseurl  +'v8_2/rkszones?listSize=1000',  verify=False)#get all of the zones
         result = getallzones.json()#convert  to json format
         for ids in result.get('list'):
            try:
               zoneid = ids['id']#get zone id
               name = ids['name']#get zone name
               print("\nZone name: " + name)
               getallzonesssid = session.get(baseurl + f'/v8_2/rkszones/{zoneid}/wlans?listSize=1000', verify=False,headers=headers)#get all of the zones SSID
               result2 = getallzonesssid.json()#convert it to json format
               for names in result2.get('list'):
                  ssid_id = names['id']
                  getallssidparameters = session.get(baseurl + f'/v8_2/rkszones/{zoneid}/wlans/{ssid_id}?listSize=1000', verify=False, headers=headers)#get all of the parameters of all SSID per Zones
                  wlansconfig = getallssidparameters.json()#convert  to json format
                  essid = wlansconfig['ssid']
                  print("SSID: " + essid)
            except:
               print('\t')

            print("\n")
      else:
         print("UNAUTHORIZED USER")

      session.delete(logout, verify=False)
      print("\nLogout SuccessFul !")

   except requests.exceptions.ConnectionError:
      print("\nCould not connect to the controller")
      again()
   except:
      print("\nIncorrect Username or Password")
      again()

def again():
    repeat_again = input("\nDo you want to continue? \n Please type 'Y' for yes or 'N' for No : ")
    if repeat_again.upper() == 'Y':
        checkssid()
    elif repeat_again.upper() == 'N':
        print("\n\nThank you See you Later!")
    else:
        again()

checkssid()
