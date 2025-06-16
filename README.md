# Data_analysis

# IT Inventory Dashboard

A Streamlit web app for analyzing and reporting software installation status on employee devices.  
Upload a single Excel file (with multiple sheets) or multiple CSV files (one per sheet) to get instant, interactive reports on software deployment.

## Features

- Upload Excel or CSV data (main sheet + separate sheets for each software)
- Automatically merges software status into the main device list
- Click any software to see "Installed" and "Not Installed" devices
- Download filtered results as CSV
- No coding required for end users

## How to Use

1. **Prepare Your Data**
    - **Main sheet/file:** Must contain `Serial Number` and `Device` columns.
    - **Each sub-sheet/file:** Must contain `Serial Number` and a status column named like `Status(SoftwareName)` (e.g., `Status(Chrome)`).

2. **Upload Data**
    - Run the app locally with `streamlit run app.py`  
      *or*  
    - Deploy to Streamlit Community Cloud for web access.

3. **Interact**
    - Click a software button in the sidebar to view installed/not installed devices.
    - Download results as CSV if needed.

## Example File Structure

**Main Sheet Example:**
| Serial Number | Device               |
|---------------|----------------------|
| SN0001        | Lenovo Thinkbook     |
| SN0002        | Apple MacBook Air M1 |

**Sub-Sheet Example (Status(Chrome)):**
| Serial Number | Status(Chrome) |
|---------------|---------------|
| SN0001        | Installed     |
| SN0002        | Not Installed |

## Requirements

- Python 3.8+
- streamlit
- pandas

Install dependencies:
