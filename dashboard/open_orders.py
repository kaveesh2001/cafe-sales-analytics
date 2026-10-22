import streamlit as st

from services.sales_manager import SalesManager


# =========================================================
# FORMAT HELPERS
# =========================================================

def format_date(date_value):

    if date_value is None:
        return "-"

    try:

        return date_value.strftime(
            "%Y-%m-%d"
        )

    except Exception:

        return str(
            date_value
        )


def format_time(time_value):

    if time_value is None:
        return "-"

    try:

        return time_value.strftime(
            "%I:%M %p"
        )

    except Exception:

        return str(
            time_value
        )


# =========================================================
# STATUS STYLE
# =========================================================

def get_status_style(status):

    styles = {

        "Open": {
            "background": "#EAF4EF",
            "border": "#BFDCCA",
            "color": "#176B4D"
        },

        "Preparing": {
            "background": "#FFF5DD",
            "border": "#E8D39A",
            "color": "#8A6200"
        },

        "Ready": {
            "background": "#E8F2FB",
            "border": "#BDD6EC",
            "color": "#23618C"
        },

        "Served": {
            "background": "#EEEAF8",
            "border": "#D1C5EA",
            "color": "#624E8A"
        },

        "Completed": {
            "background": "#EAF4EF",
            "border": "#BFDCCA",
            "color": "#176B4D"
        },

        "Cancelled": {
            "background": "#FDECEC",
            "border": "#F0C3C3",
            "color": "#A33A3A"
        }

    }

    return styles.get(
        status,
        {
            "background": "#F3F5F4",
            "border": "#D8DFDB",
            "color": "#5E6863"
        }
    )


def show_status_badge(status):

    style = get_status_style(
        status
    )

    st.html(
        f"""
        <div style="
            display:inline-block;

            padding:7px 13px;

            border-radius:999px;

            background:{style["background"]};

            border:1px solid {style["border"]};

            color:{style["color"]};

            font-size:12px;

            font-weight:700;

            white-space:nowrap;
        ">
            {status}
        </div>
        """
    )


# =========================================================
# USER HELPER
# =========================================================

def get_user_name(
    users,
    user_id
):

    for user in users:

        if user.user_id == user_id:

            username = getattr(
                user,
                "username",
                None
            )

            if username:

                return username

            name = getattr(
                user,
                "name",
                None
            )

            if name:

                return name

            return (
                f"User {user_id}"
            )

    return (
        f"User {user_id}"
    )


# =========================================================
# TABLE HELPER
# =========================================================

def get_table_name(
    tables,
    table_id
):

    for table in tables:

        if table.table_id == table_id:

            table_number = getattr(
                table,
                "table_number",
                None
            )

            if table_number:

                return str(
                    table_number
                )

            return (
                f"Table {table_id}"
            )

    return (
        f"Table {table_id}"
    )


# =========================================================
# OPEN ORDERS PAGE
# =========================================================

def show_open_orders_page():

    sales_manager = SalesManager()


    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title(
        "📋 Open Orders"
    )

    st.caption(
        "Monitor active orders and manage their progress."
    )


    # =====================================================
    # REFRESH
    # =====================================================

    refresh_col1, refresh_col2 = st.columns(
        [5, 1]
    )


    with refresh_col2:

        if st.button(
            "🔄 Refresh",
            width="stretch"
        ):

            st.rerun()


    # =====================================================
    # LOAD DATA
    # =====================================================

    open_orders = (
        sales_manager.get_open_orders()
    )

    customers = (
        sales_manager.get_all_customers()
    )

    users = (
        sales_manager.get_all_users()
    )

    tables = (
        sales_manager.get_all_tables()
    )

    products = (
        sales_manager.get_all_products()
    )


    # =====================================================
    # EMPTY STATE
    # =====================================================

    if not open_orders:

        st.divider()

        st.success(
            "🎉 No active orders at the moment."
        )

        st.caption(
            "New orders created from the POS will appear here."
        )

        return


    # =====================================================
    # SUMMARY
    # =====================================================

    total_orders = len(
        open_orders
    )


    open_count = sum(
        1
        for order in open_orders
        if order[8] == "Open"
    )


    preparing_count = sum(
        1
        for order in open_orders
        if order[8] == "Preparing"
    )


    ready_count = sum(
        1
        for order in open_orders
        if order[8] == "Ready"
    )


    served_count = sum(
        1
        for order in open_orders
        if order[8] == "Served"
    )


    total_active_value = sum(
        float(
            order[9] or 0
        )
        for order in open_orders
    )


    # =====================================================
    # SUMMARY METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Active Orders",
            total_orders
        )


    with col2:

        st.metric(
            "🟢 Open",
            open_count
        )


    with col3:

        st.metric(
            "🟡 Preparing",
            preparing_count
        )


    with col4:

        st.metric(
            "🔵 Ready",
            ready_count
        )


    col5, col6 = st.columns(2)


    with col5:

        st.metric(
            "🟣 Served",
            served_count
        )


    with col6:

        st.metric(
            "Active Order Value",
            f"Rs. {total_active_value:,.2f}"
        )


    st.divider()


    # =====================================================
    # SEARCH + FILTER
    # =====================================================

    search_col, filter_col = st.columns(
        [2, 1]
    )


    with search_col:

        search_text = st.text_input(
            "🔎 Search Orders",
            placeholder=(
                "Order ID, customer, table or waiter..."
            ),
            key="open_orders_search"
        )


    with filter_col:

        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "Open",
                "Preparing",
                "Ready",
                "Served"
            ],
            key="open_orders_status"
        )


    # =====================================================
    # FILTER ORDERS
    # =====================================================

    filtered_orders = []


    search_value = (
        search_text
        .strip()
        .lower()
    )


    for order in open_orders:

        order_id = order[0]

        customer_id = order[1]

        customer_name = order[2]

        user_id = order[3]

        table_id = order[4]

        table_number = order[5]

        status = order[8]

        payment_status = order[10]

        payment_method = order[11]


        waiter_name = get_user_name(
            users,
            user_id
        )


        if search_value:

            searchable_text = (
                f"{order_id} "
                f"{customer_id} "
                f"{customer_name} "
                f"{user_id} "
                f"{waiter_name} "
                f"{table_id} "
                f"{table_number} "
                f"{status} "
                f"{payment_status} "
                f"{payment_method}"
            ).lower()


            if search_value not in searchable_text:

                continue


        if (
            status_filter != "All"
            and status != status_filter
        ):

            continue


        filtered_orders.append(
            order
        )


    # =====================================================
    # RESULT COUNT
    # =====================================================

    st.caption(
        f"Showing {len(filtered_orders)} "
        f"of {len(open_orders)} active order(s)."
    )


    if not filtered_orders:

        st.info(
            "No active orders match your search or filter."
        )

        return


    st.divider()


    # =====================================================
    # ORDER CARDS
    # =====================================================

    for order in filtered_orders:

        order_id = order[0]

        customer_id = order[1]

        customer_name = order[2]

        user_id = order[3]

        table_id = order[4]

        table_number = order[5]

        order_date = order[6]

        order_time = order[7]

        status = order[8]

        total_amount = float(
            order[9] or 0
        )

        payment_status = order[10]

        payment_method = order[11]


        waiter_name = get_user_name(
            users,
            user_id
        )


        if table_number is not None:

            display_table = str(
                table_number
            )

        else:

            display_table = get_table_name(
                tables,
                table_id
            )


        customer_phone = "-"


        for customer in customers:

            if customer.customer_id == customer_id:

                customer_phone = str(
                    customer.phone
                )

                break


        # =================================================
        # ORDER CARD
        # =================================================

        with st.container(
            border=True
        ):

            # =============================================
            # HEADER
            # =============================================

            header_col1, header_col2 = st.columns(
                [4, 1]
            )


            with header_col1:

                st.html(
                    f"""
                    <div>

                        <div style="
                            font-size:22px;
                            font-weight:800;

                            color:#202824;

                            margin-bottom:4px;
                        ">
                            Order #{order_id}
                        </div>

                        <div style="
                            font-size:13px;

                            color:#7A8580;
                        ">
                            {format_date(order_date)}
                            &nbsp;•&nbsp;
                            {format_time(order_time)}
                        </div>

                    </div>
                    """
                )


            with header_col2:

                show_status_badge(
                    status
                )


            st.divider()


            # =============================================
            # ORDER INFORMATION
            # =============================================

            info1, info2, info3, info4 = st.columns(
                4
            )


            with info1:

                st.html(
                    f"""
                    <div>

                        <div style="
                            font-size:11px;
                            text-transform:uppercase;
                            letter-spacing:0.8px;

                            color:#8A948F;

                            margin-bottom:5px;
                        ">
                            Customer
                        </div>

                        <div style="
                            font-size:15px;
                            font-weight:700;

                            color:#27312D;
                        ">
                            👤 {customer_name}
                        </div>

                        <div style="
                            font-size:12px;
                            color:#7A8580;

                            margin-top:3px;
                        ">
                            {customer_phone}
                        </div>

                    </div>
                    """
                )


            with info2:

                st.html(
                    f"""
                    <div>

                        <div style="
                            font-size:11px;
                            text-transform:uppercase;
                            letter-spacing:0.8px;

                            color:#8A948F;

                            margin-bottom:5px;
                        ">
                            Table
                        </div>

                        <div style="
                            font-size:15px;
                            font-weight:700;

                            color:#27312D;
                        ">
                            🪑 {display_table}
                        </div>

                        <div style="
                            font-size:12px;
                            color:#7A8580;

                            margin-top:3px;
                        ">
                            Table ID: {table_id}
                        </div>

                    </div>
                    """
                )


            with info3:

                st.html(
                    f"""
                    <div>

                        <div style="
                            font-size:11px;
                            text-transform:uppercase;
                            letter-spacing:0.8px;

                            color:#8A948F;

                            margin-bottom:5px;
                        ">
                            Staff / Waiter
                        </div>

                        <div style="
                            font-size:15px;
                            font-weight:700;

                            color:#27312D;
                        ">
                            👨‍🍳 {waiter_name}
                        </div>

                        <div style="
                            font-size:12px;
                            color:#7A8580;

                            margin-top:3px;
                        ">
                            User ID: {user_id}
                        </div>

                    </div>
                    """
                )


            with info4:

                st.html(
                    f"""
                    <div>

                        <div style="
                            font-size:11px;
                            text-transform:uppercase;
                            letter-spacing:0.8px;

                            color:#8A948F;

                            margin-bottom:5px;
                        ">
                            Order Total
                        </div>

                        <div style="
                            font-size:19px;
                            font-weight:800;

                            color:#176B4D;
                        ">
                            Rs. {total_amount:,.2f}
                        </div>

                        <div style="
                            font-size:12px;
                            color:#7A8580;

                            margin-top:3px;
                        ">
                            {payment_status}
                        </div>

                    </div>
                    """
                )


            st.divider()


            # =============================================
            # MANAGE ORDER
            # =============================================

            with st.expander(
                f"⚙️ Manage Order #{order_id}"
            ):

                st.markdown(
                    "### 🧾 Order Items"
                )


                # =========================================
                # GET ORDER ITEMS
                # =========================================

                order_items = (
                    sales_manager.get_order_items(
                        order_id
                    )
                )


                if not order_items:

                    st.info(
                        "No items found for this order."
                    )

                else:

                    for item in order_items:

                        order_item_id = item[0]

                        product_id = item[2]

                        product_name = item[3]

                        quantity = int(
                            item[4]
                        )

                        unit_price = float(
                            item[5]
                        )

                        subtotal = float(
                            item[6]
                        )


                        item_col1, item_col2, item_col3, item_col4 = (
                            st.columns(
                                [1.1, 3.5, 1.5, 2]
                            )
                        )


                        # ---------------------------------
                        # PRODUCT IMAGE
                        # ---------------------------------

                        with item_col1:

                            item_product = next(
                                (
                                    product
                                    for product in products
                                    if product.product_id
                                    == product_id
                                ),
                                None
                            )


                            image_source = None


                            if item_product is not None:

                                image_source = getattr(
                                    item_product,
                                    "image_url",
                                    None
                                )


                            if image_source:

                                if (
                                    str(
                                        image_source
                                    )
                                    .startswith(
                                        "http://"
                                    )
                                    or
                                    str(
                                        image_source
                                    )
                                    .startswith(
                                        "https://"
                                    )
                                ):

                                    st.image(
                                        image_source,
                                        width=65
                                    )

                                else:

                                    st.caption(
                                        "Image"
                                    )

                            else:

                                st.html(
                                    """
                                    <div style="
                                        width:65px;
                                        height:65px;

                                        border-radius:11px;

                                        background:#F1F5F3;

                                        border:
                                            1px solid #D8E1DC;

                                        display:flex;
                                        align-items:center;
                                        justify-content:center;

                                        color:#7A8580;

                                        font-size:10px;
                                    ">
                                        No Image
                                    </div>
                                    """
                                )


                        # ---------------------------------
                        # PRODUCT
                        # ---------------------------------

                        with item_col2:

                            st.html(
                                f"""
                                <div style="
                                    padding-top:5px;
                                ">

                                    <div style="
                                        font-size:15px;
                                        font-weight:700;

                                        color:#27312D;

                                        margin-bottom:3px;
                                    ">
                                        {product_name}
                                    </div>

                                    <div style="
                                        font-size:12px;
                                        color:#7A8580;
                                    ">
                                        Rs. {unit_price:,.2f}
                                        each
                                    </div>

                                </div>
                                """
                            )


                        # ---------------------------------
                        # QUANTITY
                        # ---------------------------------

                        with item_col3:

                            st.html(
                                f"""
                                <div style="
                                    padding-top:15px;

                                    font-size:15px;

                                    font-weight:700;

                                    color:#27312D;
                                ">
                                    × {quantity}
                                </div>
                                """
                            )


                        # ---------------------------------
                        # SUBTOTAL
                        # ---------------------------------

                        with item_col4:

                            st.html(
                                f"""
                                <div style="
                                    padding-top:15px;

                                    text-align:right;

                                    font-size:16px;

                                    font-weight:800;

                                    color:#176B4D;
                                ">
                                    Rs. {subtotal:,.2f}
                                </div>
                                """
                            )


                        st.html(
                            """
                            <div style="
                                height:8px;
                            ">
                            </div>
                            """
                        )


                st.divider()


                # =============================================
                # ORDER STATUS
                # =============================================

                st.markdown(
                    "### 🔄 Order Status"
                )


                show_status_badge(
                    status
                )


                st.markdown(
                    "<div style='height:10px;'></div>",
                    unsafe_allow_html=True
                )


                # =============================================
                # STATUS PROGRESS
                # =============================================

                status_flow = [
                    "Open",
                    "Preparing",
                    "Ready",
                    "Served"
                ]


                current_index = (
                    status_flow.index(status)
                    if status in status_flow
                    else 0
                )


                flow_html = []


                for index, flow_status in enumerate(
                    status_flow
                ):

                    if index <= current_index:

                        background = "#176B4D"

                        color = "#FFFFFF"

                        border = "#176B4D"

                    else:

                        background = "#F3F5F4"

                        color = "#87918C"

                        border = "#D9E1DD"


                    flow_html.append(
                        f"""
                        <div style="
                            display:inline-block;

                            padding:7px 11px;

                            border-radius:999px;

                            background:{background};

                            color:{color};

                            border:
                                1px solid {border};

                            font-size:11px;

                            font-weight:700;
                        ">
                            {flow_status}
                        </div>
                        """
                    )


                    if index < len(status_flow) - 1:

                        flow_html.append(
                            """
                            <span style="
                                margin:0 4px;
                                color:#98A29D;
                                font-weight:700;
                            ">
                                →
                            </span>
                            """
                        )


                st.html(
                    f"""
                    <div style="
                        margin:10px 0 18px 0;
                        line-height:34px;
                    ">
                        {"".join(flow_html)}
                    </div>
                    """
                )


                # =============================================
                # OPEN
                # =============================================

                if status == "Open":

                    st.info(
                        "This order has been created and "
                        "is waiting to be prepared."
                    )


                    if st.button(
                        "🍳 Start Preparing",
                        key=f"prepare_{order_id}",
                        width="stretch"
                    ):

                        success, result = (
                            sales_manager.update_order_status(
                                order_id,
                                "Preparing"
                            )
                        )


                        if success:

                            st.success(
                                "✅ Order moved to Preparing."
                            )

                            st.rerun()

                        else:

                            st.error(
                                f"❌ Could not update status: "
                                f"{result}"
                            )


                # =============================================
                # PREPARING
                # =============================================

                elif status == "Preparing":

                    st.warning(
                        "👨‍🍳 This order is currently being prepared."
                    )


                    if st.button(
                        "✅ Mark as Ready",
                        key=f"ready_{order_id}",
                        width="stretch"
                    ):

                        success, result = (
                            sales_manager.update_order_status(
                                order_id,
                                "Ready"
                            )
                        )


                        if success:

                            st.success(
                                "✅ Order marked as Ready."
                            )

                            st.rerun()

                        else:

                            st.error(
                                f"❌ Could not update status: "
                                f"{result}"
                            )


                # =============================================
                # READY
                # =============================================

                elif status == "Ready":

                    st.success(
                        "✅ This order is ready to be served."
                    )


                    if st.button(
                        "🍽️ Mark as Served",
                        key=f"served_{order_id}",
                        width="stretch"
                    ):

                        success, result = (
                            sales_manager.update_order_status(
                                order_id,
                                "Served"
                            )
                        )


                        if success:

                            st.success(
                                "✅ Order marked as Served."
                            )

                            st.rerun()

                        else:

                            st.error(
                                f"❌ Could not update status: "
                                f"{result}"
                            )


                # =============================================
                # SERVED
                # =============================================

                elif status == "Served":

                    st.success(
                        "🍽️ Order has been served."
                    )


                    st.html(
                        """
                        <div style="
                            margin-top:10px;

                            padding:17px 18px;

                            border-radius:14px;

                            background:#EAF4EF;

                            border:
                                1px solid #BFDCCA;

                            color:#176B4D;
                        ">

                            <div style="
                                font-size:16px;

                                font-weight:750;

                                margin-bottom:5px;
                            ">
                                💳 Ready for Payment
                            </div>

                            <div style="
                                font-size:13px;

                                color:#60716A;

                                line-height:1.5;
                            ">
                                This order has been served.
                                Complete the payment from
                                the POS to close the order.
                            </div>

                        </div>
                        """
                    )


                    if st.button(
                        "🛒 Go to POS for Payment",
                        key=f"pos_payment_{order_id}",
                        width="stretch"
                    ):

                        # -------------------------------------
                        # SAVE ACTIVE ORDER
                        # -------------------------------------

                        st.session_state.active_order_id = (
                            order_id
                        )


                        st.session_state.checkout_ready = (
                            False
                        )


                        # -------------------------------------
                        # TELL APP TO OPEN POS
                        # -------------------------------------

                        st.session_state.go_to_pos = (
                            True
                        )


                        st.rerun()


                st.divider()


                # =============================================
                # CANCEL ORDER
                # =============================================

                st.markdown(
                    "### ❌ Cancel Order"
                )


                if status in {
                    "Open",
                    "Preparing",
                    "Ready",
                    "Served"
                }:

                    confirm_cancel = st.checkbox(
                        "I understand that this order will be cancelled.",
                        key=f"cancel_confirm_{order_id}"
                    )


                    if st.button(
                        "❌ Cancel Order",
                        key=f"cancel_{order_id}",
                        width="stretch"
                    ):

                        if not confirm_cancel:

                            st.error(
                                "Please confirm cancellation first."
                            )

                        else:

                            success, result = (
                                sales_manager.cancel_order(
                                    order_id
                                )
                            )


                            if success:

                                st.success(
                                    "✅ Order cancelled successfully."
                                )

                                st.rerun()

                            else:

                                st.error(
                                    f"❌ Could not cancel order: "
                                    f"{result}"
                                )


                # =============================================
                # FINAL INFORMATION
                # =============================================

                st.divider()


                st.caption(
                    "ℹ️ Completed orders are closed automatically "
                    "after successful payment."
                )


            st.markdown(
                "<div style='height:6px;'></div>",
                unsafe_allow_html=True
            )