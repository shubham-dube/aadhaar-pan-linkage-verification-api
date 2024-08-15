from flask import Flask, jsonify, Response, make_response, request
import requests
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

@app.route("/api/v1/check-PAN-aadhaar-linkage", methods=["POST"])
def check_PAN_aadhaar_linkage():
    try:
        post_url = "https://eportal.incometax.gov.in/iec/servicesapi/getEntity"

        PAN = request.json.get("PAN")
        aadhaar = request.json.get("aadhaar")
        session = requests.Session()
    
        postBody = {
            "aadhaarNumber": aadhaar,
            "pan": PAN,
            "preLoginFlag": "Y",
            "serviceName": "linkAadhaarPreLoginService"
        }

        response = session.post(post_url, json=postBody)

        objectBody = response.json()

        # linkedAadhaarNumber = objectBody['aadhaarNumber']
        # errors = objectBody['errors']
        # isMigrated = objectBody['isMigrated']
        description = objectBody['messages'][0]['desc']
        print(description)

        withGivenAadhar = None
        withGivenPAN = None
        isPanExist = None
        isAadhaarValid = None
        isPanInactive = None

        if("valid 12 digit Aadhaar" in description):
            isAadhaarValid = False
            jsonResponse = {
                "isPanExist": "Unknown",
                "isAadhaarValid": isAadhaarValid,
                "linkedAadharNumber": "Unknown",
                "linkedPanNumber": "Unknown",
                "isPanLinkedToAdhaar": "Unknown",
                "description": description
            }
            return jsonify(jsonResponse)
        
        if("PAN entered is inactive"in description):
            isAadhaarValid = True
            jsonResponse = {
                "isPanExist": True,
                "isAadhaarValid": isAadhaarValid,
                "linkedAadharNumber": "Unknown",
                "linkedPanNumber": "Unknown",
                "isPanLinkedToAdhaar": False,
                "description": description
            }
            return jsonify(jsonResponse)
        
        if("enter valid Pan Card" in description):
            jsonResponse = {
                "isPanExist": False,
                "isAadhaarValid": "Unknown",
                "linkedAadharNumber": "Unknown",
                "linkedPanNumber": "Unknown",
                "isPanLinkedToAdhaar": "Unknown",
                "description": description
            }
            return jsonify(jsonResponse)
        if(("Your PAN" in description) and ("is already linked to given Aadhaar" in description)):
            jsonResponse = {
                "isPanExist": True,
                "isAadhaarValid": True,
                "linkedAadharNumber": objectBody['aadhaarNumber'],
                "linkedPanNumber": objectBody['pan'],
                "isPanLinkedToAdhaar": True,
                "description": description
            }
            return jsonify(jsonResponse)
        
        if(("Your PAN" in description) and ("is linked to some other Aadhaar" in description)):
            jsonResponse = {
                "isPanExist": True,
                "isAadhaarValid": True,
                "linkedAadharNumber": objectBody['aadhaarNumber'],
                "linkedPanNumber": objectBody['pan'],
                "isPanLinkedToAdhaar": True,
                "description": description
            }
            return jsonify(jsonResponse)
        
        if(("Your Aadhaar Number" in description) and ("is linked to some other PAN" in description)):
            jsonResponse = {
                "isPanExist": True,
                "isAadhaarValid": True,
                "linkedAadharNumber": objectBody['aadhaarNumber'],
                "linkedPanNumber": objectBody['pan'],
                "isPanLinkedToAdhaar": True,
                "description": description
            }
            return jsonify(jsonResponse)
        else:
            jsonResponse = {
                "isPanExist": "Unknown",
                "isAadhaarValid": "Unknown",
                "linkedAadharNumber": "Unknown",
                "linkedPanNumber": "Unknown",
                "isPanLinkedToAdhaar": False,
                "description": description
            }
            return jsonify(jsonResponse)
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Error in Checking the linkage status of PAN and Aadhaar."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(asgi_app, host='0.0.0.0', port=5001)