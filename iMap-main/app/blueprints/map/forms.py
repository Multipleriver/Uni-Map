from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField

class CoordinateForm(FlaskForm):
    lng = FloatField(label="经度", render_kw={"placeholder": "请输入经度"})
    lat = FloatField(label="纬度", render_kw={"placeholder": "请输入纬度"})
    address = StringField(label="详细地址", render_kw={"placeholder": "请输入详细地址"})
    tag = StringField(label="标签", render_kw={"placeholder": "请输入标签"})
    submit = SubmitField(label="添加")
