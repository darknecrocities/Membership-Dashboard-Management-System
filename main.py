import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
from io import BytesIO

DB_NAME = "membership.db"

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        time TEXT NOT NULL,
        mode_of_payment TEXT NOT NULL,
        student_number TEXT NOT NULL UNIQUE,
        gmail TEXT NOT NULL UNIQUE,
        details TEXT
    )
''')
    conn.commit()
    conn.close()

# Add Member
def add_member(name, mode_of_payment, student_number, gmail, details):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO members (name, time, mode_of_payment, student_number, gmail, details)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, current_time, mode_of_payment, student_number, gmail, details))
    conn.commit()
    conn.close()

# Search Members
def search_members(keyword):
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT * FROM members 
        WHERE name LIKE ? OR student_number LIKE ?
    '''
    results = pd.read_sql_query(query, conn, params=(f'%{keyword}%', f'%{keyword}%'))
    conn.close()
    return results

# Update Member
def update_member(member_id, name, mode_of_payment, student_number, gmail, details):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE members 
        SET name = ?, mode_of_payment = ?, student_number = ?, gmail = ?, details = ?
        WHERE id = ?
    ''', (name, mode_of_payment, student_number, gmail, details, member_id))
    conn.commit()
    conn.close()

# Delete Member
def delete_member(member_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM members WHERE id = ?', (member_id,))
    conn.commit()
    conn.close()

# Export Data to Excel in memory
def export_to_excel():
    conn = sqlite3.connect(DB_NAME)
    data = pd.read_sql_query("SELECT * FROM members", conn)
    conn.close()
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False, sheet_name="Members")
    output.seek(0)
    return output

# Export Data to CSV in memory
def export_to_csv():
    conn = sqlite3.connect(DB_NAME)
    data = pd.read_sql_query("SELECT * FROM members", conn)
    conn.close()
    output = BytesIO()
    data.to_csv(output, index=False)
    output.seek(0)
    return output

# Get Recent Entries
def get_recent_entries(limit=5):
    conn = sqlite3.connect(DB_NAME)
    data = pd.read_sql_query(f"SELECT * FROM members ORDER BY id DESC LIMIT {limit}", conn)
    conn.close()
    return data

# Advanced Insights
def get_advanced_insights():
    conn = sqlite3.connect(DB_NAME)
    data = pd.read_sql_query("SELECT * FROM members", conn)
    conn.close()
    total_members = len(data)
    if total_members == 0:
        return 0, {}, None
    payment_mode_distribution = data['mode_of_payment'].value_counts().to_dict()
    most_common_mode = data['mode_of_payment'].mode()[0]
    return total_members, payment_mode_distribution, most_common_mode

# Streamlit App
def main():
    st.set_page_config(page_title="Membership Dashboard", layout="wide")
    st.title("🌐📊 Google Developer Group HAU Membership Management System")

    menu = ["Add Member", "View Members", "Edit Member", "Delete Member", "Export Data", "Recent Entries", "Data Insights"]
    choice = st.sidebar.selectbox("Menu", menu)

    init_db()

    if choice == "Add Member":
        st.subheader("➕ Add New Member")
        with st.form("Add Member Form", clear_on_submit=True):
            name = st.text_input("Name")
            mode_of_payment = st.selectbox("Mode of Payment", ["Cash", "Card", "Online"])
            student_number = st.text_input("Student Number")
            gmail = st.text_input("Gmail")
            details = st.text_area("Details (optional)")
            submitted = st.form_submit_button("Add Member")
        if submitted:
            try:
                add_member(name, mode_of_payment, student_number, gmail, details)
                st.success(f"🎉 Member {name} added successfully!")
            except sqlite3.IntegrityError:
                st.error("⚠️ Student Number or Gmail already exists.")

    elif choice == "View Members":
        st.subheader("📋 View Members")
        keyword = st.text_input("Search by Name or Student Number", "")
        results = search_members(keyword)
        if not results.empty:
            st.dataframe(results, use_container_width=True)
        else:
            st.info("No records found.")

    elif choice == "Edit Member":
        st.subheader("✏️ Edit Member Information")
        all_members = search_members("")
        if not all_members.empty:
            member_id = st.selectbox("Select Member to Edit", all_members["id"])
            member_details = all_members[all_members["id"] == member_id].iloc[0]
            with st.form("Edit Member Form", clear_on_submit=True):
                name = st.text_input("Name", member_details["name"])
                mode_of_payment = st.selectbox("Mode of Payment", ["Cash", "Card", "Online"], index=["Cash", "Card", "Online"].index(member_details["mode_of_payment"]))
                student_number = st.text_input("Student Number", member_details["student_number"])
                gmail = st.text_input("Gmail", member_details["gmail"])
                details = st.text_area("Details (optional)", member_details["details"])
                submitted = st.form_submit_button("Update Member")
            if submitted:
                update_member(member_id, name, mode_of_payment, student_number, gmail, details)
                st.success(f"✅ Member {name} updated successfully!")

    elif choice == "Delete Member":
        st.subheader("❌ Delete a Member")
        all_members = search_members("")
        if not all_members.empty:
            member_id = st.selectbox("Select Member to Delete", all_members["id"])
            if st.button("Delete"):
                delete_member(member_id)
                st.success(f"✅ Member ID {member_id} deleted successfully!")
        else:
            st.info("No members to delete.")

    elif choice == "Export Data":
        st.subheader("📤 Export Data")
        col1, col2 = st.columns(2)
        with col1:
            excel_data = export_to_excel()
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name="members.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with col2:
            csv_data = export_to_csv()
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="members.csv",
                mime="text/csv"
            )

    elif choice == "Recent Entries":
        st.subheader("🕒 Recent Entries")
        recent_entries = get_recent_entries()
        if not recent_entries.empty:
            st.dataframe(recent_entries, use_container_width=True)
        else:
            st.info("No recent entries.")

    elif choice == "Data Insights":
        st.subheader("📈 Data Insights")
        total_members, payment_mode_distribution, most_common_mode = get_advanced_insights()
        if total_members == 0:
            st.info("No data available for insights.")
        else:
            st.metric("Total Members", total_members)
            st.write("**Payment Mode Distribution:**")
            st.bar_chart(pd.DataFrame(payment_mode_distribution.items(), columns=["Mode of Payment", "Count"]).set_index("Mode of Payment"))
            st.write(f"**Most Common Payment Mode:** {most_common_mode}")

if __name__ == "__main__":
    main()
