
# 🌐📊 Google Developer Group HAU Membership Management System

🌐📊 **Google Developer Group HAU Membership Management System** is a powerful and easy-to-use membership management application designed to help you manage the membership of your community, university group, or organization. With features like adding new members, searching, updating, deleting, and exporting member data, this system helps you stay organized and efficient.

## 🚀 Features

- **➕ Add Member**: Easily add new members to the system, including personal details, mode of payment, and contact information.
- **📋 View Members**: Search for members by name or student number and view all the details in a table format.
- **✏️ Edit Member**: Update member information such as name, mode of payment, student number, and contact details.
- **❌ Delete Member**: Remove a member from the database by selecting the member and clicking delete.
- **📤 Export Data**: Export the entire member list to either Excel or CSV format.
- **🕒 Recent Entries**: View the most recent members added to the system.
- **📈 Data Insights**: Get valuable insights into the membership data, including the total number of members, payment mode distribution, and the most common payment mode.

## 🛠️ Technologies Used

- **🐍 Python**: The main programming language for the application.
- **🗃️ SQLite**: Used for the database to store member information.
- **📊 Pandas**: Used for data manipulation and exporting data to Excel and CSV.
- **🌐 Streamlit**: A framework for building the web interface of the app.
- **📝 XlsxWriter**: For generating Excel files from the data.

## 📥 Setup

To run this project locally, follow the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/membership-management-system.git
   cd membership-management-system
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Open the app in your browser at `http://localhost:8501`.

## 🔍 Features in Detail

### ➕ Add Member
- Add new members to the system with details like name, payment mode, student number, Gmail, and an optional text field for additional details.

### 📋 View Members
- Search for members using keywords like name or student number and view the results in a dynamic table.

### ✏️ Edit Member
- Edit the details of existing members. You can update personal information, payment mode, student number, and Gmail.

### ❌ Delete Member
- Select and delete members from the system by their ID.

### 📤 Export Data
- Export all members to either an Excel or CSV file to back up or analyze the data.

### 🕒 Recent Entries
- View the most recent member entries in the system.

### 📈 Data Insights
- Get advanced insights like the total number of members, the distribution of payment modes, and the most common payment mode.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Developed by: Arron Kian M. Parejas
