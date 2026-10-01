
import pandas as pd
import matplotlib.pyplot as plt



X = pd.read_excel("Online Retail.xlsx")

print("حجم البيانات:", X.shape)
print(X.head())
print("\nأسماء الأعمدة:")
print(X.columns.tolist())
print("\nمعلومات الأعمدة وأنواعها:")
X.info()
print("\nعدد القيم الناقصة في كل عمود:")
print(X.isna().sum())


X["InvoiceDate"] = pd.to_datetime(
    X["InvoiceDate"],
    format="%m/%d/%Y %H:%M"
)
analysis_data = X.copy()
analysis_data["LineValue"] = analysis_data["Quantity"] * analysis_data["UnitPrice"]
analysis_data["Month"] = analysis_data["InvoiceDate"].dt.to_period("M")
normal_sale_mask = (
    (analysis_data["Quantity"] > 0)
    & (analysis_data["UnitPrice"] > 0)
   & (~analysis_data["InvoiceNo"].astype("string").str.startswith("C", na=False))
  )  
print("عدد أسطر البيع العادي:", normal_sale_mask.sum())
print("إجمالي قيمة أسطر البيع العادي:", analysis_data.loc[normal_sale_mask, "LineValue"].sum())
cancellation_mask = analysis_data["InvoiceNo"].astype("string").str.startswith("C", na=False)
print("إجمالي قيمة أسطر الإلغاء:", analysis_data.loc[cancellation_mask, "LineValue"].sum())
print("عدد أسطر الإلغاء:", cancellation_mask.sum())
print("عدد فواتير الإلغاء المختلفة:", analysis_data.loc[cancellation_mask, "InvoiceNo"].nunique())
monthly_sales = analysis_data.loc[normal_sale_mask].groupby("Month")["LineValue"].sum()
print(monthly_sales)
monthly_cancellations = analysis_data.loc[cancellation_mask].groupby("Month")["LineValue"].sum()
print(monthly_cancellations)
monthly_net = monthly_sales.add(monthly_cancellations, fill_value=0)
print(monthly_net)
monthly_cancellation_rate = monthly_cancellations.abs().div(monthly_sales) * 100
print(monthly_cancellation_rate)
country_sales = (
    analysis_data.loc[normal_sale_mask]
    .groupby("Country")["LineValue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(country_sales)
non_product_codes = ["POST", "DOT", "M"]
product_mask = normal_sale_mask & (~analysis_data["StockCode"].isin(non_product_codes))
product_sales = (
    analysis_data.loc[product_mask]
    .groupby("StockCode")["LineValue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(product_sales)
top_product_descriptions = analysis_data.loc[
    product_mask & analysis_data["StockCode"].isin(product_sales.index),
    ["StockCode", "Description"]
].dropna().drop_duplicates()

print(top_product_descriptions)
product_country_sales = (
    analysis_data.loc[product_mask]
    .groupby("Country")["LineValue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("أعلى 10 دول حسب مبيعات المنتجات فقط:")
print(product_country_sales)
monthly_summary = pd.concat(
    [
        monthly_sales.rename("GrossSales"),
        monthly_cancellations.rename("CancellationValue"),
        monthly_net.rename("NetSales"),
        monthly_cancellation_rate.rename("CancellationRatePct")
    ],
    axis=1
)

print(monthly_summary.round(2))
monthly_summary.to_csv("monthly_sales_summary.csv")

months = monthly_summary.index.astype(str)

plt.figure(figsize=(12, 6))
plt.plot(months, monthly_summary["GrossSales"] / 1000, marker="o", label="Gross sales")
plt.plot(months, monthly_summary["NetSales"] / 1000, marker="o", label="Net sales after cancellations")

plt.title("Monthly Sales Before and After Cancellations\n(December 2011 is partial)")
plt.xlabel("Month")
plt.ylabel("Amount (£ thousands)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.subplots_adjust(left=0.18)
plt.savefig(
    r"C:\Users\compu city\Downloads\monthly_sales_chart.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.figure(figsize=(12, 6))
plt.bar(months, monthly_summary["CancellationRatePct"], color="tomato")

plt.title("Monthly Cancellation Value as % of Gross Sales\n(December 2011 is partial)")
plt.xlabel("Month")
plt.ylabel("Cancellation value (% of gross sales)")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    r"C:\Users\compu city\Downloads\monthly_cancellation_rate.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
