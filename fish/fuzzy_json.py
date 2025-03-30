import json
import re


class FuzzyJsonStorage:
    def __init__(self, data=None):
        """Initialize the storage with optional data dictionary."""
        self.original_data = data or {}
        self.normalized_keys = self._build_normalized_keys(self.original_data)

    def set(self, key, value):
        """Add or update a key-value pair."""
        normalized_key = self._normalize_key(key)
        self.original_data[key] = value
        self.normalized_keys[normalized_key] = key
        return self

    def get(self, search_key, threshold=0.7):
        """Get a value by key with fuzzy matching."""
        # First try exact match with normalized key
        normalized_search_key = self._normalize_key(search_key)
        if normalized_search_key in self.normalized_keys:
            original_key = self.normalized_keys[normalized_search_key]
            return self.original_data[original_key]

        # If no exact match on normalized key, try fuzzy matching
        matches = self._find_fuzzy_matches(search_key, threshold)
        if matches:
            # Return the best match
            best_match = matches[0]
            return self.original_data[best_match["original_key"]]

        # No matches found
        return None

    def find_all(self, search_key, threshold=0.7):
        """Find all matches using fuzzy matching."""
        matches = self._find_fuzzy_matches(search_key, threshold)
        return [
            {
                "key": match["original_key"],
                "value": self.original_data[match["original_key"]],
                "similarity": match["similarity"]
            }
            for match in matches
        ]

    def _normalize_key(self, key):
        """Normalize a key for comparison."""
        if not isinstance(key, str):
            return str(key)
        # Convert to lowercase and remove non-alphanumeric characters
        return re.sub(r'[^a-z0-9]', '', key.lower())

    def _build_normalized_keys(self, data):
        """Build a lookup of normalized keys to original keys."""
        normalized = {}
        for key in data:
            normalized_key = self._normalize_key(key)
            normalized[normalized_key] = key
        return normalized

    def _find_fuzzy_matches(self, search_key, threshold):
        """Find fuzzy matches using string similarity."""
        normalized_search_key = self._normalize_key(search_key)
        results = []

        # Calculate similarity for all keys
        for original_key in self.original_data:
            similarity = self._calculate_similarity(
                normalized_search_key,
                self._normalize_key(original_key)
            )
            
            if similarity >= threshold:
                results.append({
                    "original_key": original_key,
                    "similarity": similarity
                })

        # Sort by similarity (highest first)
        return sorted(results, key=lambda x: x["similarity"], reverse=True)

    def _calculate_similarity(self, str1, str2):
        """Calculate string similarity using Levenshtein distance."""
        len1, len2 = len(str1), len(str2)
        
        # If either string is empty, the similarity is 0
        if len1 == 0 or len2 == 0:
            return 0
        
        # Early exact match
        if str1 == str2:
            return 1
        
        # Calculate Levenshtein distance
        distance = self._levenshtein_distance(str1, str2)
        
        # Convert distance to similarity score (0-1)
        max_len = max(len1, len2)
        return 1 - (distance / max_len)

    def _levenshtein_distance(self, str1, str2):
        """Compute Levenshtein distance between two strings."""
        len1, len2 = len(str1), len(str2)
        
        # Create 2D matrix
        matrix = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]
        
        # Initialize first row and column
        for i in range(len1 + 1):
            matrix[i][0] = i
        for j in range(len2 + 1):
            matrix[0][j] = j
        
        # Fill the matrix
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if str1[i-1] == str2[j-1] else 1
                matrix[i][j] = min(
                    matrix[i-1][j] + 1,       # deletion
                    matrix[i][j-1] + 1,       # insertion
                    matrix[i-1][j-1] + cost   # substitution
                )
        
        return matrix[len1][len2]

    def get_all_data(self):
        """Get all data."""
        return self.original_data.copy()
    
    def save_to_file(self, filename):
        """Save the data to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.original_data, f, indent=2)
            
    @classmethod
    def load_from_file(cls, filename):
        """Load data from a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(data)


# Example usage
if __name__ == "__main__":
    storage = FuzzyJsonStorage({
        "Peter Griffin": {"age": 43, "occupation": "Safety Inspector"},
        "Lois Griffin": {"age": 40, "occupation": "Housewife"},
        "Brian Griffin": {"age": 7, "occupation": "Writer"}
    })

    # Exact match
    print("Exact match:", storage.get("Peter Griffin"))

    # Normalized match
    print("Normalized match:", storage.get("petergriffin"))

    # Fuzzy match
    print("Fuzzy match:", storage.get("peter griffen"))

    # No Match
    # Fuzzy match
    print("Fuzzy match:", storage.get("donald trump"))

    # Find all potential matches
    print("All Griffin matches:", storage.find_all("griffin", 0.5))

    # Add a new entry
    storage.set("Stewie Griffin", {"age": 1, "occupation": "Evil Genius"})

    # Get all data
    print("All data:", storage.get_all_data())
    
    # Save to file
    storage.save_to_file("family_data.json")
    
    # Load from file
    loaded_storage = FuzzyJsonStorage.load_from_file("family_data.json")
    print("Loaded data:", loaded_storage.get_all_data())