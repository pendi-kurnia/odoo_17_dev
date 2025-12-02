from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(
        required=True,
        string="Title"
        )
    description = fields.Text(
        string="Description"
        )
    postcode = fields.Char(
        string="Postcode"
        )
    date_availability = fields.Date(
        copy=False,
        default=lambda self:(fields.Datetime.now()+relativedelta(months=3)),
        string="Available From"
        )
    expected_price = fields.Float(
        required=True,
        string="Expected Price"
        )
    selling_price = fields.Float(
        readonly=True,
        copy=False,
        string="Selling Price")
    bedrooms = fields.Integer(
        default=2
        )
    living_area = fields.Integer(
        string=" Living Area (sqm)"
        )
    facades = fields.Integer(
        string="Facedes"
        )
    garage = fields.Boolean(
        string="Garage"
        )
    garden = fields.Boolean(
        string="gaqrden"
        )
    garden_area = fields.Integer(
        string=" Garden Area (sqm)"
        )
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation",
        default='north'
        )
    active = fields.Boolean(
        default=False
        )
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string="Status",
        required=True,
        copy=False,
        default='new',
        )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property type"
        )
    buyer_id = fields.Many2one(
        "res.partner",
        index=True,
        string="Buyer",
        copy=False,
        )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags"
        )  
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        )
 













