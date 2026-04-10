To build a professional-grade web application for processing bank statements like BCA Tahapan, you need an architecture that handles **OCR asynchronous processing**, **relational data storage**, and a **"Human-in-the-loop" validation UI**.

Here is a comprehensive 5-step plan to build this application.

---

### 1. The Tech Stack
*   **Frontend:** React.js or Next.js (for the dashboard and file upload).
*   **Backend:** Python (FastAPI or Flask) – Python is essential for the data processing libraries.
*   **Database:** PostgreSQL (to handle structured transaction history and relational accounts).
*   **File Storage:** AWS S3 or Google Cloud Storage (to store the original statement images/PDFs).
*   **OCR Engine:** 
    *   *Tier 1 (Pro):* AWS Textract or Google Cloud Vision (they handle tables perfectly).
    *   *Tier 2 (DIY):* Tesseract OCR + the Python parsing script provided earlier.
*   **Task Queue:** Celery + Redis (Processing OCR takes 10–30 seconds; you need a queue so the user doesn't wait on a frozen screen).

---

### 2. Database Schema (The Foundation)
To support "History per month" and "multiple accounts," your schema should look like this:

*   **Users:** ID, Name, Email, Password.
*   **Accounts:** ID, User_ID, Account_Number (e.g., 0953709187), Account_Name (Raka Feisal), Bank_Name (BCA).
*   **Statements:** ID, Account_ID, Period_Month, Period_Year, File_URL, Upload_Date.
*   **Transactions:** ID, Statement_ID, Date, Description, Mutation_Amount, Type (Debit/Credit), Balance, **Category** (e.g., Food, Transport, Transfer).

---

### 3. The Processing Pipeline (The "Brain")
Since OCR is never 100% perfect, your app should follow this workflow:

1.  **Upload:** User uploads images/PDF.
2.  **Extraction:** 
    *   Backend sends files to OCR.
    *   OCR returns raw text or JSON.
    *   Your Python script parses the raw text into a list of transaction objects.
3.  **Intermediate Storage:** Save results into a "Pending Review" state in the database.
4.  **Verification (Crucial):** Show the user a spreadsheet-like UI where they can fix any OCR typos or assign categories.
5.  **Commit:** Once the user clicks "Save," move data to the permanent `Transactions` table.

---

### 4. Application Features Roadmap

#### Phase 1: MVP (Extract & Export)
*   User login/signup.
*   Simple upload button.
*   Table view of extracted data.
*   "Download as CSV" button.

#### Phase 2: History & Accounts
*   **Dashboard:** Show "Total Spent this Month" vs "Total Income."
*   **Account Switching:** A sidebar to choose between different bank accounts.
*   **Date Filters:** Filter history by month/year (e.g., "Show me March 2026").

#### Phase 3: Intelligence
*   **Auto-Categorization:** Use simple keywords (e.g., "IDM INDOMA" -> *Groceries*, "SOTO AYAM" -> *Dining*) to automatically categorize spending.
*   **Visualizations:** Charts (Pie chart of spending, Line chart of balance over time).
*   **Search:** A search bar to find that one specific transaction from 6 months ago.

---

### 5. Key Technical Challenges & Solutions

| Challenge | Solution |
| :--- | :--- |
| **Multi-line Descriptions** | Use a "Buffer" logic in your Python parser: if a line doesn't start with a date, append it to the description of the previous transaction. |
| **Data Privacy** | Encrypt the `Account_Number` in the database. Ensure the S3 bucket for images is private and uses signed URLs for viewing. |
| **Duplicate Prevention** | Before saving, check if a transaction with the same Date, Amount, and Balance already exists for that Account to prevent double-uploading the same statement. |
| **OCR Table Alignment** | Use **AWS Textract "Queries" or "Tables" feature**. It specifically identifies rows and columns, which is much more reliable than parsing raw text strings. |

---

### Recommended UI Layout
*   **Sidebar:** Accounts List, History (Months/Years), Settings.
*   **Header:** Current Account Balance, User Profile.
*   **Main Content:**
    *   *Top:* Key Stats (Total Out, Total In).
    *   *Middle:* A searchable, sortable data table of transactions.
    *   *Action:* Floating "Upload New Statement" button.

**Would you like a sample database schema (SQL) or a basic FastAPI starter structure to get started on the backend?**
