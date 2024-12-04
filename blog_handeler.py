import os
import frontmatter
import time
import mistune
import json
import sqlite3

def fetch(database):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    last_modfified_dates = cur.execute("SELECT last_modified_date FROM records;")
    #WIP

def convert_mdh(text: str) -> str:
    """ Converts a markdown into HTML """
    markdown = mistune.create_markdown()
    html = markdown(text)
    return html

class Database():
    def __init__(self, filepath = "C:/Users/ghosa/Desktop/Master Folder/Programing/portfolio-web/blog") -> None:
        self.cur = None
        self.filepath = filepath

    
    def create_db(self):
        # Create SQLite Database
        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS records (title TEXT NOT NULL UNIQUE, data TEXT NOT NULL UNIQUE, last_modified_date TEXT NOT NULL);")

        # Intiate Search for written blogs
        absolute_blog_folder_path = self.filepath
        os.chdir(absolute_blog_folder_path)
        directories = os.listdir()

        # Create database useing files, their contents, metadata
        for filename in directories:
            filepath = f"{self.filepath}/{filename}"
            markdown_file_object = frontmatter.load(filepath)
            text = markdown_file_object.content
            timestamp = os.path.getmtime(filename)

            data = convert_mdh(text)
            title = filename.rstrip('.md')
            self.title = title
            last_modified_date = time.strftime('%B %d %Y', time.localtime(timestamp))
            
            # Fill Database
            try:
                self.cur.execute("INSERT INTO records (title, data, last_modified_date) VALUES (?,?,?);", (title, data, last_modified_date))
            except sqlite3.IntegrityError:
                continue
            self.con.commit()

# Create Database
database = Database()
database.create_db()

