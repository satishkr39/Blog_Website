from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
    title = StringField("Title ", validators=[DataRequired()])
    text = TextField("Text", validators=[DataRequired()])
    submit = SubmitField("Submit")