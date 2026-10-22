from services.sales_manager import SalesManager


sales_manager = SalesManager()


print("\n" + "=" * 50)
print("OPEN ORDER UI TEST")
print("=" * 50)


# =========================================================
# GET AVAILABLE TABLES
# =========================================================

tables = sales_manager.get_available_tables()

if not tables:

    print("No available tables.")

else:

    table = tables[0]

    print(
        f"Selected Table: {table.table_number}"
    )


    # =====================================================
    # CREATE OPEN ORDER
    # =====================================================

    success, result = (
        sales_manager
        .create_open_order(
            1,                  # customer_id
            1,                  # user_id
            table.table_id
        )
    )

    print(
        "Create Order:",
        success
    )

    print(
        "Result:",
        result
    )


    if success:

        order_id = result

        # =================================================
        # ADD ITEM
        # =================================================

        success, result = (
            sales_manager
            .add_item_to_order(
                order_id,
                1,      # product_id
                2       # quantity
            )
        )

        print(
            "Add Item:",
            success
        )

        print(
            "Total:",
            result
        )

        print(
            f"\nOpen Order Created: #{order_id}"
        )