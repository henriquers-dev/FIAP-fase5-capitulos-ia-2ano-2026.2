# HEADER
# KPI: GMV v1.2.0 | Author: Analytics Team | Date: 2025-09-20
import pandas as pd
import hashlib
...
# HASH SAMPLE
sample_hash = hashlib.sha256(df.head(100).to_csv().encode()).hexdigest()
assert sample_hash == 'abc123...'
