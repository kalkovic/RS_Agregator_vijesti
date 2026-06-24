import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRACT_PATH = os.path.join(BASE_DIR, "NewsRegistry.sol")
OUTPUT_PATH = os.path.join(BASE_DIR, "deployed_contract.json")

with open(CONTRACT_PATH, "r", encoding="utf-8") as file:
    news_registry_file = file.read()

print("-> Kompajliram pametni ugovor...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"NewsRegistry.sol": {"content": news_registry_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

bytecode = compiled_sol["contracts"]["NewsRegistry.sol"]["NewsRegistry"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["NewsRegistry.sol"]["NewsRegistry"]["metadata"])["output"]["abi"]

ganache_url = "http://ganache-cli:8545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

if not w3.is_connected():
    print("❌ GREŠKA: Ne mogu se spojiti na Ganache! Provjeri radi li Ganache u pozadinskom terminalu.")
    exit()

print("✅ Uspješno spojen na Ganache blockchain.")

w3.eth.default_account = w3.eth.accounts[0]

print("-> Pokrećem deploy ugovora na mrežu...")
NewsRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = NewsRegistry.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
print(f"🎉 Pametni ugovor je USPJEŠNO POSTAVLJEN!")
print(f"📍 Adresa ugovora: {contract_address}")

deployment_info = {
    "contract_address": contract_address,
    "abi": abi
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(deployment_info, f, indent=4, ensure_ascii=False)

print(f"💾 Podaci za spajanje spremljeni u: blockchain/deployed_contract.json")