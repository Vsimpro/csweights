import src.queries  as queries
import src.database as database

import src.items   as item_bank
import src.parser  as parser
import src.scraper as scraper


def ensure_item_in_db( item_url ) -> bool:
    item_name   = item_bank.defang_item_url( item_url )
    item_exists = database.query_database( "SELECT 1 FROM Item WHERE item_name = ?", (item_name,) )

    if item_exists:
        return True
    
    database.insert_data(
        queries.insert_into_item,
        ( item_name, item_url )
    )
    return False
    

def main( debug : bool = False ):

    #
    #   Make sure all the items of interest are found in DB.
    #
    items = item_bank.read_file( "./items/cases.txt" )
    for item in items:
        if not ensure_item_in_db( item ):
            print( "[+] Added", item )
        
        elif debug:
            print( f"[+] {item} Already in database!" )

    #
    #   Get & Store data for the item
    #

    for item_url in items:
        if debug: print( "[+] Scraping page for: ", item_bank.defang_item_url( item_url ))
        page = scraper.fetch_market_page( item_url )

        if page == "":
            continue

        if debug: print( "[+] Parsing data for: ", item_bank.defang_item_url( item_url ) )
        data = str(parser.parse( page ))

        item_id = database.query_database( "SELECT id FROM Item WHERE item_url = ?", (item_url,) )[0][0]

        if debug: print( "[+] Storing data for: ", item_bank.defang_item_url( item_url ) )
        database.insert_data(
            queries.insert_data_table,
            (item_id, data)
        )

    return


if __name__ == "__main__":
    database.initialize_db()
    database.create_tables(
        {
            "Item" : queries.create_item_table,
            "Data" : queries.create_data_table 
        }
    )

    main( True )
