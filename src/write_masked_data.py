#Write to PostgreSQL


def create_user_logins_table(conn):
    """
    Creates a table called user_logins if it does not exist
    Appends the table with new entries
    """
    create_table_query = """
        CREATE TABLE IF NOT EXISTS user_logins(
            user_id varchar(128),
            device_type varchar(32),
            masked_ip varchar(256),
            masked_device_id varchar(256),
            locale varchar(32),
            app_version integer,
            create_date date
        )
    """

    try:
        # Creating a cursor object using the connection
        cursor = conn.cursor()

        # Executing the SQL command
        cursor.execute(create_table_query)

        # Commit the changes
        conn.commit()
        print("Table created successfully!")

    except Exception as e:
        print(f"Error creating table: {e}")

    finally:
        # Close the cursor
        cursor.close()

def write_to_postgres(data, conn):
    query = """
        INSERT INTO user_logins (
            user_id, device_type, masked_ip, masked_device_id,
            locale, app_version
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """

    with conn.cursor() as cur:
        cur.execute(query, (
            data['user_id'],
            data['device_type'],
            data['masked_ip'],
            data['masked_device_id'],
            data['locale'],
            data['app_version'],
        ))

    conn.commit()