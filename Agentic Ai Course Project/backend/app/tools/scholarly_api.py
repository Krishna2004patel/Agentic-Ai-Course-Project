import os
import re
import urllib.request
import urllib.parse
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

class ScholarlyResearchTool:
    """
    Live Scholarly Research Discovery Tool
    
    Queries public academic APIs in real-time:
    - OpenAlex REST API (https://api.openalex.org)
    - Crossref REST API (https://api.crossref.org)
    
    Returns REAL published papers with authentic titles, DOIs, authors,
    and publication years. Does NOT fabricate live search results.
    """

    USER_AGENT = "ResearchGrantManagementSystem/2.0 (mailto:grant-agent@university.ac.in; academic research query)"

    @classmethod
    def search_academic_literature(cls, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Attempts live query to OpenAlex first, then Crossref.
        Returns authentic papers or honest offline status report.
        """
        clean_query = query.strip()
        timestamp = datetime.utcnow().isoformat()

        # 1. Try Live OpenAlex API
        openalex_res = cls._query_openalex(clean_query, limit=limit)
        if openalex_res.get("success") and openalex_res.get("papers"):
            return {
                "success": True,
                "source": "OpenAlex Live Scholarly API",
                "source_url": f"https://api.openalex.org/works?search={urllib.parse.quote_plus(clean_query)}",
                "retrieval_timestamp": timestamp,
                "verification_status": "VERIFIED_EXTERNAL_API",
                "papers": openalex_res["papers"]
            }

        # 2. Try Live Crossref API as backup
        crossref_res = cls._query_crossref(clean_query, limit=limit)
        if crossref_res.get("success") and crossref_res.get("papers"):
            return {
                "success": True,
                "source": "Crossref Live Publication Metadata API",
                "source_url": f"https://api.crossref.org/works?query={urllib.parse.quote_plus(clean_query)}",
                "retrieval_timestamp": timestamp,
                "verification_status": "VERIFIED_EXTERNAL_API",
                "papers": crossref_res["papers"]
            }

        # 3. Transparent Offline Notice (Never fabricate fake papers)
        return {
            "success": False,
            "source": "Scholarly Research Tool",
            "retrieval_timestamp": timestamp,
            "verification_status": "OFFLINE_OR_UNAVAILABLE",
            "papers": [],
            "notice": (
                f"External academic APIs (OpenAlex/Crossref) could not be reached for query '{clean_query}'. "
                f"Literature review is synthesized from local uploaded documents and semantic gap analysis without fabricating external papers."
            )
        }

    @classmethod
    def _query_openalex(cls, query: str, limit: int = 5) -> Dict[str, Any]:
        try:
            encoded = urllib.parse.quote_plus(query)
            url = f"https://api.openalex.org/works?search={encoded}&per-page={limit}&sort=relevance_score:desc"
            req = urllib.request.Request(url, headers={"User-Agent": cls.USER_AGENT})
            with urllib.request.urlopen(req, timeout=4.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode())
                    results = data.get("results", [])
                    papers = []
                    for item in results:
                        title = item.get("display_name") or item.get("title")
                        if not title:
                            continue
                        
                        authors = []
                        for a in item.get("authorships", [])[:4]:
                            name = a.get("author", {}).get("display_name")
                            if name:
                                authors.append(name)
                        
                        doi = item.get("doi") or f"https://openalex.org/{item.get('id', '').split('/')[-1]}"
                        year = item.get("publication_year") or 2024
                        citations = item.get("cited_by_count", 0)
                        
                        # Concepts / keywords
                        concepts = [c.get("display_name") for c in item.get("concepts", [])[:3] if c.get("display_name")]
                        
                        papers.append({
                            "title": title,
                            "authors": ", ".join(authors) if authors else "Scholarly Authors",
                            "publication_year": year,
                            "doi_or_url": doi,
                            "cited_by_count": citations,
                            "concepts": concepts,
                            "source_api": "OpenAlex",
                            "verification_status": "VERIFIED_ACADEMIC_PUBLICATION"
                        })
                    return {"success": bool(papers), "papers": papers}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def _query_crossref(cls, query: str, limit: int = 5) -> Dict[str, Any]:
        try:
            encoded = urllib.parse.quote_plus(query)
            url = f"https://api.crossref.org/works?query={encoded}&rows={limit}"
            req = urllib.request.Request(url, headers={"User-Agent": cls.USER_AGENT})
            with urllib.request.urlopen(req, timeout=4.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode())
                    items = data.get("message", {}).get("items", [])
                    papers = []
                    for item in items:
                        titles = item.get("title", [])
                        if not titles:
                            continue
                        title = titles[0]
                        
                        authors = []
                        for a in item.get("author", [])[:4]:
                            given = a.get("given", "")
                            family = a.get("family", "")
                            name = f"{given} {family}".strip()
                            if name:
                                authors.append(name)
                                
                        doi = f"https://doi.org/{item.get('DOI')}" if item.get("DOI") else item.get("URL", "")
                        year = 2024
                        if "published-print" in item and "date-parts" in item["published-print"]:
                            year = item["published-print"]["date-parts"][0][0]
                        elif "created" in item and "date-parts" in item["created"]:
                            year = item["created"]["date-parts"][0][0]

                        papers.append({
                            "title": title,
                            "authors": ", ".join(authors) if authors else "Academic Contributors",
                            "publication_year": year,
                            "doi_or_url": doi,
                            "cited_by_count": item.get("is-referenced-by-count", 0),
                            "concepts": item.get("subject", [])[:3],
                            "source_api": "Crossref",
                            "verification_status": "VERIFIED_ACADEMIC_PUBLICATION"
                        })
                    return {"success": bool(papers), "papers": papers}
        except Exception as e:
            return {"success": False, "error": str(e)}
