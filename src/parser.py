from bs4 import BeautifulSoup


def parse( html : bytearray ) -> dict:
    
    data = {
        
        "buy"  : {

        },
        "sell" : {
            
        },
    
        "sellpoint" : 0,
        "buypoint"  : 999999999,
        
    }

    soup = BeautifulSoup( html, "html.parser" )
    
    forsale_div = soup.find_all("div", id="market_commodity_forsale_table")
    buyreq_div  = soup.find_all("div", id="market_commodity_buyreqeusts_table")

    try:
        # Parse "For sale"-listings
        for table in buyreq_div[0].find_all("tbody"):
            for row in table.find_all("tr"):
                
                tags = row.find_all( "td" )
                
                if tags == []:
                    continue
                
                price, amount = tags[ 0 ].get_text(strip=True).strip("$"), tags[ 1 ].get_text(strip=True)
                
                if "or" in str(price):
                    continue

                data["sell"][float(price)] = int( amount )
            
                data["sellpoint"] = max( float(price), data["sellpoint"] )

        # Parse "Buy requests"-listings
        for table in forsale_div[0].find_all("tbody"):
            for row in table.find_all("tr"):
                
                tags = row.find_all( "td" )
                
                if tags == []:
                    continue
                
                price, amount = tags[ 0 ].get_text(strip=True).strip("$"), tags[ 1 ].get_text(strip=True)

                if "or" in str(price):
                    continue

                data["buy"][float(price)] = int( amount )

                data["buypoint"] = min( float(price), data["buypoint"] )

    except IndexError:
        print( f"[!] Ran into an IndexError. Context:", str(soup) )

    return data
