# Python Generators Project (0x00)

Demonstrates advanced Python generator usage for large datasets, batch processing, pagination, and memory-efficient aggregation.

## Setup
1. Install Python 3.x and `mysql-connector-python`.
2. Install MySQL Server (Windows) and note root password.
3. Create database `ALX_prodev` and user `proj_user` (see guide above).
4. Clone this directory in VS Code and run:
   ```bash
   python seed.py      # create schema & seed data
   python 0-stream_users.py
   Python 1-batch_processing.py
   python 2-lazy_paginate.py
   python 4-stream_ages.py