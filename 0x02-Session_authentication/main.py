#!/usr/bin/env python
import requests

if __name__ == "__main__":
    user_email = "u@hbtn.io"
    r = requests.post('http://localhost:5000/api/v1/auth_session/login', data={ 'email': user_email })
    if r.status_code != 400:
        print("Wrong status code: {}".format(r.status_code))
        exit(1)
    if r.headers.get('content-type') != "application/json":
        print("Wrong content type: {}".format(r.headers.get('content-type')))
        exit(1)
    
    try:
        r_json = r.json()
        
        if len(r_json.keys()) != 1:
            print("Not the right number of element in the JSON: {}".format(r_json))
            exit(1)
        
        error_value = r_json.get('error')
        if error_value is None:
            print("Missing 'error' key in the JSON: {}".format(r_json))
            exit(1)
        if error_value != "password missing":
            print("'error' doesn't have the right value: {}".format(error_value))
            exit(1)
            
        print("OK", end="")
    except:
        print("Error, not a JSON")
