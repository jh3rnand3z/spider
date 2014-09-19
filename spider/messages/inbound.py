import uuid

from schematics import models
from schematics import types


class Contact(models.Model):
    '''
        Outbound contact
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    account = types.StringType(required=True)
    first_name = types.StringType()
    last_name = types.StringType()
    phone_1 = types.StringType(required=True)
    phone_2 = types.StringType()
    phone_3 = types.StringType()


class Call(models.Model):
    '''
        Outbound call
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    # Specify where and how to call
    account = types.StringType(required=True)
    channel = types.StringType()
    callerid = types.StringType()
    max_retries = types.IntType(default=2)
    retry_time = types.IntType(default=300)
    wait_time = types.IntType(default=45)
    # If the call answers, connect it here
    context = types.StringType()
    extension = types.StringType()
    priority = types.IntType(default=1)
    # Set a variable for use in the extension logic
    set_var = types.StringType()
    # other stuff
    archive = types.StringType(default='no', choices=['yes',
                                                      'no'])