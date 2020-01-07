from troposphere import Sub, Ref
from troposphere import cognito

class UserPool:
    name = Sub("UserPoolName")
    allowAdminCreateUserOnly = False
    autoVerifiedAttributes = []
    schema = []

    def __init__(self, **kwargs):
        self.name = Sub(kwargs['name'])
        if 'AllowAdminCreateUserOnly' in kwargs:
            self.allowAdminCreateUserOnly = kwargs['AllowAdminCreateUserOnly']
        
        if 'AutoVerifiedAttributes' in kwargs:
            self.autoVerifiedAttributes = kwargs['AutoVerifiedAttributes']

        if 'Schema' in kwargs:
            self.schema= kwargs['Schema']

    def set_schema_attr(self, list_schema_attrs):
        attr_list = []
        if len(list_schema_attrs) > 0 :
            for attr in list_schema_attrs :
                attr_list.append(
                     cognito.SchemaAttribute(**{
                        "Name": attr['namew'],
                        "AttributeDataType" : attr['type'],
                        "Mutable" : attr['mutable'],
                        "Required" : attr['required']
                    })
                )
            self.schema = attr_list    
            return attr_list

        return False

    def getResource(self):
        
        adminCreateUserConfig = cognito.AdminCreateUserConfig(AllowAdminCreateUserOnly=self.allowAdminCreateUserOnly)

        return cognito.UserPool('UserPool', **{
            "UserPoolName" : self.name,
            "AdminCreateUserConfig": adminCreateUserConfig,
            "AutoVerifiedAttributes": self.autoVerifiedAttributes,
            "Schema": self.schema
        })


class UserPoolClient:
    userPoolId = Ref("UserPool")
    clientName = Sub("${Environment}UserPoolClient")
    generateSecret = True
    allowedOAuthFlows = []
    supportedIdentityProviders = []

    def __init__(self, **kwargs):
        if 'userPoolId' in kwargs:
            self.userPoolId = Ref(kwargs['userPoolId'])
        
        if 'clientName' in kwargs:
            self.clientName = Sub(kwargs['clientName'])

        if 'generateSecret' in kwargs:
            self.generateSecret = kwargs['generateSecret']

        if 'allowedOAuthFlows' in kwargs:
            self.allowedOAuthFlows = kwargs['allowedOAuthFlows']        
        
        if 'supportedIdentityProviders' in kwargs:
            self.supportedIdentityProviders = kwargs['supportedIdentityProviders']
        
    def getResource(self):
        return cognito.UserPoolClient(title="UserPoolClient", **{
            'UserPoolId': self.userPoolId,
            'ClientName': self.clientName,
            'GenerateSecret': self.generateSecret,
            'AllowedOAuthFlows': self.allowedOAuthFlows,
            'SupportedIdentityProviders': self.supportedIdentityProviders
        })

class UserPoolDomain:

    domain = Ref("AuthDomain")
    userPoolId = Ref("UserPool")

    def __init__(self, **kwargs):

        if 'domain' in kwargs:
            self.domain = Ref(kwargs['domain'])
        if 'userPoolId' in kwargs['userPoolId']:
            self.userPoolId = Ref(kwargs['userPoolId'])

    def getResource(self):
        return cognito.UserPoolDomain(title="UserPoolDomain", **{
            'Domain': self.domain,
            'UserPoolId': self.userPoolId
        })
    