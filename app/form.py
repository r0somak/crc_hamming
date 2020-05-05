# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

lstCrc = [
    ('crc-8', 'crc-8'),
    ('crc-8-darc', 'crc-8-darc'),
    ('crc-8-i-code', 'crc-8-i-code'),
    ('crc-8-itu', 'crc-8-itu'),
    ('kermit', 'kermit'),
    ('crc-64-jones', 'crc-64-jones'),
    ('crc-64-we', 'crc-64-we'),
]


class CrcForm(FlaskForm):
    crcType = SelectField(u"CRC type", choices=lstCrc)