from resources import BucketResource, Cognito
from troposphere import Parameter

def generateParams(params): 
    parameters = []

    for param in params: 
        noecho = param['noecho'] if 'noecho' in param else False
        parameters.append(
            Parameter(
                param['name'],
                Type=param['type'], 
                Description=param['description'],
                NoEcho=noecho
            )
        )

    return parameters

def dispatcher(resource):

    if(resource['id'] == 's3-bucket'):
        r = BucketResource.BucketResource(BucketName=resource['BucketName'])
        return r.getResource()

    if(resource['id'] == 'cognito-userpool'):
        r = Cognito.UserPool(**resource)
        return r.getResource()
    
    if(resource['id'] == 'cognito-userpool-client'):
        r = Cognito.UserPoolClient(**resource)
        return r.getResource()

    if(resource['id'] == 'cognito-userpool-domain'):
        r = Cognito.UserPoolDomain(**resource)
        return r.getResource()
