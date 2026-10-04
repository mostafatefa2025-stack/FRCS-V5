import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data_store")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "frcs_v5_master.db")
APP_TITLE = "Financial Risk & Corporate Support System - FRCS V5"
APP_VERSION = "5.0.0"

SECTORS = [
    "Manufacturing & Industrial",
    "Food & Agriculture Manufacturing",
    "Real Estate & Construction",
    "Retail & Wholesale Trade",
    "Commercial Services",
    "Healthcare & Pharmaceuticals",
    "Technology & Telecom",
    "SME General Trading"
]

ACCOUNTING_STANDARDS = ["IFRS", "EAS (Egyptian Accounting Standards)", "US GAAP"]
CURRENCIES = ["EGP", "USD", "EUR", "SAR", "AED"]
