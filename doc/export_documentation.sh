#!/usr/bin/env bash

echo
./docs2markdown.py

echo "AirwindoPedia: Markdown -> HTML..."
pandoc --self-contained \
    --from=commonmark \
    --to=html+native_spans \
    --css="include/documentation.css" \
    --variable="pagetitle:AirwindoPedia" \
    --variable="lang:en-US" \
    --output="AirwindoPedia.html" \
    "AirwindoPedia.md"

echo "AirwindoPedia: Done."
echo