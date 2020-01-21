from app.models import UserTable, BookTable, SubmissionTable
import sys


def main():

    msg = "You can use command init to create app tables and reset to drop app tables"

    if len(sys.argv) <= 1:
        print(msg)
        return

    if sys.argv[1] == "init":
        create_tables()
        return

    if sys.argv[1] == "reset":
        drop_tables()
        return

    print(msg)


def create_tables():
    ut = UserTable()
    bt = BookTable()
    st = SubmissionTable()

    ut.create_table()
    bt.create_table()
    st.create_table()


def drop_tables():
    ut = UserTable()
    bt = BookTable()
    st = SubmissionTable()

    ut.drop_table()
    bt.drop_table()
    st.drop_table()


main()
