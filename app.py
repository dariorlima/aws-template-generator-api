from flask import Flask, request
from troposphere import Template
from resources import BucketResource
from dispatcher import dispatcher, generateParams
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def generate_template():
    _template = request.get_json()

    template = Template()
    template.set_version('2010-09-09')
    template.set_description(_template['description'])

    params = _template['parameters']

    params = generateParams(params)

    for param in params:
        template.add_parameter(param)

    resources = _template['resources']
    
    for resource in resources:
        template.add_resource(dispatcher(resource))

    return template.to_dict()

if __name__ == '__main__':
    app.run()