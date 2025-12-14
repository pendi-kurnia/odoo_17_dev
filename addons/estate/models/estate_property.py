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
        string="Garden"
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
    total_area = fields.Float(
        compute="_compute_total_area",
        string="Total Area (sqm)",
        readonly=True,
    )
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    best_price = fields.Float(
        compute="_compute_best_price",
        string="Best Offer",
        readonly=True,
    )
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area =10
            self.garden_orientation = "north"
        else :
            self.garden_atrea = None
            self.garden_orientation = None

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
            return {
            'warning': {
                'title': 'warning',
                'message': 'this option will enable Garden Area (default: 10) &  Orientation (default: north)',
            }
        }
        else:
            self.garden_area = 0
            self.garden_orientation = False

















