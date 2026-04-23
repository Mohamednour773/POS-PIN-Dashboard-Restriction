from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PosConfig(models.Model):
    _inherit = 'pos.config'

    @api.model
    def verify_pin_and_get_action(self, pin_code):
        """
        Verifies the PIN code against hr.employee and returns the POS dashboard action
        filtered by authorized POS configs.
        """
        if not pin_code:
            raise UserError(_("Please enter a PIN code."))

        # Search for employee with this PIN
        # Check if 'pin' field exists (might be missing if pos_hr is not installed correctly)
        if 'pin' not in self.env['hr.employee']._fields:
            return {
                'error': _("The Employee PIN system is not properly configured. Please ensure 'pos_hr' is installed.")
            }

        employee = self.env['hr.employee'].sudo().search([('pin', '=', pin_code)], limit=1)
        
        if not employee:
            return {
                'error': _("Invalid PIN code. Please try again.")
            }

        # Find POS configs where this employee is allowed
        # Odoo versions differ in field names (employee_ids, basic_employee_ids, etc.)
        # We search dynamically on all relevant employee fields that exist in the model
        employee_fields = ['employee_ids', 'minimal_employee_ids', 'basic_employee_ids', 'advanced_employee_ids']
        existing_fields = [f for f in employee_fields if f in self._fields]
        
        if not existing_fields:
            # If no employee fields exist, maybe the module isn't configured for employees
            # We return an empty set or maybe all? Let's return error to inform user.
            return {
                'error': _("No employee configuration found in Point of Sale. Please check your POS settings.")
            }

        domain = ['|'] * (len(existing_fields) - 1)
        for field in existing_fields:
            domain.append((field, 'in', employee.id))
        
        # We use sudo() to ensure we can read all configs for filtering purposes
        allowed_pos_configs = self.env['pos.config'].sudo().search(domain)

        # If the user is an admin, they might expect to see all? 
        # But we follow the request: "show only points where employee's pin code is added"
        
        action = self.env.ref('point_of_sale.action_pos_config_kanban').read()[0]
        action['domain'] = [('id', 'in', allowed_pos_configs.ids)]
        action['name'] = _("Authorized POS for %s") % employee.name
        
        # We can also add a context flag to indicate we are in "filtered mode"
        action['context'] = dict(self.env.context, search_default_available=1)
        
        return {
            'action': action
        }
