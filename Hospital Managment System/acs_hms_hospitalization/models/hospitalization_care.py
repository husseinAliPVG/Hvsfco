# coding=utf-8

from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
import dateutil.relativedelta
from odoo.exceptions import ValidationError, AccessError, UserError, RedirectWarning, Warning
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Anaesthesia(models.Model):
    _name = "anaesthesia"
    _rec_name="name"
    _description = "Anesthesia"

    name = fields.Char('Anaesthesia Name', required=True)


class AdmissionCheckListTemplate(models.Model):
    _name="inpatient.checklist.template"
    _description = "Inpatient Checklist Template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")


class AdmissionCheckList(models.Model):
    _name="inpatient.checklist"
    _description = "Inpatient Checklist"

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Y/N", default=False)
    remark = fields.Char(string="Remarks")
    hospitalization_id = fields.Many2one("acs.hospitalization", ondelete="cascade", string="Hospitalization")


class PreOpetativeCheckListTemplate(models.Model):
    _name="pre.operative.check.list.template"
    _description = "Pre Operative Checklist Template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")


class PreOpetativeCheckList(models.Model):
    _name="pre.operative.check.list"
    _description = "Pre Operative Checklist"

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Done", default=False)
    remark = fields.Char(string="Remarks")
    surgery_id = fields.Many2one("hms.surgery", ondelete="cascade", string="Surgery")


class PreWardCheckListTemplate(models.Model):
    _name="pre.ward.check.list.template"
    _description = "Pre Ward Checklist Template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")


class PreWardCheckList(models.Model):
    _name="pre.ward.check.list"
    _description = "Pre Ward Checklist"

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Done", default=False)
    remark = fields.Char(string="Remarks")
    hospitalization_id = fields.Many2one("acs.hospitalization", ondelete="cascade", string="Hospitalization")


class PatientAccomodationHistory(models.Model):
    _name = "patient.accomodation.history"
    _rec_name = "patient_id"
    _description = "Patient Accomodation History"

    @api.one
    def _rest_days(self):
        self.ensure_one()
        for registration in self:
            if registration.end_date and registration.start_date:
                diff = (registration.end_date - registration.start_date).days
                self.days = diff if diff > 0 else 1
            else:
                self.days = 0

    hospitalization_id = fields.Many2one('acs.hospitalization', ondelete="cascade", string='Inpatient', required=True)
    patient_id = fields.Many2one('hms.patient', ondelete="restrict", string='Patient', required=True)
    ward_id = fields.Many2one('hospital.ward', ondelete="restrict", string='Ward/Room')
    bed_id = fields.Many2one('hospital.bed', ondelete="restrict", string='Bed No.')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    days = fields.Integer(compute=_rest_days, string='Total Rest Days')
    company_id = fields.Many2one('res.company', ondelete='restrict', 
        string='Institution', related='hospitalization_id.company_id') 


class WardRounds(models.Model):
    _name = "ward.rounds"
    _description = "Ward Rounds"

    instruction = fields.Char(string='Instruction')
    remarks = fields.Char(string='Remarks')          
    hospitalization_id = fields.Many2one('acs.hospitalization', ondelete="restrict",string='Inpatient')
    date = fields.Date(string='Date')
    execution_time = fields.Datetime(string='Execution Time')
    executed_by = fields.Many2one('res.users', ondelete="restrict", string='Executed By')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: