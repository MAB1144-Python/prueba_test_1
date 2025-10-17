"""
Website Design Evaluator Package
Herramienta automatizada para evaluar el diseño de sitios web
"""

from .website_evaluator import WebsiteEvaluator
from .screenshot_capture import ScreenshotCapture
from .design_analyzer import DesignAnalyzer
from .cloud_storage import CloudStorageManager
from .report_generator import ReportGenerator
from .google_sheets_integration import GoogleSheetsIntegration

__version__ = "1.0.0"
__author__ = "Website Design Evaluator Team"

# Exportar clases principales
__all__ = [
    'WebsiteEvaluator',
    'ScreenshotCapture', 
    'DesignAnalyzer',
    'CloudStorageManager',
    'ReportGenerator',
    'GoogleSheetsIntegration'
]