$ pip install psycopg2
$ pip freeze > requirements.txt
import urllib
import json
import os
from flask import Flask
from flask import request
from flask import make_response
#connection to heroku database
import psycopg2
import urlparse
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["postgres://zejdwoyqvispdp:fce5ba7eea7d4d34ba8f5bb53217504523086195be1d662494ac92b01f6b7f73@ec2-54-228-189-223.eu-west-1.compute.amazonaws.com:5432/dcemdk759ojm1j"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.zejdwoyqvispdp,
    password=url.fce5ba7eea7d4d34ba8f5bb53217504523086195be1d662494ac92b01f6b7f73,
    host=url.ec2-54-228-189-223.eu-west-1.compute.amazonaws.com,
    port=url.5432
)
# Flask app should start in global layout
app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    print(res)
   r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "ask.question":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    #type = parameters.get("type")
	type = select('name', 'serie') from('produits')
    speech = "Ok, j'ai l'ordinateur qu'il vous faut : " + type 
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
	print "Starting app on port %d" % port
    app.run(debug=True, port=port, host='0.0.0.0')

	
