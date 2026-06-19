import hashlib
import json
import os
from web3 import Web3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRACT_JSON_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "..", "blockchain", "deployed_contract.json"))

GANACHE_URL = os.getenv("GANACHE_URL", "http://127.0.0.1:8545")
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

def get_contract():
    if not os.path.exists(CONTRACT_JSON_PATH):
        print(f"❌ Upozorenje: Datoteka {CONTRACT_JSON_PATH} ne postoji. Pokreni deploy.py prvo!")
        return None
        
    with open(CONTRACT_JSON_PATH, "r", encoding="utf-8") as f:
        contract_data = json.load(f)
        
    return w3.eth.contract(
        address=contract_data["contract_address"],
        abi=contract_data["abi"]
    )

def calculate_event_hash(articles: list) -> str:
    urls = sorted([str(article.get("url", "")) for article in articles if article.get("url")])
    
    combined_string = "".join(urls)
    
    return hashlib.sha256(combined_string.encode("utf-8")).hexdigest()

def record_event_on_blockchain(event_id: str, articles: list) -> bool:
    try:
        contract = get_contract()
        if not contract or not w3.is_connected():
            print("❌ Neuspješno spajanje na blockchain.")
            return False
            
        content_hash = calculate_event_hash(articles)
        
        w3.eth.default_account = w3.eth.accounts[0]
        
        print(f"🔗 Zapisujem na blockchain: Event {event_id} sa hashem {content_hash}...")
        
        tx_hash = contract.functions.storeEvent(event_id, content_hash).transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"✅ Uspješno zapisano! TX Hash: {tx_hash.hex()}")
        return True
    except Exception as e:
        print(f"❌ Greška pri zapisu na blockchain: {e}")
        return False