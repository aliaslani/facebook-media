from django.urls import path
from market.views import TotalProductSales, TotalProductSalesByCountry, MonthlyProductSales, ProductSalesPerCountryCrosstab, LastTenSales


urlpatterns = [
    path("total-product-sales/", TotalProductSales.as_view(), name="total-product-sales"),
    path("total-product-country/", TotalProductSalesByCountry.as_view(), name="total-product-country"),
    path("total-monthly-sales/", MonthlyProductSales.as_view(), name="total-monthly-sales"),
    path("total-product-sales-per-country/", ProductSalesPerCountryCrosstab.as_view(), name="total-product-sales-per-country"),
    path("last-ten-sales/", LastTenSales.as_view(), name="last-ten-sales"),
    ]