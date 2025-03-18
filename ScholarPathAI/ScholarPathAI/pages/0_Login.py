import streamlit as st
import hashlib
import psycopg2
from urllib.parse import urlparse
import os

# Database connection
def get_db_connection():
    try:
        db_url = os.environ['DATABASE_URL']
        result = urlparse(db_url)
        connection = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        return connection
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return None

def create_user_table():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error creating user table: {str(e)}")

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    return stored_password == hash_password(provided_password)

def authenticate_user(username, password):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            
            if result and verify_password(result[0], password):
                return True
            return False
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return False
    return False

def create_user(username, password, email):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            password_hash = hash_password(password)
            cur.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                (username, password_hash, email)
            )
            conn.commit()
            cur.close()
            conn.close()
            return True
        except psycopg2.IntegrityError:
            st.error("Username or email already exists")
            return False
        except Exception as e:
            st.error(f"Error creating user: {str(e)}")
            return False
    return False

def main():
    st.set_page_config(page_title="Login / Signup", layout="centered")
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        
    if st.session_state.logged_in:
        st.success("You are logged in!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        return

    # Create the users table if it doesn't exist
    create_user_table()
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if login_username and login_password:
                if authenticate_user(login_username, login_password):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please fill in all fields")
    
    with tab2:
        st.header("Sign Up")
        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        email = st.text_input("Email", key="signup_email")
        
        if st.button("Sign Up"):
            if new_username and new_password and confirm_password and email:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    if create_user(new_username, new_password, email):
                        st.success("Account created successfully! Please log in.")
                        st.session_state.logged_in = False
                        st.rerun()
            else:
                st.warning("Please fill in all fields")

if __name__ == "__main__":
    main()
