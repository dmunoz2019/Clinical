# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPatient(models.Model):
    _name = 'res.patient'
    _description = 'Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}

    # sequence for patient
    _sql_constraints = [
        ('patient_id_unique',
         'UNIQUE(patient_id)',
         "Patient ID must be unique"),
    ]

    
    def _compute_patient_number(self):
        return self.env['ir.sequence'].next_by_code('res.patient')
        
    patient_id = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('res.patient'))
    patient_name = fields.Char(string='Patient Name', required=True , related='partner_id.name', store=True, readonly=False) 
    blood_type = fields.Selection([
        ('a+', 'A+'), 
        ('a-', 'A-'),
        ('b+', 'B+'), 
        ('b-', 'B-'),
        ('ab+', 'AB+'), 
        ('ab-', 'AB-'),
        ('o+', 'O+'), 
        ('o-', 'O-')
    ], string='Blood Type')
    doctor_id = fields.Many2one('res.doctor', string='Doctor')
    channel_ids = fields.Many2many(
    "discuss.channel",
    "patient_discuss_channel_member",  # New unique relation table name
    "res_patient_id",  # Column for 'res.patient'
    "channel_id",  # Column for 'discuss.channel'
    string="Channels",
    copy=False,)
    meeting_ids = fields.Many2many('calendar.event', 'calendar_event_res_patient_rel', 'patient_id',
                                   'calendar_event_id', string='Meetings', copy=False)
    consultations_ids = fields.One2many(
        comodel_name='health.consultation',  # Replace with your consultation model's name
        inverse_name='patient_id',           # Field in 'health.consultation' that refers to 'res.patient'
        string='Consultations'
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade')
    def _get_mail_thread_data(self, request_list):
        res = super(ResPatient, self)._get_mail_thread_data(request_list)
        return res

    