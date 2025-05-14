#
#
#
create_item_table = """
CREATE TABLE Item (
    
    id         INTEGER PRIMARY KEY,
    item_name  TEXT, -- Case Name
    item_url   TEXT -- Market URL for case    

);
"""

insert_into_item = """
INSERT INTO Item (

    item_name,
    item_url    

) VALUES (?, ?);
"""


#
#
#
create_data_table = """
CREATE TABLE Data (

    id         INTEGER PRIMARY KEY,
    item_id    INTEGER,                            -- Case ID
    json       TEXT,                               -- JSON stored as TEXT
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Auto timestamp

    FOREIGN KEY (item_id) REFERENCES Item(id)

);
"""

insert_data_table = """
INSERT INTO Data (

    item_id,
    json    

) VALUES (?, ?);
"""