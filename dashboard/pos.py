from pathlib import Path

import streamlit as st

from services.sales_manager import SalesManager


# =========================================================
# IMAGE HELPERS
# =========================================================

def get_project_root():

    return (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )


def get_local_image_path(image_source):

    if not image_source:
        return None

    image_source = str(
        image_source
    ).strip()

    # -----------------------------------------------------
    # Remote image URL
    # -----------------------------------------------------

    if (
        image_source.startswith("http://")
        or image_source.startswith("https://")
    ):
        return image_source

    # -----------------------------------------------------
    # Local image path
    # -----------------------------------------------------

    project_root = get_project_root()

    image_path = (
        project_root
        / image_source
    )

    if image_path.exists():
        return str(image_path)

    return None


def display_product_image(
    image_source,
    width=160
):

    image_path = get_local_image_path(
        image_source
    )

    if image_path:

        try:

            st.image(
                image_path,
                width=width
            )

        except Exception:

            st.caption(
                "Image unavailable"
            )

    else:

        st.html(
            f"""
            <div style="
                width:{width}px;
                height:{width}px;
                border-radius:15px;

                background:#F3F5F4;

                border:
                    1px solid #D8DFDB;

                display:flex;
                align-items:center;
                justify-content:center;

                color:#6B746F;
                font-size:13px;
                text-align:center;

                margin-bottom:8px;
            ">
                No Image
            </div>
            """
        )


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_user_display_name(user):

    username = getattr(
        user,
        "username",
        None
    )

    if username:

        return (
            f"{user.user_id} - "
            f"{username}"
        )

    name = getattr(
        user,
        "name",
        None
    )

    if name:

        return (
            f"{user.user_id} - "
            f"{name}"
        )

    return (
        f"User {user.user_id}"
    )


def get_table_display_name(table):

    table_number = getattr(
        table,
        "table_number",
        None
    )

    if table_number:

        return (
            f"{table_number} "
            f"(Table ID: {table.table_id})"
        )

    return (
        f"Table {table.table_id}"
    )


def convert_order_items_to_dict(raw_items):

    order_items = []

    for item in raw_items:

        # -------------------------------------------------
        # Already dictionary
        # -------------------------------------------------

        if isinstance(item, dict):

            order_items.append(
                item
            )

            continue

        # -------------------------------------------------
        # Tuple / List
        # -------------------------------------------------

        if isinstance(
            item,
            (tuple, list)
        ):

            if len(item) >= 7:

                order_items.append(
                    {
                        "order_item_id": item[0],
                        "order_id": item[1],
                        "product_id": item[2],
                        "product_name": item[3],
                        "quantity": item[4],
                        "unit_price": item[5],
                        "subtotal": item[6]
                    }
                )

    return order_items


def convert_summary_items_to_dict(
    summary_items
):

    items = []

    for item in summary_items:

        # -------------------------------------------------
        # Already dictionary
        # -------------------------------------------------

        if isinstance(item, dict):

            items.append(
                item
            )

            continue

        # -------------------------------------------------
        # Tuple / List
        # -------------------------------------------------

        if isinstance(
            item,
            (tuple, list)
        ):

            if len(item) >= 5:

                items.append(
                    {
                        "product_id": item[0],
                        "product_name": item[1],
                        "quantity": item[2],
                        "unit_price": item[3],
                        "subtotal": item[4]
                    }
                )

    return items


# =========================================================
# POS PAGE
# =========================================================

def show_pos_page():

    sales_manager = SalesManager()


    # =====================================================
    # SESSION STATE
    # =====================================================

    if "active_order_id" not in st.session_state:

        st.session_state.active_order_id = None


    if "selected_customer_id" not in st.session_state:

        st.session_state.selected_customer_id = None


    if "selected_user_id" not in st.session_state:

        st.session_state.selected_user_id = None


    if "selected_table_id" not in st.session_state:

        st.session_state.selected_table_id = None


    if "checkout_ready" not in st.session_state:

        st.session_state.checkout_ready = False


    if "last_receipt" not in st.session_state:

        st.session_state.last_receipt = None


    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title(
        "🛒 Point of Sale"
    )


    st.caption(
        "Create customer orders and manage live orders."
    )


    # =====================================================
    # ACTIVE ORDER
    # =====================================================

    active_order_id = (
        st.session_state.active_order_id
    )


    if active_order_id is not None:

        active_order = (
            sales_manager.get_order_by_id(
                active_order_id
            )
        )


        # -------------------------------------------------
        # ORDER NOT FOUND
        # -------------------------------------------------

        if active_order is None:

            st.error(
                "The active order could not be found."
            )

            st.session_state.active_order_id = None

            st.session_state.checkout_ready = False

            st.rerun()


        # =================================================
        # ACTIVE ORDER INFORMATION
        # =================================================

        st.success(
            f"🟢 Active Order #{active_order.order_id}"
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Customer ID",
                active_order.customer_id
            )


        with col2:

            st.metric(
                "Table ID",
                (
                    active_order.table_id
                    if active_order.table_id is not None
                    else "-"
                )
            )


        with col3:

            st.metric(
                "Order Status",
                active_order.status
            )


        with col4:

            st.metric(
                "Payment",
                active_order.payment_status
            )


        st.divider()


        # =================================================
        # CUSTOMER INFORMATION
        # =================================================

        customers = (
            sales_manager.get_all_customers()
        )


        active_customer = next(
            (
                customer

                for customer in customers

                if (
                    customer.customer_id
                    == active_order.customer_id
                )
            ),
            None
        )


        if active_customer is not None:

            st.write(
                f"👤 **Customer:** "
                f"{active_customer.name} "
                f"({active_customer.phone})"
            )


        # =================================================
        # CURRENT ORDER ITEMS
        # =================================================

        raw_order_items = (
            sales_manager.get_order_items(
                active_order_id
            )
        )


        order_items = (
            convert_order_items_to_dict(
                raw_order_items
            )
        )


        # =================================================
        # AVAILABLE PRODUCTS
        # =================================================

        products = (
            sales_manager.get_all_products()
        )


        available_products = [

            product

            for product in products

            if product.availability

        ]


        # =================================================
        # ADD PRODUCTS
        # =================================================

        st.subheader(
            "📦 Add Products"
        )


        if not available_products:

            st.warning(
                "No available products found."
            )

        else:

            # -------------------------------------------------
            # SEARCH + CATEGORY
            # -------------------------------------------------

            search_col, category_col = st.columns(
                [2, 1]
            )


            with search_col:

                product_search = st.text_input(
                    "🔎 Search Product",
                    placeholder=(
                        "Search product name..."
                    ),
                    key="pos_product_search"
                )


            with category_col:

                product_categories = sorted(
                    set(
                        product.category
                        for product in available_products
                        if product.category
                    )
                )


                category_options = (
                    ["All"] + product_categories
                )


                selected_category = st.selectbox(
                    "Category",
                    category_options,
                    key="pos_product_category"
                )


            # -------------------------------------------------
            # FILTER PRODUCTS
            # -------------------------------------------------

            filtered_products = []


            for product in available_products:

                if product_search:

                    search_value = (
                        product_search
                        .strip()
                        .lower()
                    )


                    if (
                        search_value
                        not in str(
                            product.product_name
                        ).lower()
                    ):

                        continue


                if (
                    selected_category != "All"
                    and product.category
                    != selected_category
                ):

                    continue


                filtered_products.append(
                    product
                )


            # -------------------------------------------------
            # PRODUCT COUNT
            # -------------------------------------------------

            st.caption(
                f"{len(filtered_products)} "
                f"available product(s)"
            )


            if not filtered_products:

                st.info(
                    "No products match your search."
                )


            else:

                # -------------------------------------------------
                # PRODUCT CARDS
                # -------------------------------------------------

                products_per_row = 3


                for row_start in range(
                    0,
                    len(filtered_products),
                    products_per_row
                ):

                    row_products = (
                        filtered_products[
                            row_start:
                            row_start + products_per_row
                        ]
                    )


                    columns = st.columns(
                        products_per_row
                    )


                    for index, product in enumerate(
                        row_products
                    ):

                        with columns[index]:

                            # ---------------------------------
                            # PRODUCT CARD
                            # ---------------------------------

                            st.html(
                                """
                                <div style="
                                    border:
                                        1px solid #D9E2DD;

                                    border-radius:16px;

                                    padding:14px;

                                    margin-bottom:10px;

                                    background:#FFFFFF;

                                    box-shadow:
                                        0 3px 10px
                                        rgba(
                                            25,
                                            85,
                                            60,
                                            0.08
                                        );
                                ">
                                """
                            )


                            # ---------------------------------
                            # IMAGE
                            # ---------------------------------

                            display_product_image(
                                product.image_url,
                                width=180
                            )


                            # ---------------------------------
                            # PRODUCT NAME
                            # ---------------------------------

                            st.markdown(
                                f"### "
                                f"{product.product_name}"
                            )


                            # ---------------------------------
                            # CATEGORY
                            # ---------------------------------

                            st.caption(
                                product.category
                            )


                            # ---------------------------------
                            # PRICE
                            # ---------------------------------

                            st.markdown(
                                f"**Rs. "
                                f"{float(product.price):,.2f}**"
                            )


                            # ---------------------------------
                            # QUANTITY
                            # ---------------------------------

                            product_quantity = (
                                st.number_input(
                                    "Quantity",
                                    min_value=1,
                                    max_value=50,
                                    value=1,
                                    step=1,
                                    key=(
                                        f"pos_qty_"
                                        f"{product.product_id}"
                                    )
                                )
                            )


                            # ---------------------------------
                            # ADD BUTTON
                            # ---------------------------------

                            if st.button(
                                "➕ Add to Order",
                                key=(
                                    f"pos_add_"
                                    f"{product.product_id}"
                                ),
                                width="stretch"
                            ):

                                success, result = (
                                    sales_manager.add_item_to_order(
                                        active_order_id,
                                        product.product_id,
                                        product_quantity
                                    )
                                )


                                if success:

                                    st.success(
                                        f"✅ "
                                        f"{product.product_name} "
                                        f"x {product_quantity} added."
                                    )

                                    st.rerun()


                                else:

                                    st.error(
                                        f"❌ Could not add item: "
                                        f"{result}"
                                    )


                            st.html(
                                """
                                </div>
                                """
                            )


        # =================================================
        # CURRENT ORDER
        # =================================================

        st.divider()


        st.subheader(
            "🛒 Current Order"
        )


        # =================================================
        # EMPTY ORDER
        # =================================================

        if not order_items:

            st.info(
                "No items added to this order yet."
            )


        else:

            # -------------------------------------------------
            # PRODUCT LOOKUP
            # -------------------------------------------------

            product_lookup = {
                product.product_id: product
                for product in products
            }


            # -------------------------------------------------
            # ORDER SUMMARY
            # -------------------------------------------------

            total_item_quantity = sum(
                int(item["quantity"])
                for item in order_items
            )


            st.caption(
                f"{len(order_items)} unique item(s) • "
                f"{total_item_quantity} total quantity"
            )


            # =================================================
            # CART HEADER
            # =================================================

            header_col1, header_col2, header_col3, header_col4 = (
                st.columns(
                    [1.0, 3.5, 3.0, 1.2]
                )
            )


            with header_col1:

                st.caption(
                    "ITEM"
                )


            with header_col2:

                st.caption(
                    "PRODUCT"
                )


            with header_col3:

                st.caption(
                    "QUANTITY / SUBTOTAL"
                )


            with header_col4:

                st.caption(
                    "ACTION"
                )


            st.html(
                """
                <div style="
                    height:1px;
                    background:#DDE5E1;
                    margin:0 0 12px 0;
                ">
                </div>
                """
            )


            # =================================================
            # CART ITEMS
            # =================================================

            for item in order_items:

                item_product = product_lookup.get(
                    item["product_id"]
                )


                item_quantity = int(
                    item["quantity"]
                )


                item_subtotal = float(
                    item["subtotal"]
                )


                item_unit_price = float(
                    item["unit_price"]
                )


                # =================================================
                # CART ROW
                # =================================================

                with st.container(
                    border=True
                ):

                    item_col1, item_col2, item_col3, item_col4 = (
                        st.columns(
                            [1.0, 3.5, 3.0, 1.2],
                            vertical_alignment="center"
                        )
                    )


                    # =============================================
                    # IMAGE
                    # =============================================

                    with item_col1:

                        if item_product is not None:

                            display_product_image(
                                item_product.image_url,
                                width=76
                            )

                        else:

                            st.html(
                                """
                                <div style="
                                    width:76px;
                                    height:76px;

                                    border-radius:14px;

                                    background:#F1F5F3;

                                    border:
                                        1px solid #D8E1DC;

                                    display:flex;
                                    align-items:center;
                                    justify-content:center;

                                    color:#7A8580;

                                    font-size:11px;
                                    font-weight:600;
                                ">
                                    No Image
                                </div>
                                """
                            )


                    # =============================================
                    # PRODUCT DETAILS
                    # =============================================

                    with item_col2:

                        st.html(
                            f"""
                            <div style="
                                padding:4px 0;
                            ">

                                <div style="
                                    font-size:17px;
                                    font-weight:700;

                                    color:#202824;

                                    margin-bottom:5px;
                                ">
                                    {item["product_name"]}
                                </div>

                                <div style="
                                    font-size:13px;
                                    color:#7A8580;

                                    margin-bottom:4px;
                                ">
                                    Unit Price
                                </div>

                                <div style="
                                    font-size:15px;
                                    font-weight:600;

                                    color:#39433F;
                                ">
                                    Rs. {item_unit_price:,.2f}
                                </div>

                            </div>
                            """
                        )


                    # =============================================
                    # QUANTITY + SUBTOTAL
                    # =============================================

                    with item_col3:

                        qty_col1, qty_col2, qty_col3 = (
                            st.columns(
                                [0.8, 1.0, 0.8],
                                vertical_alignment="center"
                            )
                        )


                        # -----------------------------------------
                        # MINUS
                        # -----------------------------------------

                        with qty_col1:

                            minus_clicked = st.button(
                                "−",
                                key=(
                                    f"cart_minus_"
                                    f"{item['order_item_id']}"
                                ),
                                disabled=(
                                    item_quantity <= 1
                                    or active_order.status
                                    not in {
                                        "Open",
                                        "Preparing"
                                    }
                                ),
                                width="stretch"
                            )


                        # -----------------------------------------
                        # QUANTITY
                        # -----------------------------------------

                        with qty_col2:

                            st.html(
                                f"""
                                <div style="
                                    height:38px;

                                    min-width:38px;

                                    border-radius:10px;

                                    background:#EAF4EF;

                                    border:
                                        1px solid #C5DED1;

                                    display:flex;

                                    align-items:center;
                                    justify-content:center;

                                    font-size:16px;
                                    font-weight:700;

                                    color:#176B4D;
                                ">
                                    {item_quantity}
                                </div>
                                """
                            )


                        # -----------------------------------------
                        # PLUS
                        # -----------------------------------------

                        with qty_col3:

                            plus_clicked = st.button(
                                "+",
                                key=(
                                    f"cart_plus_"
                                    f"{item['order_item_id']}"
                                ),
                                disabled=(
                                    item_quantity >= 50
                                    or active_order.status
                                    not in {
                                        "Open",
                                        "Preparing"
                                    }
                                ),
                                width="stretch"
                            )


                        # -----------------------------------------
                        # DECREASE
                        # -----------------------------------------

                        if minus_clicked:

                            new_quantity = (
                                item_quantity - 1
                            )


                            success, result = (
                                sales_manager.update_order_item_quantity(
                                    item["order_item_id"],
                                    new_quantity
                                )
                            )


                            if success:

                                st.rerun()


                            else:

                                st.error(
                                    f"Could not update quantity: "
                                    f"{result}"
                                )


                        # -----------------------------------------
                        # INCREASE
                        # -----------------------------------------

                        if plus_clicked:

                            new_quantity = (
                                item_quantity + 1
                            )


                            success, result = (
                                sales_manager.update_order_item_quantity(
                                    item["order_item_id"],
                                    new_quantity
                                )
                            )


                            if success:

                                st.rerun()


                            else:

                                st.error(
                                    f"Could not update quantity: "
                                    f"{result}"
                                )


                        # -----------------------------------------
                        # SUBTOTAL
                        # -----------------------------------------

                        st.html(
                            f"""
                            <div style="
                                margin-top:10px;
                                text-align:right;
                            ">

                                <div style="
                                    font-size:12px;
                                    color:#7A8580;

                                    margin-bottom:3px;
                                ">
                                    Subtotal
                                </div>

                                <div style="
                                    font-size:17px;
                                    font-weight:800;

                                    color:#176B4D;
                                ">
                                    Rs. {item_subtotal:,.2f}
                                </div>

                            </div>
                            """
                        )


                    # =============================================
                    # REMOVE
                    # =============================================

                    with item_col4:

                        remove_clicked = st.button(
                            "🗑️ Remove",
                            key=(
                                f"cart_remove_"
                                f"{item['order_item_id']}"
                            ),
                            disabled=(
                                active_order.status
                                not in {
                                    "Open",
                                    "Preparing"
                                }
                            ),
                            width="stretch"
                        )


                        if remove_clicked:

                            success, result = (
                                sales_manager.remove_order_item(
                                    item["order_item_id"]
                                )
                            )


                            if success:

                                st.rerun()


                            else:

                                st.error(
                                    f"Could not remove item: "
                                    f"{result}"
                                )


                st.html(
                    """
                    <div style="
                        height:8px;
                    ">
                    </div>
                    """
                )


            # =================================================
            # GET LATEST TOTAL
            # =================================================

            latest_order = (
                sales_manager.get_order_by_id(
                    active_order_id
                )
            )


            if latest_order is not None:

                total_amount = float(
                    latest_order.total_amount
                )

            else:

                total_amount = 0.0


            # =================================================
            # ORDER TOTAL - GREEN CARD
            # =================================================

            st.divider()


            st.html(
                f"""
                <div style="
                    margin:16px 0 26px 0;

                    padding:24px 28px;

                    border-radius:18px;

                    background:
                        linear-gradient(
                            135deg,
                            #176B4D 0%,
                            #0F5138 100%
                        );

                    border:
                        1px solid #2A8B67;

                    color:#FFFFFF;

                    box-shadow:
                        0 7px 20px
                        rgba(
                            15,
                            81,
                            56,
                            0.28
                        );
                ">

                    <div style="
                        display:flex;

                        justify-content:
                            space-between;

                        align-items:center;
                    ">

                        <div>

                            <div style="
                                font-size:13px;

                                font-weight:700;

                                letter-spacing:1.4px;

                                color:#D8F0E4;

                                margin-bottom:7px;
                            ">
                                ORDER TOTAL
                            </div>

                            <div style="
                                font-size:34px;

                                font-weight:800;

                                color:#FFFFFF;

                                letter-spacing:-0.6px;
                            ">
                                Rs. {total_amount:,.2f}
                            </div>

                        </div>

                        <div style="
                            font-size:38px;
                            line-height:1;
                        ">
                            🧾
                        </div>

                    </div>

                </div>
                """
            )


            # =================================================
            # CHECKOUT
            # =================================================

            if not st.session_state.checkout_ready:

                st.html(
                    """
                    <div style="
                        margin:8px 0 12px 0;
                    ">

                        <div style="
                            font-size:23px;
                            font-weight:700;

                            margin-bottom:4px;
                        ">
                            🧾 Checkout
                        </div>

                        <div style="
                            font-size:14px;
                            color:#68736E;

                            margin-bottom:10px;
                        ">
                            Review the order before payment.
                        </div>

                    </div>
                    """
                )


                if st.button(
                    "✅ Checkout Order",
                    width="stretch"
                ):

                    success, result, saved_total = (
                        sales_manager.checkout_order(
                            active_order_id
                        )
                    )


                    if success:

                        st.session_state.checkout_ready = (
                            True
                        )


                        st.success(
                            f"✅ {result}"
                        )


                        st.info(
                            f"Amount to pay: "
                            f"Rs. "
                            f"{float(saved_total):,.2f}"
                        )


                    else:

                        st.error(
                            f"❌ Checkout failed: "
                            f"{result}"
                        )


            # =================================================
            # PAYMENT
            # =================================================

            if st.session_state.checkout_ready:

                st.html(
                    """
                    <div style="
                        margin-top:22px;
                        margin-bottom:14px;

                        padding:18px 20px;

                        border-radius:16px;

                        background:
                            linear-gradient(
                                135deg,
                                #176B4D 0%,
                                #0F5138 100%
                            );

                        border:
                            1px solid #2A8B67;

                        color:#FFFFFF;

                        box-shadow:
                            0 5px 16px
                            rgba(
                                15,
                                81,
                                56,
                                0.22
                            );
                    ">

                        <div style="
                            font-size:22px;
                            font-weight:700;

                            margin-bottom:5px;

                            color:#FFFFFF;
                        ">
                            💳 Payment
                        </div>

                        <div style="
                            font-size:14px;
                            color:#D8F0E4;
                        ">
                            Select a payment method
                            to complete the order.
                        </div>

                    </div>
                    """
                )


                payment_method = st.radio(
                    "Payment Method",
                    [
                        "Cash",
                        "Card",
                        "QR"
                    ],
                    horizontal=True,
                    key="payment_method"
                )


                if st.button(
                    "💰 Make Payment",
                    width="stretch"
                ):

                    success, result = (
                        sales_manager.make_payment(
                            active_order_id,
                            payment_method
                        )
                    )


                    if success:

                        # -------------------------------------
                        # GET FINAL SUMMARY
                        # -------------------------------------

                        summary = (
                            sales_manager.get_order_summary(
                                active_order_id
                            )
                        )


                        # -------------------------------------
                        # CREATE RECEIPT
                        # -------------------------------------

                        if summary is not None:

                            receipt_lines = []


                            receipt_lines.append(
                                "========================================"
                            )


                            receipt_lines.append(
                                "                MY CAFÉ"
                            )


                            receipt_lines.append(
                                "             SALES RECEIPT"
                            )


                            receipt_lines.append(
                                "========================================"
                            )


                            receipt_lines.append(
                                f"Order ID: "
                                f"{summary['order_id']}"
                            )


                            receipt_lines.append(
                                f"Customer: "
                                f"{summary['customer_name']}"
                            )


                            receipt_lines.append(
                                f"Table: "
                                f"{summary['table_number']}"
                            )


                            receipt_lines.append(
                                f"Date: "
                                f"{summary['order_date']}"
                            )


                            receipt_lines.append(
                                f"Time: "
                                f"{summary['order_time']}"
                            )


                            receipt_lines.append(
                                f"Payment: "
                                f"{summary['payment_method']}"
                            )


                            receipt_lines.append(
                                "----------------------------------------"
                            )


                            summary_items = (
                                convert_summary_items_to_dict(
                                    summary["items"]
                                )
                            )


                            for item in summary_items:

                                receipt_lines.append(
                                    f"{item['product_name']}"
                                )


                                receipt_lines.append(
                                    f"  "
                                    f"{item['quantity']} x "
                                    f"Rs. "
                                    f"{float(item['unit_price']):,.2f}"
                                    f" = "
                                    f"Rs. "
                                    f"{float(item['subtotal']):,.2f}"
                                )


                            receipt_lines.append(
                                "----------------------------------------"
                            )


                            receipt_lines.append(
                                f"TOTAL: "
                                f"Rs. "
                                f"{float(summary['total_amount']):,.2f}"
                            )


                            receipt_lines.append(
                                "========================================"
                            )


                            receipt_lines.append(
                                "              Thank You!"
                            )


                            receipt_lines.append(
                                "========================================"
                            )


                            receipt_text = "\n".join(
                                receipt_lines
                            )


                            st.session_state.last_receipt = (
                                receipt_text
                            )


                        # -------------------------------------
                        # CLEAR ACTIVE ORDER
                        # -------------------------------------

                        completed_order_id = (
                            active_order_id
                        )


                        st.session_state.active_order_id = (
                            None
                        )


                        st.session_state.selected_customer_id = (
                            None
                        )


                        st.session_state.selected_user_id = (
                            None
                        )


                        st.session_state.selected_table_id = (
                            None
                        )


                        st.session_state.checkout_ready = (
                            False
                        )


                        st.success(
                            f"✅ Payment completed successfully. "
                            f"Order #{completed_order_id} "
                            f"is now Completed."
                        )


                        st.rerun()


                    else:

                        st.error(
                            f"❌ Payment failed: {result}"
                        )


        # =================================================
        # START ANOTHER ORDER
        # =================================================

        st.divider()


        if st.button(
            "➕ Start Another Order",
            width="stretch"
        ):

            st.session_state.active_order_id = None

            st.session_state.selected_customer_id = None

            st.session_state.selected_user_id = None

            st.session_state.selected_table_id = None

            st.session_state.checkout_ready = False

            st.rerun()


        # =================================================
        # LATEST RECEIPT
        # =================================================

        if (
            st.session_state.last_receipt
            is not None
        ):

            st.divider()


            st.subheader(
                "🧾 Latest Receipt"
            )


            st.code(
                st.session_state.last_receipt,
                language=None
            )


            st.download_button(
                label="📥 Download Receipt",
                data=st.session_state.last_receipt,
                file_name="cafe_receipt.txt",
                mime="text/plain",
                width="stretch"
            )


        return


    # =====================================================
    # NEW ORDER SECTION
    # =====================================================

    st.subheader(
        "👤 Customer"
    )


    customer_type = st.radio(
        "Customer Type",
        [
            "Existing Customer",
            "New Customer"
        ],
        horizontal=True
    )


    customer_id = None


    # =====================================================
    # EXISTING CUSTOMER
    # =====================================================

    if customer_type == "Existing Customer":

        customers = (
            sales_manager.get_all_customers()
        )


        if not customers:

            st.info(
                "No registered customers found. "
                "Select 'New Customer' to register one."
            )


            st.session_state.selected_customer_id = (
                None
            )


        else:

            search_text = st.text_input(
                "🔎 Search by name or phone number",
                placeholder="Enter customer name or phone"
            )


            search_text = (
                search_text
                .strip()
                .lower()
            )


            # -------------------------------------------------
            # FILTER CUSTOMERS
            # -------------------------------------------------

            if search_text:

                filtered_customers = [

                    customer

                    for customer in customers

                    if (
                        search_text
                        in str(
                            customer.name
                        ).lower()
                    )
                    or
                    (
                        search_text
                        in str(
                            customer.phone
                        ).lower()
                    )

                ]

            else:

                filtered_customers = customers


            # -------------------------------------------------
            # NO MATCH
            # -------------------------------------------------

            if not filtered_customers:

                st.warning(
                    "No matching customer found."
                )


            else:

                customer_options = {}


                for customer in filtered_customers:

                    label = (
                        f"{customer.customer_id} - "
                        f"{customer.name} - "
                        f"{customer.phone}"
                    )


                    customer_options[label] = (
                        customer.customer_id
                    )


                option_labels = list(
                    customer_options.keys()
                )


                # -------------------------------------------------
                # FIND SAVED CUSTOMER
                # -------------------------------------------------

                selected_index = 0


                saved_customer_id = (
                    st.session_state.selected_customer_id
                )


                if saved_customer_id is not None:

                    for index, customer in enumerate(
                        filtered_customers
                    ):

                        if (
                            customer.customer_id
                            == saved_customer_id
                        ):

                            selected_index = index

                            break


                # -------------------------------------------------
                # SELECT CUSTOMER
                # -------------------------------------------------

                selected_customer_label = st.selectbox(
                    "Select Customer",
                    options=option_labels,
                    index=selected_index
                )


                customer_id = (
                    customer_options[
                        selected_customer_label
                    ]
                )


                selected_customer = next(

                    customer

                    for customer in filtered_customers

                    if (
                        customer.customer_id
                        == customer_id
                    )

                )


                st.session_state.selected_customer_id = (
                    customer_id
                )


                st.success(
                    f"✅ Customer selected: "
                    f"{selected_customer.name} "
                    f"({selected_customer.phone})"
                )


    # =====================================================
    # NEW CUSTOMER
    # =====================================================

    else:

        st.markdown(
            "### ➕ Register New Customer"
        )


        new_customer_name = st.text_input(
            "Customer Name",
            placeholder="Enter customer name"
        )


        new_customer_phone = st.text_input(
            "Phone Number",
            placeholder="Enter customer phone number"
        )


        if st.button(
            "➕ Register Customer",
            width="stretch"
        ):

            name = (
                new_customer_name
                .strip()
            )


            phone = (
                new_customer_phone
                .strip()
            )


            # -------------------------------------------------
            # VALIDATION
            # -------------------------------------------------

            if not name:

                st.error(
                    "Please enter the customer's name."
                )


            elif not phone:

                st.error(
                    "Please enter the customer's phone number."
                )


            elif not phone.isdigit():

                st.error(
                    "Phone number should contain digits only."
                )


            elif len(phone) < 9 or len(phone) > 15:

                st.error(
                    "Please enter a valid phone number."
                )


            else:

                customers = (
                    sales_manager.get_all_customers()
                )


                existing_customer = next(

                    (
                        customer

                        for customer in customers

                        if (
                            str(
                                customer.phone
                            ).strip()
                            == phone
                        )

                    ),

                    None

                )


                # -------------------------------------------------
                # DUPLICATE CUSTOMER
                # -------------------------------------------------

                if existing_customer is not None:

                    st.warning(
                        f"This phone number is already "
                        f"registered under "
                        f"{existing_customer.name}."
                    )


                    st.info(
                        "Select 'Existing Customer' "
                        "to continue."
                    )


                else:

                    # -------------------------------------------------
                    # ADD CUSTOMER
                    # -------------------------------------------------

                    try:

                        success, result = (
                            sales_manager.add_customer(
                                name,
                                phone
                            )
                        )


                        if success:

                            st.session_state.selected_customer_id = (
                                result
                            )


                            st.success(
                                f"✅ Customer '{name}' "
                                f"registered successfully."
                            )


                            st.rerun()


                        else:

                            st.error(
                                f"❌ Customer registration failed: "
                                f"{result}"
                            )


                    except Exception as error:

                        st.error(
                            f"❌ Customer registration failed: "
                            f"{error}"
                        )


    # =====================================================
    # CUSTOMER VALIDATION
    # =====================================================

    if customer_id is None:

        customer_id = (
            st.session_state.selected_customer_id
        )


    if customer_id is None:

        st.info(
            "Please select an existing customer or "
            "register a new customer."
        )


        # ---------------------------------------------
        # SHOW LAST RECEIPT
        # ---------------------------------------------

        if (
            st.session_state.last_receipt
            is not None
        ):

            st.divider()


            st.subheader(
                "🧾 Latest Receipt"
            )


            st.code(
                st.session_state.last_receipt,
                language=None
            )


            st.download_button(
                label="📥 Download Receipt",
                data=st.session_state.last_receipt,
                file_name="cafe_receipt.txt",
                mime="text/plain",
                width="stretch"
            )


        return


    # =====================================================
    # STAFF / WAITER
    # =====================================================

    st.subheader(
        "👨‍🍳 Staff / Waiter"
    )


    users = (
        sales_manager.get_all_users()
    )


    if not users:

        st.error(
            "No users found. "
            "Please add a staff user before creating an order."
        )

        return


    user_options = {}


    for user in users:

        label = (
            get_user_display_name(
                user
            )
        )


        user_options[label] = (
            user.user_id
        )


    user_labels = list(
        user_options.keys()
    )


    selected_user_index = 0


    saved_user_id = (
        st.session_state.selected_user_id
    )


    if saved_user_id is not None:

        for index, user in enumerate(
            users
        ):

            if user.user_id == saved_user_id:

                selected_user_index = index

                break


    selected_user_label = st.selectbox(
        "Select Staff / Waiter",
        options=user_labels,
        index=selected_user_index
    )


    user_id = user_options[
        selected_user_label
    ]


    st.session_state.selected_user_id = (
        user_id
    )


    # =====================================================
    # TABLE SELECTION
    # =====================================================

    st.subheader(
        "🪑 Table"
    )


    available_tables = (
        sales_manager.get_available_tables()
    )


    if not available_tables:

        st.warning(
            "No available tables at the moment."
        )

        return


    table_options = {}


    for table in available_tables:

        label = (
            get_table_display_name(
                table
            )
        )


        table_options[label] = (
            table.table_id
        )


    table_labels = list(
        table_options.keys()
    )


    selected_table_index = 0


    saved_table_id = (
        st.session_state.selected_table_id
    )


    if saved_table_id is not None:

        for index, table in enumerate(
            available_tables
        ):

            if (
                table.table_id
                == saved_table_id
            ):

                selected_table_index = index

                break


    selected_table_label = st.selectbox(
        "Select Available Table",
        options=table_labels,
        index=selected_table_index
    )


    table_id = table_options[
        selected_table_label
    ]


    st.session_state.selected_table_id = (
        table_id
    )


    # =====================================================
    # ORDER CREATION
    # =====================================================

    st.divider()


    if st.button(
        "📝 Create Open Order",
        width="stretch"
    ):

        success, result = (
            sales_manager.create_open_order(
                customer_id,
                user_id,
                table_id
            )
        )


        if success:

            st.session_state.active_order_id = (
                result
            )


            st.session_state.checkout_ready = (
                False
            )


            st.success(
                f"✅ Open Order #{result} "
                f"created successfully."
            )


            st.rerun()


        else:

            st.error(
                f"❌ Could not create order: "
                f"{result}"
            )


    # =====================================================
    # LATEST RECEIPT
    # =====================================================

    if (
        st.session_state.last_receipt
        is not None
    ):

        st.divider()


        st.subheader(
            "🧾 Latest Receipt"
        )


        st.code(
            st.session_state.last_receipt,
            language=None
        )


        st.download_button(
            label="📥 Download Receipt",
            data=st.session_state.last_receipt,
            file_name="cafe_receipt.txt",
            mime="text/plain",
            width="stretch"
        )