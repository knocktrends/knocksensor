from wtforms import Form, validators, StringField, IntegerField


class UserProfileForm(Form):
    """
    Form for collecting user information

    Needed payload:
    {
        "username": "TestUser",
        "device_id": "00:00:00:00:00"
        "expire_threshold": 123,
        "failed_attempts_threshold": 2,
        "remaining_use_threshold": 2,
        "send_no_earlier": 123,
        "send_no_later": 555,
        "success_threshold": 1,
        "name": "ifttt_success",
        "failure_endpoint": "ifttt_failure",
        "ifttt_secret": "asdf"
    }
    """
    username = StringField('Username:', validators=[validators.required()])
    device_id = StringField('Device Id:', validators=[validators.required(),
                                                      validators.length(min=14, max=14)])
    expire_threshold = IntegerField('Expire Threshold:', validators=[validators.required(),
                                                                     validators.NumberRange(min=0, max=999999)])
    failed_attempts_threshold = IntegerField('Failed Attempts Threshold:',
                                             validators=[validators.required(),
                                                         validators.NumberRange(min=1, max=999999)])
    remaining_use_threshold = IntegerField('Remaining Use Threshold:',
                                           validators=[validators.required(),
                                                       validators.NumberRange(min=0, max=999999)])
    send_no_earlier = IntegerField('Send No Earlier:',
                                   validators=[validators.required(),
                                               validators.NumberRange(min=0, max=999999)])
    send_no_later = IntegerField('Send No Later:',
                                 validators=[validators.required(),
                                             validators.NumberRange(min=0, max=999999)])
    success_threshold = IntegerField('Success Threshold:',
                                     validators=[validators.required(),
                                                 validators.NumberRange(min=0, max=999999)])
    name = StringField('Device Name:', validators=[validators.required(),
                                                   validators.length(min=1, max=20)])
    failure_endpoint = StringField('Failure Endpoint:',
                                   validators=[validators.required(),
                                               validators.length(min=1, max=250)])
    ifttt_secret = StringField('IFTTT Secret:',
                               validators=[validators.required(),
                                           validators.length(min=1, max=64)])
