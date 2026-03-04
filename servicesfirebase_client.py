"""
Firebase Client Service
Architectural Choice: Singleton pattern with lazy initialization ensures
only one Firebase connection pool and prevents resource leaks.
Edge Cases Handled: Connection retries, credential validation, timeout handling.
"""

import os
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging

import firebase_admin
from firebase_admin import credentials, firestore, auth, exceptions
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.base_query import FieldFilter

from config.settings import settings

logger = logging.getLogger(__name__)

class FirebaseClient:
    """Singleton Firebase client with connection pooling and error recovery"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Lazy initialization