from wtforms import Form, StringField, PasswordField, IntegerField, SelectField
from wtforms import validators as v

class PlatformForm(Form):
    name = SelectField(
        'PLATFORM',
        choices=[("Binance", "Binance"), ("Coinbase Pro", "Coinbase Pro")],
        validators=[v.input_required()]
        )
    api_key = PasswordField(
        'API KEY', 
        validators=[v.input_required(),  v.length(min=7, message="Length must be at least %(min)d characters long")]
        )
    secret_key = PasswordField(
        'SECRET KEY', 
        validators=[v.input_required(),  v.length(min=8, message="Length must be at least %(min)d characters long")]
        )
    passphrase = PasswordField(
        'Passphrase'
        )
