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


def get_image_folder():

    image_folder = (
        get_project_root()
        / "assets"
        / "products"
    )

    image_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return image_folder


def save_uploaded_image(
    uploaded_file,
    product_id
):

    if uploaded_file is None:

        return None


    file_extension = (
        Path(uploaded_file.name)
        .suffix
        .lower()
    )


    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }


    if file_extension not in allowed_extensions:

        return None


    image_folder = get_image_folder()


    file_name = (
        f"product_{product_id}"
        f"{file_extension}"
    )


    file_path = (
        image_folder
        / file_name
    )


    # -----------------------------------------------------
    # Remove old local product images
    # -----------------------------------------------------

    for old_file in image_folder.glob(
        f"product_{product_id}.*"
    ):

        if old_file != file_path:

            try:

                old_file.unlink()

            except OSError:

                pass


    # -----------------------------------------------------
    # Save new image
    # -----------------------------------------------------

    with open(
        file_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )


    # -----------------------------------------------------
    # Database path
    # -----------------------------------------------------

    relative_path = (
        Path("assets")
        / "products"
        / file_name
    )


    return str(
        relative_path
    ).replace(
        "\\",
        "/"
    )


def get_local_image_path(
    image_source
):

    if not image_source:

        return None


    image_source = str(
        image_source
    ).strip()


    # -----------------------------------------------------
    # Remote image URL
    # -----------------------------------------------------

    if (
        image_source.startswith(
            "http://"
        )
        or image_source.startswith(
            "https://"
        )
    ):

        return image_source


    # -----------------------------------------------------
    # Local image
    # -----------------------------------------------------

    project_root = get_project_root()


    image_path = (
        project_root
        / image_source
    )


    if image_path.exists():

        return str(
            image_path
        )


    return None


def display_product_image(
    image_source,
    width=85
):

    if not image_source:

        st.caption(
            "No Image"
        )

        return


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

        st.caption(
            "Image unavailable"
        )


# =========================================================
# PRODUCT MANAGEMENT PAGE
# =========================================================

def show_product_management():

    sales_manager = SalesManager()


    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.markdown(
        """
        <div style="
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        ">
            🍔 Product Management
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div style="
            font-size: 1rem;
            color: #666666;
            margin-bottom: 1.2rem;
        ">
            Manage café products, prices, categories,
            images and availability
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # LOAD PRODUCTS
    # =====================================================

    products = (
        sales_manager.get_all_products()
    )


    # =====================================================
    # SUMMARY METRICS
    # =====================================================

    total_products = len(
        products
    )


    available_products = len(
        [
            product
            for product in products
            if product.availability
        ]
    )


    unavailable_products = (
        total_products
        - available_products
    )


    categories = sorted(
        set(
            product.category
            for product in products
            if product.category
        )
    )


    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total Products",
            total_products
        )


    with col2:

        st.metric(
            "Available",
            available_products
        )


    with col3:

        st.metric(
            "Unavailable",
            unavailable_products
        )


    with col4:

        st.metric(
            "Categories",
            len(categories)
        )


    st.divider()


    # =====================================================
    # ADD PRODUCT
    # =====================================================

    st.subheader(
        "➕ Add New Product"
    )


    with st.form(
        "add_product_form"
    ):

        col1, col2 = st.columns(2)


        with col1:

            product_name = st.text_input(
                "Product Name",
                placeholder="e.g. Chicken Burger"
            )


        with col2:

            category = st.text_input(
                "Category",
                placeholder="e.g. Burger"
            )


        col1, col2 = st.columns(2)


        with col1:

            price = st.number_input(
                "Price (Rs.)",
                min_value=0.0,
                max_value=1000000.0,
                value=0.0,
                step=50.0
            )


        with col2:

            availability = st.checkbox(
                "Available for Sale",
                value=True
            )


        # -------------------------------------------------
        # IMAGE UPLOAD
        # -------------------------------------------------

        uploaded_image = st.file_uploader(
            "Product Image",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ],
            help=(
                "Upload a product photo "
                "from your computer."
            )
        )


        # -------------------------------------------------
        # IMAGE PREVIEW
        # -------------------------------------------------

        if uploaded_image is not None:

            st.markdown(
                "#### 🖼️ Image Preview"
            )

            st.image(
                uploaded_image,
                width=180
            )


        add_product_button = (
            st.form_submit_button(
                "➕ Add Product",
                width="stretch"
            )
        )


        if add_product_button:

            product_name = (
                product_name
                .strip()
            )


            category = (
                category
                .strip()
            )


            # ---------------------------------------------
            # VALIDATION
            # ---------------------------------------------

            if not product_name:

                st.error(
                    "Please enter a product name."
                )


            elif not category:

                st.error(
                    "Please enter a category."
                )


            elif price <= 0:

                st.error(
                    "Price must be greater than 0."
                )


            else:

                # -----------------------------------------
                # Create product first
                # -----------------------------------------

                success, result = (
                    sales_manager.add_product(
                        product_name,
                        category,
                        price,
                        availability,
                        None
                    )
                )


                if success:

                    product_id = result


                    # -------------------------------------
                    # Save uploaded image
                    # -------------------------------------

                    image_path = (
                        save_uploaded_image(
                            uploaded_image,
                            product_id
                        )
                    )


                    # -------------------------------------
                    # Update image path
                    # -------------------------------------

                    if image_path:

                        sales_manager.update_product(
                            product_id,
                            product_name,
                            category,
                            price,
                            availability,
                            image_path
                        )


                    st.success(
                        f"✅ Product '{product_name}' "
                        f"added successfully."
                    )


                    st.rerun()


                else:

                    st.error(
                        f"❌ Could not add product: "
                        f"{result}"
                    )


    st.divider()


    # =====================================================
    # SEARCH + FILTER
    # =====================================================

    st.subheader(
        "🔎 Product List"
    )


    filter_col1, filter_col2, filter_col3 = st.columns(
        [2, 1, 1]
    )


    with filter_col1:

        search_text = st.text_input(
            "Search Product",
            placeholder=(
                "Search by product name "
                "or category..."
            )
        )


    with filter_col2:

        category_filter_options = (
            ["All"] + categories
        )


        category_filter = st.selectbox(
            "Category",
            category_filter_options
        )


    with filter_col3:

        availability_filter = (
            st.selectbox(
                "Availability",
                [
                    "All",
                    "Available",
                    "Unavailable"
                ]
            )
        )


    # =====================================================
    # FILTER PRODUCTS
    # =====================================================

    filtered_products = []


    for product in products:

        # ---------------------------------------------
        # SEARCH
        # ---------------------------------------------

        if search_text:

            search_value = (
                search_text
                .strip()
                .lower()
            )


            searchable_text = (
                str(product.product_name)
                + " "
                + str(product.category)
            ).lower()


            if (
                search_value
                not in searchable_text
            ):

                continue


        # ---------------------------------------------
        # CATEGORY
        # ---------------------------------------------

        if (
            category_filter != "All"
            and product.category
            != category_filter
        ):

            continue


        # ---------------------------------------------
        # AVAILABILITY
        # ---------------------------------------------

        if (
            availability_filter
            == "Available"
            and not product.availability
        ):

            continue


        if (
            availability_filter
            == "Unavailable"
            and product.availability
        ):

            continue


        filtered_products.append(
            product
        )


    # =====================================================
    # RESULT COUNT
    # =====================================================

    st.caption(
        f"Showing {len(filtered_products)} "
        f"of {len(products)} product(s)."
    )


    # =====================================================
    # NO PRODUCTS
    # =====================================================

    if not filtered_products:

        st.info(
            "No products match the selected filters."
        )

        return


    # =====================================================
    # PRODUCT TABLE HEADER
    # =====================================================

    (
        header_col1,
        header_col2,
        header_col3,
        header_col4,
        header_col5,
        header_col6
    ) = st.columns(
        [1, 1.5, 3, 2, 1.5, 2]
    )


    with header_col1:

        st.write(
            "**ID**"
        )


    with header_col2:

        st.write(
            "**Image**"
        )


    with header_col3:

        st.write(
            "**Product**"
        )


    with header_col4:

        st.write(
            "**Category**"
        )


    with header_col5:

        st.write(
            "**Price**"
        )


    with header_col6:

        st.write(
            "**Availability**"
        )


    st.divider()


    # =====================================================
    # PRODUCT LIST
    # =====================================================

    for product in filtered_products:

        (
            col1,
            col2,
            col3,
            col4,
            col5,
            col6
        ) = st.columns(
            [1, 1.5, 3, 2, 1.5, 2]
        )


        # -------------------------------------------------
        # ID
        # -------------------------------------------------

        with col1:

            st.write(
                product.product_id
            )


        # -------------------------------------------------
        # IMAGE
        # -------------------------------------------------

        with col2:

            display_product_image(
                product.image_url,
                width=85
            )


        # -------------------------------------------------
        # PRODUCT NAME
        # -------------------------------------------------

        with col3:

            st.write(
                f"**{product.product_name}**"
            )


        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        with col4:

            st.write(
                product.category
            )


        # -------------------------------------------------
        # PRICE
        # -------------------------------------------------

        with col5:

            st.write(
                f"Rs. "
                f"{float(product.price):,.2f}"
            )


        # -------------------------------------------------
        # AVAILABILITY
        # -------------------------------------------------

        with col6:

            if product.availability:

                st.success(
                    "Available"
                )

            else:

                st.error(
                    "Unavailable"
                )


        # =================================================
        # EDIT PRODUCT
        # =================================================

        with st.expander(
            f"✏️ Manage Product #{product.product_id}"
        ):

            st.markdown(
                "### Edit Product"
            )


            edit_col1, edit_col2 = (
                st.columns(2)
            )


            with edit_col1:

                new_product_name = (
                    st.text_input(
                        "Product Name",
                        value=product.product_name,
                        key=(
                            f"edit_name_"
                            f"{product.product_id}"
                        )
                    )
                )


            with edit_col2:

                new_category = (
                    st.text_input(
                        "Category",
                        value=product.category,
                        key=(
                            f"edit_category_"
                            f"{product.product_id}"
                        )
                    )
                )


            edit_col1, edit_col2 = (
                st.columns(2)
            )


            with edit_col1:

                new_price = (
                    st.number_input(
                        "Price (Rs.)",
                        min_value=0.0,
                        value=float(
                            product.price
                        ),
                        step=50.0,
                        key=(
                            f"edit_price_"
                            f"{product.product_id}"
                        )
                    )
                )


            with edit_col2:

                new_availability = (
                    st.checkbox(
                        "Available for Sale",
                        value=bool(
                            product.availability
                        ),
                        key=(
                            f"edit_available_"
                            f"{product.product_id}"
                        )
                    )
                )


            # -------------------------------------------------
            # EXISTING IMAGE
            # -------------------------------------------------

            st.markdown(
                "#### Current Image"
            )


            display_product_image(
                product.image_url,
                width=180
            )


            # -------------------------------------------------
            # NEW IMAGE UPLOAD
            # -------------------------------------------------

            new_uploaded_image = (
                st.file_uploader(
                    "Replace Product Image",
                    type=[
                        "jpg",
                        "jpeg",
                        "png",
                        "webp"
                    ],
                    key=(
                        f"edit_image_"
                        f"{product.product_id}"
                    ),
                    help=(
                        "Upload a new photo "
                        "to replace the current image."
                    )
                )
            )


            # -------------------------------------------------
            # NEW IMAGE PREVIEW
            # -------------------------------------------------

            if (
                new_uploaded_image
                is not None
            ):

                st.markdown(
                    "#### New Image Preview"
                )


                st.image(
                    new_uploaded_image,
                    width=180
                )


            # =================================================
            # UPDATE
            # =================================================

            if st.button(
                "💾 Update Product",
                key=(
                    f"update_product_"
                    f"{product.product_id}"
                ),
                width="stretch"
            ):

                new_product_name = (
                    new_product_name
                    .strip()
                )


                new_category = (
                    new_category
                    .strip()
                )


                # ---------------------------------------------
                # VALIDATION
                # ---------------------------------------------

                if not new_product_name:

                    st.error(
                        "Product name cannot be empty."
                    )


                elif not new_category:

                    st.error(
                        "Category cannot be empty."
                    )


                elif new_price <= 0:

                    st.error(
                        "Price must be greater than 0."
                    )


                else:

                    # -----------------------------------------
                    # Keep current image by default
                    # -----------------------------------------

                    image_path = (
                        product.image_url
                    )


                    # -----------------------------------------
                    # Save new image if uploaded
                    # -----------------------------------------

                    if (
                        new_uploaded_image
                        is not None
                    ):

                        new_image_path = (
                            save_uploaded_image(
                                new_uploaded_image,
                                product.product_id
                            )
                        )


                        if new_image_path:

                            image_path = (
                                new_image_path
                            )


                    # -----------------------------------------
                    # Update database
                    # -----------------------------------------

                    success, result = (
                        sales_manager.update_product(
                            product.product_id,
                            new_product_name,
                            new_category,
                            new_price,
                            new_availability,
                            image_path
                        )
                    )


                    if success:

                        st.success(
                            "✅ Product updated successfully."
                        )


                        st.rerun()


                    else:

                        st.error(
                            f"❌ Update failed: "
                            f"{result}"
                        )


            # =================================================
            # DELETE
            # =================================================

            st.markdown(
                "### 🗑️ Delete Product"
            )


            st.warning(
                "Deleting a product that is already "
                "used in orders may be prevented by "
                "the database."
            )


            delete_confirm = st.checkbox(
                "I understand that this product will be deleted.",
                key=(
                    f"delete_confirm_"
                    f"{product.product_id}"
                )
            )


            if st.button(
                "🗑️ Delete Product",
                key=(
                    f"delete_product_"
                    f"{product.product_id}"
                ),
                width="stretch"
            ):

                if not delete_confirm:

                    st.error(
                        "Please confirm deletion first."
                    )


                else:

                    success, result = (
                        sales_manager.delete_product(
                            product.product_id
                        )
                    )


                    if success:

                        st.success(
                            "✅ Product deleted successfully."
                        )

                        st.rerun()


                    else:

                        st.error(
                            f"❌ Could not delete product: "
                            f"{result}"
                        )


        st.markdown("---")