import os
import json
from typing import Dict, Any

class JSONReaderTool:
    """Safe parser and key-extractor for structured grant applications and guideline JSONs."""
    
    @staticmethod
    def read_json(file_path: str, extract_key: str = None) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if extract_key:
                val = data.get(extract_key)
                return {"success": True, "key": extract_key, "data": val}
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def validate_schema(data: Dict[str, Any], required_keys: list) -> Dict[str, Any]:
        missing = [k for k in required_keys if k not in data or data[k] is None]
        return {
            "is_valid": len(missing) == 0,
            "missing_keys": missing,
            "present_keys": [k for k in required_keys if k in data]
        }
