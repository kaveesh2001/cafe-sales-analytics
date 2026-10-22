import streamlit as st

from services.sales_manager import SalesManager


# =========================================================
# FORMAT HELPERS
# =========================================================

def format_date(
    date_value
):

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


def format_time(
    time_value
):

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

def get_status_style(
    status
):

    styles = {

        "Completed": {
            "background": "#EAF4EF",
            "border": "#BFDCCA",
            "color": "#176B4D"
        },

        "Cancelled": {
            "background": "#FDECEC",
            "border": "#F0C3C3",
            "color": "#A33A3A"
        },

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


def show_status_badge(
    status
):

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
# PAYMENT DISPLAY
# =========================================================

def get_payment_display(
    payment_method,
    status
):

    if status == "Cancelled":

        return "Not Paid"


    if payment_method:

        return str(
            payment_method
        )


    return "Not Recorded"


# =========================================================
# ORDER HISTORY PAGE
# =========================================================

def show_order_history():

    sales_manager = SalesManager()


    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title(
        "🧾 Order History"
    )


    st.caption(
        "Review completed and cancelled customer orders."
    )


    # =====================================================
    # REFRESH
    # =====================================================

    refresh_col1, refresh_col2 = st.columns(
        [6, 1]
    )


    with refresh_col2:

        if st.button(
            "🔄 Refresh",
            width="stretch"
        ):

            st.rerun()


    # =====================================================
    # LOAD ORDER HISTORY
    # =====================================================

    order_history = (
        sales_manager.get_order_history()
    )


    # =====================================================
    # EMPTY HISTORY
    # =====================================================

    if not order_history:

        st.divider()

        st.info(
            "No order history available yet."
        )

        st.caption(
            "Completed and cancelled orders will appear here."
        )

        return


    # =====================================================
    # SUMMARY
    # =====================================================

    total_orders = len(
        order_history
    )


    completed_orders = [
        order

        for order in order_history

        if order[4] == "Completed"
    ]


    cancelled_orders = [
        order

        for order in order_history

        if order[4] == "Cancelled"
    ]


    completed_revenue = sum(
        float(
            order[5] or 0
        )
        for order in completed_orders
    )


    cancelled_value = sum(
        float(
            order[5] or 0
        )
        for order in cancelled_orders
    )


    # =====================================================
    # SUMMARY METRICS
    # =====================================================

    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )


    with metric1:

        st.metric(
            "Total Orders",
            total_orders
        )


    with metric2:

        st.metric(
            "Completed",
            len(
                completed_orders
            )
        )


    with metric3:

        st.metric(
            "Cancelled",
            len(
                cancelled_orders
            )
        )


    with metric4:

        st.metric(
            "Completed Revenue",
            f"Rs. {completed_revenue:,.2f}"
        )


    st.divider()


    # =====================================================
    # FILTERS
    # =====================================================

    filter_col1, filter_col2 = st.columns(
        [2, 1]
    )


    # =====================================================
    # SEARCH
    # =====================================================

    with filter_col1:

        search_text = st.text_input(
            "🔎 Search Orders",
            placeholder=(
                "Search by order ID or customer name..."
            ),
            key="order_history_search"
        )


    # =====================================================
    # STATUS FILTER
    # =====================================================

    with filter_col2:

        status_filter = st.selectbox(
            "📌 Status",
            [
                "All",
                "Completed",
                "Cancelled"
            ],
            key="order_history_status"
        )


    filter_col3, filter_col4 = st.columns(
        [1.5, 1.5]
    )


    # =====================================================
    # DATE RANGE
    # =====================================================

    dates = [

        order[1]

        for order in order_history

        if order[1] is not None

    ]


    if dates:

        min_date = min(
            dates
        )

        max_date = max(
            dates
        )


        with filter_col3:

            start_date = st.date_input(
                "📅 From",
                value=min_date,
                key="order_history_start"
            )


        with filter_col4:

            end_date = st.date_input(
                "📅 To",
                value=max_date,
                key="order_history_end"
            )

    else:

        start_date = None

        end_date = None


    # =====================================================
    # PAYMENT FILTER
    # =====================================================

    payment_options = [
        "All",
        "Cash",
        "Card",
        "QR",
        "Not Paid"
    ]


    payment_filter = st.selectbox(
        "💳 Payment Method",
        payment_options,
        key="order_history_payment"
    )


    # =====================================================
    # VALIDATE DATE RANGE
    # =====================================================

    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):

        st.error(
            "The start date cannot be after the end date."
        )

        return


    # =====================================================
    # APPLY FILTERS
    # =====================================================

    filtered_orders = []


    search_value = (
        search_text
        .strip()
        .lower()
    )


    for order in order_history:

        order_id = order[0]

        order_date = order[1]

        order_time = order[2]

        customer_name = order[3]

        status = order[4]

        total_amount = order[5]

        payment_method = order[6]


        # -------------------------------------------------
        # SEARCH
        # -------------------------------------------------

        if search_value:

            searchable_text = (
                f"{order_id} "
                f"{customer_name}"
            ).lower()


            if search_value not in searchable_text:

                continue


        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        if (
            status_filter != "All"
            and status != status_filter
        ):

            continue


        # -------------------------------------------------
        # DATE
        # -------------------------------------------------

        if (
            start_date is not None
            and order_date is not None
        ):

            if order_date < start_date:

                continue


        if (
            end_date is not None
            and order_date is not None
        ):

            if order_date > end_date:

                continue


        # -------------------------------------------------
        # PAYMENT
        # -------------------------------------------------

        displayed_payment = get_payment_display(
            payment_method,
            status
        )


        if payment_filter != "All":

            if displayed_payment != payment_filter:

                continue


        filtered_orders.append(
            order
        )


    # =====================================================
    # FILTER RESULT
    # =====================================================

    st.caption(
        f"Showing {len(filtered_orders)} "
        f"of {len(order_history)} order(s)."
    )


    # =====================================================
    # NO RESULTS
    # =====================================================

    if not filtered_orders:

        st.info(
            "No orders match the selected filters."
        )

        return


    st.divider()


    # =====================================================
    # ORDER RECORDS
    # =====================================================

    for order in filtered_orders:

        order_id = order[0]

        order_date = order[1]

        order_time = order[2]

        customer_name = order[3]

        status = order[4]

        total_amount = float(
            order[5] or 0
        )

        payment_method = order[6]


        payment_display = get_payment_display(
            payment_method,
            status
        )


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
                [4, 1.3]
            )


            with header_col1:

                st.html(
                    f"""
                    <div>

                        <div style="
                            font-size:21px;

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
            # BASIC INFORMATION
            # =============================================

            info1, info2, info3, info4 = st.columns(
                4
            )


            # ---------------------------------------------
            # CUSTOMER
            # ---------------------------------------------

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

                    </div>
                    """
                )


            # ---------------------------------------------
            # DATE
            # ---------------------------------------------

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
                            Date
                        </div>

                        <div style="
                            font-size:15px;

                            font-weight:700;

                            color:#27312D;
                        ">
                            {format_date(order_date)}
                        </div>

                    </div>
                    """
                )


            # ---------------------------------------------
            # PAYMENT
            # ---------------------------------------------

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
                            Payment
                        </div>

                        <div style="
                            font-size:15px;

                            font-weight:700;

                            color:#27312D;
                        ">
                            💳 {payment_display}
                        </div>

                    </div>
                    """
                )


            # ---------------------------------------------
            # TOTAL
            # ---------------------------------------------

            with info4:

                total_color = (
                    "#A33A3A"
                    if status == "Cancelled"
                    else "#176B4D"
                )


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

                            color:{total_color};
                        ">
                            Rs. {total_amount:,.2f}
                        </div>

                    </div>
                    """
                )


            # =================================================
            # VIEW DETAILS
            # =================================================

            st.divider()


            with st.expander(
                f"🔍 View Order #{order_id} Details"
            ):

                # =============================================
                # GET FULL SUMMARY
                # =============================================

                summary = (
                    sales_manager.get_order_summary(
                        order_id
                    )
                )


                if summary is None:

                    st.warning(
                        "Order details could not be loaded."
                    )

                else:

                    # =========================================
                    # ORDER INFORMATION
                    # =========================================

                    st.markdown(
                        "### 🧾 Order Information"
                    )


                    detail1, detail2, detail3 = (
                        st.columns(3)
                    )


                    with detail1:

                        st.write(
                            f"**Order ID:** "
                            f"{summary['order_id']}"
                        )


                        st.write(
                            f"**Customer:** "
                            f"{summary['customer_name']}"
                        )


                    with detail2:

                        st.write(
                            f"**Table:** "
                            f"{summary['table_number']}"
                        )


                        st.write(
                            f"**Staff / Waiter ID:** "
                            f"{summary['user_id']}"
                        )


                    with detail3:

                        st.write(
                            f"**Date:** "
                            f"{format_date(summary['order_date'])}"
                        )


                        st.write(
                            f"**Time:** "
                            f"{format_time(summary['order_time'])}"
                        )


                    st.divider()


                    # =========================================
                    # STATUS + PAYMENT
                    # =========================================

                    status_col, payment_col = (
                        st.columns(2)
                    )


                    with status_col:

                        st.markdown(
                            "**Order Status**"
                        )

                        show_status_badge(
                            summary["status"]
                        )


                    with payment_col:

                        st.markdown(
                            "**Payment Method**"
                        )

                        st.write(
                            get_payment_display(
                                summary["payment_method"],
                                summary["status"]
                            )
                        )


                    st.divider()


                    # =========================================
                    # ITEMS
                    # =========================================

                    st.markdown(
                        "### 🛒 Items"
                    )


                    summary_items = (
                        summary.get(
                            "items",
                            []
                        )
                    )


                    if not summary_items:

                        st.info(
                            "No items found for this order."
                        )

                    else:

                        item_total_quantity = 0


                        # -----------------------------------------
                        # HEADER
                        # -----------------------------------------

                        item_head1, item_head2, item_head3, item_head4 = (
                            st.columns(
                                [4, 1.5, 2, 2]
                            )
                        )


                        with item_head1:

                            st.caption(
                                "PRODUCT"
                            )


                        with item_head2:

                            st.caption(
                                "QUANTITY"
                            )


                        with item_head3:

                            st.caption(
                                "UNIT PRICE"
                            )


                        with item_head4:

                            st.caption(
                                "SUBTOTAL"
                            )


                        st.html(
                            """
                            <div style="
                                height:1px;

                                background:#DDE5E1;

                                margin:2px 0 10px 0;
                            ">
                            </div>
                            """
                        )


                        # -----------------------------------------
                        # ITEMS
                        # -----------------------------------------

                        for item in summary_items:

                            product_name = item[1]

                            quantity = int(
                                item[2]
                            )

                            unit_price = float(
                                item[3]
                            )

                            subtotal = float(
                                item[4]
                            )


                            item_total_quantity += (
                                quantity
                            )


                            item_col1, item_col2, item_col3, item_col4 = (
                                st.columns(
                                    [4, 1.5, 2, 2]
                                )
                            )


                            with item_col1:

                                st.write(
                                    f"**{product_name}**"
                                )


                            with item_col2:

                                st.write(
                                    f"× {quantity}"
                                )


                            with item_col3:

                                st.write(
                                    f"Rs. {unit_price:,.2f}"
                                )


                            with item_col4:

                                st.write(
                                    f"Rs. {subtotal:,.2f}"
                                )


                        st.divider()


                        # =========================================
                        # ORDER TOTAL
                        # =========================================

                        total_col1, total_col2 = (
                            st.columns(
                                [4, 2]
                            )
                        )


                        with total_col1:

                            st.caption(
                                f"{len(summary_items)} "
                                f"product line(s) • "
                                f"{item_total_quantity} "
                                f"total item(s)"
                            )


                        with total_col2:

                            st.html(
                                f"""
                                <div style="
                                    text-align:right;
                                ">

                                    <div style="
                                        font-size:12px;

                                        color:#7A8580;

                                        margin-bottom:4px;
                                    ">
                                        TOTAL
                                    </div>

                                    <div style="
                                        font-size:22px;

                                        font-weight:800;

                                        color:#176B4D;
                                    ">
                                        Rs.
                                        {float(
                                            summary["total_amount"]
                                            or 0
                                        ):,.2f}
                                    </div>

                                </div>
                                """
                            )


                    # =========================================
                    # RECEIPT-STYLE SUMMARY
                    # =========================================

                    st.divider()


                    st.markdown(
                        "### 🧾 Receipt Summary"
                    )


                    receipt_lines = []


                    receipt_lines.append(
                        "================================"
                    )


                    receipt_lines.append(
                        "              MY CAFÉ"
                    )


                    receipt_lines.append(
                        "           ORDER SUMMARY"
                    )


                    receipt_lines.append(
                        "================================"
                    )


                    receipt_lines.append(
                        f"Order ID : {summary['order_id']}"
                    )


                    receipt_lines.append(
                        f"Customer : {summary['customer_name']}"
                    )


                    receipt_lines.append(
                        f"Table    : {summary['table_number']}"
                    )


                    receipt_lines.append(
                        f"Date     : "
                        f"{format_date(summary['order_date'])}"
                    )


                    receipt_lines.append(
                        f"Time     : "
                        f"{format_time(summary['order_time'])}"
                    )


                    receipt_lines.append(
                        f"Status   : {summary['status']}"
                    )


                    receipt_lines.append(
                        f"Payment  : "
                        f"{get_payment_display(
                            summary['payment_method'],
                            summary['status']
                        )}"
                    )


                    receipt_lines.append(
                        "--------------------------------"
                    )


                    for item in summary_items:

                        product_name = item[1]

                        quantity = int(
                            item[2]
                        )

                        unit_price = float(
                            item[3]
                        )

                        subtotal = float(
                            item[4]
                        )


                        receipt_lines.append(
                            f"{product_name}"
                        )


                        receipt_lines.append(
                            f"  {quantity} x "
                            f"Rs. {unit_price:,.2f}"
                            f" = "
                            f"Rs. {subtotal:,.2f}"
                        )


                    receipt_lines.append(
                        "--------------------------------"
                    )


                    receipt_lines.append(
                        f"TOTAL: Rs. "
                        f"{float(
                            summary['total_amount'] or 0
                        ):,.2f}"
                    )


                    receipt_lines.append(
                        "================================"
                    )


                    if summary["status"] == "Completed":

                        receipt_lines.append(
                            "             PAID"
                        )

                    else:

                        receipt_lines.append(
                            "           CANCELLED"
                        )


                    receipt_lines.append(
                        "================================"
                    )


                    receipt_text = "\n".join(
                        receipt_lines
                    )


                    st.code(
                        receipt_text,
                        language=None
                    )


                    st.download_button(
                        label="📥 Download Order Summary",
                        data=receipt_text,
                        file_name=(
                            f"order_{order_id}_summary.txt"
                        ),
                        mime="text/plain",
                        key=(
                            f"download_order_"
                            f"{order_id}"
                        ),
                        width="stretch"
                    )


            st.markdown(
                "<div style='height:6px;'></div>",
                unsafe_allow_html=True
            )