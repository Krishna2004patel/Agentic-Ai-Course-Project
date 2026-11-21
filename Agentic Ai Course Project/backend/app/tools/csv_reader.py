import os
import csv
from typing import Dict, Any, List, Optional

class CSVReaderTool:
    """Safe CSV reader and query tool for funding databases and research datasets."""
    
    @staticmethod
    def read_csv(file_path: str, filter_col: Optional[str] = None, filter_val: Optional[str] = None, limit: int = 50) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}
        
        try:
            records = []
            with open(file_path, mode='r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                for row in reader:
                    if filter_col and filter_val:
                        if filter_col in row and filter_val.lower() in str(row[filter_col]).lower():
                            records.append(row)
                    else:
                        records.append(row)
                    if len(records) >= limit:
                        break
                        
            return {
                "success": True,
                "file_path": file_path,
                "headers": headers,
                "total_matched": len(records),
                "data": records
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def aggregate_column(file_path: str, numeric_column: str) -> Dict[str, Any]:
        """Calculates sum, average, min, and max for a numeric column."""
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}
        try:
            values = []
            with open(file_path, mode='r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if numeric_column in row:
                        try:
                            # clean currency or comma
                            clean_str = str(row[numeric_column]).replace(',', '').replace('$', '').replace('₹', '').strip()
                            values.append(float(clean_str))
                        except (ValueError, TypeError):
                            continue
            if not values:
                return {"success": False, "error": f"No numeric data found in column '{numeric_column}'"}
            
            return {
                "success": True,
                "column": numeric_column,
                "count": len(values),
                "sum": round(sum(values), 2),
                "mean": round(sum(values) / len(values), 2),
                "min": min(values),
                "max": max(values)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
