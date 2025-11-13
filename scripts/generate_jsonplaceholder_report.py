"""
Script to generate enhanced HTML report for JSONPlaceholder API tests.

This script generates a comprehensive HTML report that includes:
- Test execution summary
- Endpoint coverage metrics
- Performance analysis
- Success rates by resource
- Detailed test results

Usage:
    python scripts/generate_jsonplaceholder_report.py
"""

import json
import os
from datetime import datetime
from pathlib import Path


def generate_html_report():
    """Generate enhanced HTML report for JSONPlaceholder tests."""
    
    # Read metrics file if it exists
    metrics_file = Path("reports/jsonplaceholder_metrics.txt")
    metrics_content = ""
    if metrics_file.exists():
        with open(metrics_file, "r", encoding="utf-8") as f:
            metrics_content = f.read()
    
    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSONPlaceholder API Test Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        
        .metric-card h3 {{
            color: #667eea;
            font-size: 1.2em;
            margin-bottom: 10px;
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }}
        
        .metric-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .metrics-text {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            line-height: 1.6;
            color: #333;
        }}
        
        .success {{
            color: #28a745;
        }}
        
        .warning {{
            color: #ffc107;
        }}
        
        .danger {{
            color: #dc3545;
        }}
        
        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .info-box h3 {{
            color: #2196F3;
            margin-bottom: 10px;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin: 5px;
        }}
        
        .badge-success {{
            background: #28a745;
            color: white;
        }}
        
        .badge-info {{
            background: #17a2b8;
            color: white;
        }}
        
        .badge-warning {{
            background: #ffc107;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 JSONPlaceholder API Test Report</h1>
            <p>Comprehensive test results and performance metrics</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📊 Test Execution Summary</h2>
                <div class="info-box">
                    <h3>About This Report</h3>
                    <p>This report provides comprehensive metrics for the JSONPlaceholder API test suite, including endpoint coverage, performance analysis, and success rates across all tested resources.</p>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Test Coverage</h3>
                        <div class="metric-value">5</div>
                        <div class="metric-label">Resources Tested</div>
                        <div style="margin-top: 10px;">
                            <span class="badge badge-info">Posts</span>
                            <span class="badge badge-info">Users</span>
                            <span class="badge badge-info">Comments</span>
                            <span class="badge badge-info">Todos</span>
                            <span class="badge badge-info">Albums</span>
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <h3>Test Categories</h3>
                        <div style="margin-top: 10px;">
                            <span class="badge badge-success">Smoke Tests</span>
                            <span class="badge badge-success">CRUD Tests</span>
                            <span class="badge badge-success">Validation Tests</span>
                            <span class="badge badge-success">Filter Tests</span>
                            <span class="badge badge-warning">Performance Tests</span>
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <h3>API Endpoints</h3>
                        <div class="metric-value">20+</div>
                        <div class="metric-label">Endpoints Covered</div>
                    </div>
                    
                    <div class="metric-card">
                        <h3>HTTP Methods</h3>
                        <div style="margin-top: 10px;">
                            <span class="badge badge-info">GET</span>
                            <span class="badge badge-success">POST</span>
                            <span class="badge badge-warning">PUT</span>
                            <span class="badge badge-warning">PATCH</span>
                            <span class="badge badge-danger">DELETE</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📈 Detailed Metrics</h2>
                <div class="metrics-text">{metrics_content if metrics_content else "Run tests to generate metrics: pytest tests/jsonplaceholder/ -v"}</div>
            </div>
            
            <div class="section">
                <h2>🎯 Test Execution Commands</h2>
                <div class="info-box">
                    <h3>Run All Tests</h3>
                    <code style="background: white; padding: 10px; display: block; border-radius: 4px; margin-top: 10px;">
                        pytest tests/jsonplaceholder/ -v
                    </code>
                </div>
                
                <div class="info-box">
                    <h3>Run by Marker</h3>
                    <code style="background: white; padding: 10px; display: block; border-radius: 4px; margin-top: 10px;">
                        pytest tests/jsonplaceholder/ -m smoke -v<br>
                        pytest tests/jsonplaceholder/ -m crud -v<br>
                        pytest tests/jsonplaceholder/ -m validation -v<br>
                        pytest tests/jsonplaceholder/ -m filters -v<br>
                        pytest tests/jsonplaceholder/ -m performance -v
                    </code>
                </div>
                
                <div class="info-box">
                    <h3>Run Specific Resource Tests</h3>
                    <code style="background: white; padding: 10px; display: block; border-radius: 4px; margin-top: 10px;">
                        pytest tests/jsonplaceholder/test_posts.py -v<br>
                        pytest tests/jsonplaceholder/test_users.py -v<br>
                        pytest tests/jsonplaceholder/test_comments.py -v<br>
                        pytest tests/jsonplaceholder/test_todos.py -v<br>
                        pytest tests/jsonplaceholder/test_albums.py -v
                    </code>
                </div>
            </div>
            
            <div class="section">
                <h2>📋 Test Structure</h2>
                <div class="info-box">
                    <h3>Test Files</h3>
                    <ul style="margin-left: 20px; margin-top: 10px; line-height: 1.8;">
                        <li><strong>test_posts.py</strong> - Tests for posts endpoints (GET, POST, PUT, PATCH, DELETE)</li>
                        <li><strong>test_users.py</strong> - Tests for users endpoints (GET, POST, PUT, DELETE)</li>
                        <li><strong>test_comments.py</strong> - Tests for comments endpoints (GET, POST)</li>
                        <li><strong>test_todos.py</strong> - Tests for todos endpoints (GET, POST, PUT)</li>
                        <li><strong>test_albums.py</strong> - Tests for albums endpoints (GET)</li>
                        <li><strong>test_filters.py</strong> - Tests for query parameter filtering</li>
                        <li><strong>test_performance.py</strong> - Performance validation tests</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>JSONPlaceholder API Test Suite | Python Test Automation Framework</p>
            <p style="margin-top: 5px; font-size: 0.9em;">API: https://jsonplaceholder.typicode.com</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    # Write HTML report
    output_file = Path("reports/jsonplaceholder_enhanced_report.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Enhanced HTML report generated: {output_file}")
    print(f"📊 Open the report in your browser to view detailed metrics")


if __name__ == "__main__":
    generate_html_report()
