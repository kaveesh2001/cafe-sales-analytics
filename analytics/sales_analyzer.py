import pandas as pd

from database.connection import get_connection


class SalesAnalyzer:

    # =========================================================
    # SALES DATA RETRIEVAL
    # =========================================================

    def get_sales_data(self):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                o.order_id,
                o.order_date,
                o.order_time,
                o.status,
                oi.product_id,
                p.product_name,
                p.category,
                oi.quantity,
                oi.unit_price,
                oi.subtotal
            FROM orders o
            JOIN order_item oi
                ON o.order_id = oi.order_id
            JOIN product p
                ON oi.product_id = p.product_id
            WHERE o.status = 'Completed'
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        columns = [
            "order_id",
            "order_date",
            "order_time",
            "status",
            "product_id",
            "product_name",
            "category",
            "quantity",
            "unit_price",
            "subtotal"
        ]

        dataframe = pd.DataFrame(
            rows,
            columns=columns
        )

        return dataframe


    # =========================================================
    # TOTAL REVENUE
    # =========================================================

    def get_total_revenue(self, dataframe):
        total_revenue = dataframe["subtotal"].sum()

        return total_revenue


    # =========================================================
    # TOTAL ORDERS
    # =========================================================

    def get_total_orders(self, dataframe):
        total_orders = dataframe["order_id"].nunique()

        return total_orders


    # =========================================================
    # AVERAGE ORDER VALUE
    # =========================================================

    def get_average_order_value(self, dataframe):

        total_revenue = self.get_total_revenue(
            dataframe
        )

        total_orders = self.get_total_orders(
            dataframe
        )

        if total_orders == 0:
            return 0

        average_order_value = (
            total_revenue / total_orders
        )

        return average_order_value


    # =========================================================
    # BEST SELLING PRODUCT
    # =========================================================

    def get_best_selling_product(self, dataframe):

        product_sales = (
            dataframe
            .groupby("product_name")["quantity"]
            .sum()
        )

        best_product = product_sales.idxmax()

        quantity_sold = product_sales.max()

        return best_product, quantity_sold


    # =========================================================
    # CATEGORY ANALYSIS
    # =========================================================

    def get_category_analysis(self, dataframe):

        category_analysis = (
            dataframe
            .groupby("category")
            .agg(
                total_quantity=("quantity", "sum"),
                total_revenue=("subtotal", "sum")
            )
            .sort_values(
                "total_revenue",
                ascending=False
            )
        )

        return category_analysis


    # =========================================================
    # PEAK SALES TIME
    # =========================================================

    def get_peak_sales_time(self, dataframe):

        dataframe = dataframe.copy()

        dataframe["hour"] = (
            dataframe["order_time"]
            .dt.total_seconds() // 3600
        )

        hourly_sales = (
            dataframe
            .groupby("hour")["quantity"]
            .sum()
        )

        peak_hour = hourly_sales.idxmax()

        quantity_sold = hourly_sales.max()

        return int(peak_hour), int(quantity_sold)


    # =========================================================
    # BUSINESS INSIGHTS
    # =========================================================

    def generate_business_insights(self, dataframe):

        insights = []

        total_revenue = (
            self.get_total_revenue(
                dataframe
            )
        )

        total_orders = (
            self.get_total_orders(
                dataframe
            )
        )

        average_order_value = (
            self.get_average_order_value(
                dataframe
            )
        )

        best_product, quantity_sold = (
            self.get_best_selling_product(
                dataframe
            )
        )

        category_analysis = (
            self.get_category_analysis(
                dataframe
            )
        )

        peak_hour, peak_quantity = (
            self.get_peak_sales_time(
                dataframe
            )
        )

        best_category = (
            category_analysis["total_revenue"]
            .idxmax()
        )

        insights.append(
            f"Total revenue generated is "
            f"Rs. {total_revenue:.2f}."
        )

        insights.append(
            f"The café received "
            f"{total_orders} completed orders."
        )

        insights.append(
            f"The average order value is "
            f"Rs. {average_order_value:.2f}."
        )

        insights.append(
            f"{best_product} is the best-selling "
            f"product with {quantity_sold} units sold."
        )

        insights.append(
            f"{best_category} is the highest "
            f"revenue-generating category."
        )

        insights.append(
            f"Peak sales occur around "
            f"{peak_hour}:00 with "
            f"{peak_quantity} items sold."
        )

        return insights


    # =========================================================
    # DAILY SALES
    # =========================================================

    def get_daily_sales(self, dataframe):

        daily_sales = (
            dataframe
            .groupby("order_date")["subtotal"]
            .sum()
            .reset_index()
        )

        return daily_sales


    # =========================================================
    # HOURLY SALES
    # =========================================================

    def get_hourly_sales(self, dataframe):

        dataframe = dataframe.copy()

        dataframe["hour"] = (
            dataframe["order_time"]
            .dt.total_seconds() // 3600
        )

        hourly_sales = (
            dataframe
            .groupby("hour")["quantity"]
            .sum()
            .reset_index()
        )

        hourly_sales["hour"] = (
            hourly_sales["hour"].astype(int)
        )

        return hourly_sales


    # =========================================================
    # PRODUCT PERFORMANCE
    # =========================================================

    def get_product_performance(self, dataframe):

        product_performance = (
            dataframe
            .groupby("product_name")
            .agg(
                total_quantity=("quantity", "sum"),
                total_revenue=("subtotal", "sum")
            )
            .sort_values(
                "total_quantity",
                ascending=False
            )
        )

        return product_performance