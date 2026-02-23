"""
PDB Knowledge Pack for MikoshiLang
Query the Protein Data Bank (PDB) for experimental structures.
"""

import requests
from typing import List, Dict, Any

HEADERS = {"User-Agent": "MikoshiBio/0.1.0 (https://github.com/DarrenEdwards111/MikoshiBio)"}


class PDBPack:
    """Protein Data Bank experimental structures."""
    
    SEARCH_API = "https://search.rcsb.org/rcsbsearch/v2/query"
    DATA_API = "https://data.rcsb.org/rest/v1/core"
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search PDB structures."""
        try:
            search_query = {
                "query": {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "value": query
                    }
                },
                "return_type": "entry",
                "request_options": {
                    "results_content_type": ["experimental"],
                    "return_all_hits": False,
                    "pager": {
                        "start": 0,
                        "rows": limit
                    }
                }
            }
            
            response = requests.post(
                self.SEARCH_API,
                json=search_query,
                headers=HEADERS,
                timeout=10
            )
            data = response.json()
            
            results = []
            for item in data.get("result_set", []):
                pdb_id = item.get("identifier", "")
                
                # Get basic metadata
                meta_response = requests.get(
                    f"{self.DATA_API}/entry/{pdb_id}",
                    headers=HEADERS,
                    timeout=10
                )
                meta = meta_response.json()
                
                struct = meta.get("struct", {})
                exptl = meta.get("exptl", [{}])[0]
                
                results.append({
                    "id": pdb_id,
                    "label": struct.get("title", ""),
                    "description": exptl.get("method", ""),
                    "url": f"https://www.rcsb.org/structure/{pdb_id}",
                    "source": "PDB",
                    "license": "CC0 1.0",
                })
            
            return results
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_value(self, pdb_id: str, property: str, **kwargs) -> Dict[str, Any]:
        """Get PDB entry metadata."""
        try:
            pdb_id = pdb_id.upper()
            response = requests.get(
                f"{self.DATA_API}/entry/{pdb_id}",
                headers=HEADERS,
                timeout=10
            )
            data = response.json()
            
            value = None
            
            if property == "Title":
                value = data.get("struct", {}).get("title", "")
            
            elif property == "Method":
                exptl = data.get("exptl", [{}])[0]
                value = exptl.get("method", "")
            
            elif property == "Resolution":
                refine = data.get("refine", [{}])[0]
                value = refine.get("ls_d_res_high")
            
            elif property == "ReleaseDate":
                value = data.get("rcsb_accession_info", {}).get("initial_release_date", "")
            
            elif property == "Organism":
                entity = data.get("rcsb_entry_container_identifiers", {})
                value = entity.get("source_organism_names", [None])[0]
            
            elif property == "Chains":
                value = len(data.get("polymer_entities", []))
            
            elif property == "Sequence":
                # Get first polymer entity sequence
                polymers = data.get("polymer_entities", [])
                if polymers:
                    seq_id = polymers[0].get("entity_id")
                    seq_response = requests.get(
                        f"{self.DATA_API}/polymer_entity/{pdb_id}/{seq_id}",
                        headers=HEADERS,
                        timeout=10
                    )
                    seq_data = seq_response.json()
                    seqs = seq_data.get("entity_poly", {}).get("pdbx_seq_one_letter_code", "")
                    value = seqs.replace("\n", "")
            
            elif property == "PDBFile":
                value = f"https://files.rcsb.org/download/{pdb_id}.pdb"
            
            elif property == "MMCIF":
                value = f"https://files.rcsb.org/download/{pdb_id}.cif"
            
            else:
                value = data.get(property)
            
            return {
                "value": value,
                "property": property,
                "entity": pdb_id,
                "source": f"https://www.rcsb.org/structure/{pdb_id}",
                "license": "CC0 1.0",
            }
        except Exception as e:
            return {"error": str(e)}


# Export
__all__ = ["PDBPack"]
