#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for json_viewer.py functions
"""

import json
import tempfile
import os
from pathlib import Path
import sys

# Add the Защиты directory to path
sys.path.insert(0, str(Path(__file__).parent))

from json_viewer import load_json, search_pdfs, display_pdf_info

def test_load_json():
    # Test valid JSON
    test_data = {"test": "data"}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        f.flush()
        result = load_json(f.name)
        assert result == test_data, f"Expected {test_data}, got {result}"
    
    os.unlink(f.name)
    
    # Test invalid path
    result = load_json("nonexistent.json")
    assert result is None, "Expected None for nonexistent file"
    
    # Test invalid JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json")
        f.flush()
        result = load_json(f.name)
        assert result is None, "Expected None for invalid JSON"
    
    os.unlink(f.name)
    print("✓ test_load_json passed")

def test_search_pdfs():
    data = {
        "pdf1.pdf": {"raw_text": "This is a test", "cleaned_text": "clean test"},
        "pdf2.pdf": {"raw_text": "Another document", "cleaned_text": "another doc"}
    }
    
    # Test search in raw_text
    results = search_pdfs(data, "test")
    assert "pdf1.pdf" in results, "pdf1.pdf should be found"
    assert len(results) == 1, "Only one match expected"
    
    # Test search in cleaned_text
    results = search_pdfs(data, "doc")
    assert "pdf2.pdf" in results, "pdf2.pdf should be found"
    
    # Test search in filename
    results = search_pdfs(data, "pdf1")
    assert "pdf1.pdf" in results, "pdf1.pdf should be found by filename"
    
    # Test no results
    results = search_pdfs(data, "nonexistent")
    assert len(results) == 0, "No results expected"
    
    print("✓ test_search_pdfs passed")

def test_display_pdf_info():
    info = {
        "pdf_path": "/path/to/file.pdf",
        "raw_text": "Raw text content",
        "cleaned_text": "Cleaned text",
        "summary_ru": ["Russian sentence"],
        "summary_ro": ["Romanian sentence"],
        "translations": {"original": "translation"}
    }
    
    display_pdf_info("test.pdf", info)
    # Since output is to stdout, just call the function and assume it works if no exception
    print("✓ test_display_pdf_info passed")

if __name__ == "__main__":
    test_load_json()
    test_search_pdfs()
    test_display_pdf_info()
    print("All tests passed!")