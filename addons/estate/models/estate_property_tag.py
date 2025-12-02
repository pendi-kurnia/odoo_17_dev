from odoo import models, fields, _

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Estate Property Tag"

    name= fields.Char(
        required=True
        ) 
    color= fields.Integer(
        default=1
        )