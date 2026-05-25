from django.shortcuts import render
from django.db.models import Count, Sum
from slick_reporting.views import ReportView, Chart, ListReportView
from slick_reporting.fields import ComputationField
from market.models import Product, Sales


class TotalProductSales(ReportView):
    template_name = "market/total_sale_chart.html"
    report_model = Sales
    date_field = 'doc_date'
    group_by = 'product'
    columns = [
        "name",

    ComputationField.create(
        Sum, "quantity", verbose_name="Total quantity Sold", is_summable=True,
    ),
    ComputationField.create(
        Sum, "value", name="sum__value", verbose_name="Total value Sold $",
    )
    ]
    chart_settings = [
        Chart(
            "Total Sold",
            Chart.BAR,
            data_source=["sum__value"],
            title_source=["name"],
        ),
        Chart(
            "Total Sold [PIE]",
            Chart.PIE,
            data_source=["sum__value"],
            title_source=["product_name"],
        )
    ]


class TotalProductSalesByCountry(ReportView):
    report_model = Sales
    date_field = 'doc_date'
    group_by = 'client__country'
    columns = [
        'client__country',
        ComputationField.create(
            Sum, "value", name="sum__value",
            verbose_name="Total value Sold by Country",
        ),
    ]
    chart_settings = [
        Chart(
            "Total Sold",
            Chart.PIE,
            data_source=["sum__value"],
            title_source=["client__country"],
        )
    ]

class SumValueComputationField(ComputationField):
    calculation_field = "value"
    calculation_method = Sum
    verbose_name = "Sales Value"
    name = "my_value_sum"

class MonthlyProductSales(ReportView):
    report_model = Sales
    date_field = 'doc_date'
    group_by = 'product'
    columns = ["name", "sku"]

    time_series_pattern = "monthly"
    time_series_columns = [
        SumValueComputationField,
    ]
    chart_settings = [
        Chart(
            "Total Sold",
            Chart.PIE,
            data_source=["my_value_sum"],
            title_source=["name"],
            plot_total=True,
        ),
        Chart(
            "Sales Monthly [Bar]",
            Chart.COLUMN,
            data_source=["my_value_sum"],
            title_source=["name"],
        )
    ]

class ProductSalesPerCountryCrosstab(ReportView):
    report_model = Sales
    date_field = 'doc_date'
    group_by = "product"
    crosstab_field = "client__country"
    crosstab_columns = [
        SumValueComputationField,
    ]
    crosstab_ids = [
        "client__country",
    ]
    crosstab_compute_remainder = True
    columns = [
        "name",
        "sku",
        "__crosstab__",
        SumValueComputationField,
    ]

class LastTenSales(ListReportView):
    report_model = Sales
    report_title = "Last 10 sales"
    date_field = "doc_date"
    filters = ["product", "client", "doc_date"]
    columns = [
        "product__name",
        "client__name",
        "doc_date",
        "quantity",
        "price",
        "value",
    ]
    default_order_by = "-doc_date"
    limit_records = 10