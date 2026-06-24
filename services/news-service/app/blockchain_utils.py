import hashlib
import json
import os
from web3 import Web3
from app.config import settings

CONTRACT_JSON_PATH = "/blockchain/deployed_contract.json"

w3 = Web3(Web3.HTTPProvider(settings.ganache_url))

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

def record_event_on_blockchain(event_id: str, articles: list) -> dict:
    try:
        contract = get_contract()
        if not contract or not w3.is_connected():
            print("❌ Neuspješno spajanje na blockchain.")
            return {"success": False, "tx_hash": None}

        content_hash = calculate_event_hash(articles)

        w3.eth.default_account = w3.eth.accounts[0]

        print(f"🔗 Zapisujem na blockchain: Event {event_id} sa hashem {content_hash}...")

        tx_hash = contract.functions.storeEvent(event_id, content_hash).transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)

        tx_hash_hex = tx_hash.hex()
        print(f"✅ Uspješno zapisano! TX Hash: {tx_hash_hex}")
        return {"success": True, "tx_hash": tx_hash_hex}
    except Exception as e:
        print(f"❌ Greška pri zapisu na blockchain: {e}")
        return {"success": False, "tx_hash": None}
    
def verify_event_on_blockchain(event_id: str, local_hash: str) -> dict:
    try:
        contract = get_contract()
        if not contract or not w3.is_connected():
            return {"status": "error", "message": "Nema veze s blockchainom."}
            
        try:
            stored_hash = contract.functions.getEventHash(event_id).call()
        except Exception as e:
            return {"status": "error", "message": f"Događaj nije na blockchainu: {str(e)}"}
            
        is_valid = (local_hash == stored_hash)
        
        return {
            "status": "success",
            "is_valid": is_valid,
            "local_hash": local_hash,
            "blockchain_hash": stored_hash
        }
    except Exception as e:
        return {"status": "error", "message": f"Greška pri provjeri: {str(e)}"}