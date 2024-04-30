# Vendor_self_service_portal-odoo-
Vendor Adjustment Request Module
Description
The Vendor Adjustment Request module facilitates the management of adjustment requests submitted by vendors. It allows users to create adjustment requests associated with specific sale orders, track their status, and communicate with vendors regarding the adjustments.

Classes and Fields
VendorAdjustmentRequest Class
_name: 'vendor.adjustment.request'
_description: 'Vendor Adjustment Request'
Fields
order_id: Many2one field referencing 'sale.order' model, representing the associated order reference.
adjustment_detail: Text field for providing details of the requested adjustment.
comment: Text field for additional comments.
date_request: Datetime field representing the request date, defaulted to the current datetime.
state: Selection field indicating the status of the adjustment request, with options 'draft', 'sent', and 'done'.
Methods
action_send_email: Sends an email notification regarding the adjustment request to the relevant parties.
submit_adjustment_request: Submits the adjustment request, updating its state to 'sent' and returning an action to view the list of adjustment requests.
VendorForecast Class
Methods
action_vendor_forecast_download_report: Generates and downloads a report in Excel format containing vendor forecast data.
generate_report_data: Generates report data based on applied filters.
Dependencies
This module depends on the 'sale' module for the sale order reference (sale.order model).
It utilizes the 'base' module for email template functionality (base.model_vendor_adjustment_request).
It requires the 'vendor_adjustment_request' module for email template functionality (vendor_adjustment_request.email_template_vendor_adjustment_request).
Vendor Forecast Module
Description
The Vendor Forecast module facilitates the generation and management of forecasts for vendor products. It provides functionality to filter and download forecast reports in Excel format.

Classes and Fields
VendorForecast Class
Methods
action_vendor_forecast_download_report: Generates and downloads a report in Excel format containing vendor forecast data.
generate_report_data: Generates report data based on applied filters.
VendorForecastFilter Class
_name: 'vendor.forecast.filter'
_description: 'Vendor Forecast Filter'
Fields
product_id: Many2one field referencing 'product.product' model, representing the product for which forecast is filtered.
date_from: Date field representing the starting date for the forecast filter.
date_to: Date field representing the ending date for the forecast filter.
Methods
apply_filter: Applies the specified filters to the forecast data.
Dependencies
This module depends on the 'product' module for product data (product.product model).
It utilizes the 'vendor_forecast' module for forecast data (vendor.forecast model).
It requires the 'xlsxwriter' library for generating Excel reports.
