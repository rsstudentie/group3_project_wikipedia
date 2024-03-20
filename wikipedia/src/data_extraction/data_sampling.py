from sqlalchemy import MetaData, Table, Column, Integer, String, select

from wikipedia.src.sqllite.sqllite_engine import SqlLiteEngine


def sample_data():
    """
    This function samples the data from the wikipedia_complete database and inserts the top 100 pages into a new
    SQLite database called wikipedia.

    :return: None
    """
    # Create an instance of SqlLiteEngine with the desired database
    db_engine = SqlLiteEngine(db="wikipedia_complete")

    # Connect to the existing SQLite database
    existing_engine = db_engine.get_engine()
    existing_conn = existing_engine.connect()

    # Step 1: Find the top 100 pages based on total visits
    metadata = MetaData()
    page_visits = Table(
        'page_visits',
        metadata,
        Column('Page', String),
        Column('Date', String),
        Column('Visits', Integer)
    )
    query_top_pages = select([page_visits.c.Page, page_visits.c.Date, page_visits.c.Visits]).group_by(
        page_visits.c.Page).order_by(page_visits.c.Visits.desc()).limit(100)
    top_pages = existing_conn.execute(query_top_pages)

    # Connect to the new SQLite database (this will create the file)
    new_engine = db_engine.get_engine(db="wikipedia")
    new_conn = new_engine.connect()

    # Creating a new table in the new SQLite database
    metadata.create_all(new_engine)

    # Inserting top pages into the new SQLite database
    new_page_visits = Table(
        'page_visits',
        metadata,
        autoload=True,
        autoload_with=new_engine
    )

    new_conn.execute(new_page_visits.delete())
    new_conn.execute(new_page_visits.insert(),
                     [dict(Page=page, Date=date, Visits=visits) for page, date, visits in top_pages])

    # Close connections
    existing_conn.close()
    new_conn.close()
