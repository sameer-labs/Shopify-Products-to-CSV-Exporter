# Shopify Products → CSV Exporter

## Overview

This project provides a Python script that connects to the Shopify REST API, retrieves product and inventory data, and exports it into a clean, Excel-ready CSV file.

It is designed for store owners, analysts, and operators who need a reliable way to extract Shopify product data for reporting or analysis.

## Features

- Connects to Shopify REST API
- Handles pagination for large stores
- Extracts product and inventory data
- Outputs a clean CSV file
- Uses environment variables for secure credentials

## Output Columns
```
product_id
title
vendor
sku
price
inventory_quantity
status
```

## Requirements

- Python 3.9+
- Shopify API access

Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

1. Copy `.env.example` to `.env` and add your credentials
2. Run the script:
```bash
python shopify_export.py
```

3. The CSV file will be saved to the `output/` folder

## Notes

- This script is read-only
- No store data is modified
- Suitable for one-time exports or scheduled automation
