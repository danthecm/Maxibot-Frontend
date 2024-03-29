from wtforms import Form, StringField, PasswordField, IntegerField, SelectField
from wtforms import validators as v

class RegisterForm(Form):
    name = StringField(
        'Full Name', 
        validators=[v.input_required(), v.length(min=8, message="Length must be at least %(min)d characters long")
        ])
    email = StringField(
        'Email', 
        validators=[v.email(), v.input_required()]
        )
    phone = IntegerField(
        "Phone", 
        validators=[v.input_required()]
    )
    password = PasswordField(
        'Password', 
        validators=[v.data_required(), v.equal_to('confirm', message='Passwords must match'), v.length(min=8, message="Length must be at least %(min)d characters long")]
        )
    confirm = PasswordField(
        'Confirm Password', validators=[v.input_required()]
        )

class LoginForm(Form):
    email = StringField(
        'Email', 
        validators=[v.email(), v.input_required()]
        )
    password = PasswordField(
        'Password', 
        validators=[v.data_required()]
        )