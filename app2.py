import streamlit as st
import pandas as pd

st.set_page_config(page_title="IT Inventory Dashboard", layout="wide")

uploaded_files = st.sidebar.file_uploader(
    "Upload a single Excel file (with all sheets) or multiple CSV files (main + each software sheet)",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

def read_file(file):
    file_type = file.name.split('.')[-1].lower()
    if file_type == 'xlsx':
        return pd.read_excel(file, sheet_name=None)
    elif file_type == 'csv':
        return {file.name.replace('.csv', ''): pd.read_csv(file)}
    else:
        return {}

if uploaded_files:
    all_sheets = {}
    for file in uploaded_files:
        sheets = read_file(file)
        all_sheets.update(sheets)

    sheet_names = list(all_sheets.keys())
    main_sheet_candidates = [name for name in sheet_names if "main" in name.lower() or "sheet1" in name.lower()]
    main_sheet_name = main_sheet_candidates[0] if main_sheet_candidates else sheet_names[0]
    main_df = all_sheets[main_sheet_name]

    # Map software name to column name in main_df
    software_map = {}

    # Merge each sub-sheet's status into main_df
    for sheet_name in sheet_names:
        if sheet_name == main_sheet_name:
            continue
        sub_df = all_sheets[sheet_name]
        if 'Serial Number' in sub_df.columns:
            # Dynamically detect the status column (not 'Serial Number')
            status_cols = [col for col in sub_df.columns if col != 'Serial Number']
            if status_cols:
                status_col = status_cols[0]
                # Extract software name from status column, e.g., Status(Chrome) -> Chrome
                if '(' in status_col and ')' in status_col:
                    software_col = status_col.split('(')[1].split(')')[0].strip()
                else:
                    software_col = sheet_name  # fallback to sheet name
                software_map[software_col] = software_col
                main_df = main_df.merge(
                    sub_df[['Serial Number', status_col]].rename(columns={status_col: software_col}),
                    on='Serial Number',
                    how='left'
                )
            else:
                st.warning(f"Sheet/file '{sheet_name}' does not have a status column.")
        else:
            st.warning(f"Sheet/file '{sheet_name}' must have a 'Serial Number' column.")

    # Now, main_df contains all software status columns
    if 'Device' in main_df.columns:
        software_columns = [col for col in main_df.columns if col not in ['Serial Number', 'Device']]
        for software in software_columns:
            if st.sidebar.button(software):
                installed = main_df[
                    main_df[software].astype(str).str.strip().str.lower() == 'installed'
                ][['Serial Number', 'Device', software]]
                not_installed = main_df[
                    main_df[software].astype(str).str.strip().str.lower() == 'not installed'
                ][['Serial Number', 'Device', software]]
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f"{software} Installed")
                    st.dataframe(installed)
                with col2:
                    st.subheader(f"{software} Not Installed")
                    st.dataframe(not_installed)
                if not installed.empty:
                    st.download_button("Download Installed", installed.to_csv(index=False), "installed.csv")
                if not not_installed.empty:
                    st.download_button("Download Not Installed", not_installed.to_csv(index=False), "not_installed.csv")
        st.write("Main sheet preview:")
        st.dataframe(main_df.head())
    else:
        st.warning("Main sheet/file must have a 'Device' column.")
else:
    st.warning("Please upload your Excel or CSV files.")
