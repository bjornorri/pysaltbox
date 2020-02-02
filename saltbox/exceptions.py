"""Custom exceptions"""

class RouterLoginException(Exception):
    """Exception raised for failed logins"""

class RouterNotReachableException(Exception):
    """Exception raised when data cannot be pulled from router"""
