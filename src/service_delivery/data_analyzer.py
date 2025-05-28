"""
Data Analyzer for Service Delivery
This module analyzes data for clients.
"""

import os
import logging
import json
import random
import pandas as pd
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

class DataAnalyzer:
    """Analyzes data for clients."""
    
    def __init__(self):
        """Initialize the Data Analyzer."""
        logger.info("Initialized Data Analyzer")
    
    def analyze_data(self, data_file, analysis_type, parameters=None):
        """Analyze data based on specified type and parameters."""
        logger.info(f"Analyzing data file: {data_file}, type: {analysis_type}")
        
        try:
            # Load data
            data = self._load_data(data_file)
            
            if data is None:
                return {
                    "error": "Failed to load data file",
                    "success": False
                }
            
            # Perform analysis based on type
            if analysis_type == "descriptive":
                result = self._descriptive_analysis(data, parameters)
            elif analysis_type == "trend":
                result = self._trend_analysis(data, parameters)
            elif analysis_type == "correlation":
                result = self._correlation_analysis(data, parameters)
            elif analysis_type == "segmentation":
                result = self._segmentation_analysis(data, parameters)
            else:
                return {
                    "error": f"Unknown analysis type: {analysis_type}",
                    "success": False
                }
            
            # Generate report
            report_file = self._generate_report(result, analysis_type, data_file)
            
            # Generate visualizations
            visualization_files = self._generate_visualizations(result, analysis_type, data_file)
            
            return {
                "success": True,
                "analysis_type": analysis_type,
                "result_summary": result["summary"],
                "report_file": report_file,
                "visualization_files": visualization_files
            }
        
        except Exception as e:
            logger.error(f"Error analyzing data: {e}")
            return {
                "error": str(e),
                "success": False
            }
    
    def _load_data(self, data_file):
        """Load data from file."""
        try:
            # Determine file type from extension
            file_ext = os.path.splitext(data_file)[1].lower()
            
            if file_ext == '.csv':
                return pd.read_csv(data_file)
            elif file_ext == '.xlsx' or file_ext == '.xls':
                return pd.read_excel(data_file)
            elif file_ext == '.json':
                return pd.read_json(data_file)
            else:
                logger.error(f"Unsupported file format: {file_ext}")
                return None
        
        except Exception as e:
            logger.error(f"Error loading data file {data_file}: {e}")
            return None
    
    def _descriptive_analysis(self, data, parameters=None):
        """Perform descriptive statistical analysis."""
        # In a real implementation, this would perform actual analysis
        # For this demo, we'll simulate analysis results
        
        # Get basic statistics
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) == 0:
            return {
                "summary": "No numeric columns found for analysis",
                "details": {}
            }
        
        stats = {}
        for column in numeric_columns:
            stats[column] = {
                "mean": float(data[column].mean()),
                "median": float(data[column].median()),
                "std": float(data[column].std()),
                "min": float(data[column].min()),
                "max": float(data[column].max()),
                "q1": float(data[column].quantile(0.25)),
                "q3": float(data[column].quantile(0.75))
            }
        
        # Count categorical values
        categorical_columns = data.select_dtypes(include=['object']).columns
        categories = {}
        
        for column in categorical_columns:
            categories[column] = data[column].value_counts().to_dict()
        
        # Generate insights
        insights = [
            f"The average {numeric_columns[0]} is {stats[numeric_columns[0]]['mean']:.2f}",
            f"The highest {numeric_columns[0]} is {stats[numeric_columns[0]]['max']:.2f}",
            f"The data shows a standard deviation of {stats[numeric_columns[0]]['std']:.2f} for {numeric_columns[0]}"
        ]
        
        if len(categorical_columns) > 0:
            top_category = data[categorical_columns[0]].value_counts().index[0]
            insights.append(f"The most common {categorical_columns[0]} is {top_category}")
        
        return {
            "summary": "Descriptive analysis completed successfully",
            "statistics": stats,
            "categories": categories,
            "insights": insights,
            "details": {
                "numeric_columns": list(numeric_columns),
                "categorical_columns": list(categorical_columns),
                "row_count": len(data),
                "column_count": len(data.columns)
            }
        }
    
    def _trend_analysis(self, data, parameters=None):
        """Perform trend analysis."""
        # In a real implementation, this would perform actual trend analysis
        # For this demo, we'll simulate analysis results
        
        # Check if we have date/time columns
        date_columns = []
        for column in data.columns:
            if 'date' in column.lower() or 'time' in column.lower():
                date_columns.append(column)
        
        if not date_columns:
            return {
                "summary": "No date/time columns found for trend analysis",
                "details": {}
            }
        
        # Use the first date column
        date_column = date_columns[0]
        
        # Find numeric columns for trends
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) == 0:
            return {
                "summary": "No numeric columns found for trend analysis",
                "details": {}
            }
        
        # Simulate trend results
        trends = {}
        for column in numeric_columns:
            # Generate random trend data
            trend_direction = random.choice(["increasing", "decreasing", "stable"])
            trend_strength = random.uniform(0.1, 0.9)
            
            trends[column] = {
                "direction": trend_direction,
                "strength": trend_strength,
                "significance": trend_strength > 0.5
            }
        
        # Generate insights
        insights = []
        for column, trend in trends.items():
            insights.append(f"{column} shows a {trend['direction']} trend (strength: {trend['strength']:.2f})")
            
            if trend["significance"]:
                insights.append(f"The {trend['direction']} trend in {column} is statistically significant")
        
        return {
            "summary": "Trend analysis completed successfully",
            "date_column": date_column,
            "trends": trends,
            "insights": insights,
            "details": {
                "date_columns": date_columns,
                "numeric_columns": list(numeric_columns),
                "time_period": f"{data[date_column].min()} to {data[date_column].max()}"
            }
        }
    
    def _correlation_analysis(self, data, parameters=None):
        """Perform correlation analysis."""
        # In a real implementation, this would perform actual correlation analysis
        # For this demo, we'll simulate analysis results
        
        # Get numeric columns for correlation
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) < 2:
            return {
                "summary": "Need at least 2 numeric columns for correlation analysis",
                "details": {}
            }
        
        # Calculate correlation matrix
        corr_matrix = data[numeric_columns].corr().to_dict()
        
        # Find strongest correlations
        strong_correlations = []
        for col1 in numeric_columns:
            for col2 in numeric_columns:
                if col1 != col2:
                    corr_value = corr_matrix[col1][col2]
                    if abs(corr_value) > 0.5:  # Threshold for strong correlation
                        strong_correlations.append({
                            "column1": col1,
                            "column2": col2,
                            "correlation": corr_value,
                            "type": "positive" if corr_value > 0 else "negative"
                        })
        
        # Sort by absolute correlation strength
        strong_correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)
        
        # Generate insights
        insights = []
        for corr in strong_correlations[:3]:  # Top 3 correlations
            insights.append(
                f"{corr['column1']} and {corr['column2']} have a {corr['type']} correlation of {corr['correlation']:.2f}"
            )
        
        return {
            "summary": "Correlation analysis completed successfully",
            "correlation_matrix": corr_matrix,
            "strong_correlations": strong_correlations,
            "insights": insights,
            "details": {
                "numeric_columns": list(numeric_columns),
                "correlation_count": len(strong_correlations)
            }
        }
    
    def _segmentation_analysis(self, data, parameters=None):
        """Perform customer segmentation analysis."""
        # In a real implementation, this would perform actual segmentation
        # For this demo, we'll simulate analysis results
        
        # Get parameters
        segment_column = None
        if parameters and "segment_column" in parameters:
            segment_column = parameters["segment_column"]
        
        # If no segment column specified, try to find one
        if not segment_column:
            for column in data.columns:
                if "segment" in column.lower() or "category" in column.lower() or "type" in column.lower():
                    segment_column = column
                    break
        
        # If still no segment column, use the first categorical column
        if not segment_column:
            categorical_columns = data.select_dtypes(include=['object']).columns
            if len(categorical_columns) > 0:
                segment_column = categorical_columns[0]
        
        if not segment_column:
            return {
                "summary": "No suitable column found for segmentation analysis",
                "details": {}
            }
        
        # Get segments
        segments = data[segment_column].unique()
        
        # Get numeric columns for segment comparison
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) == 0:
            return {
                "summary": "No numeric columns found for segment comparison",
                "details": {}
            }
        
        # Calculate segment statistics
        segment_stats = {}
        for segment in segments:
            segment_data = data[data[segment_column] == segment]
            
            segment_stats[segment] = {}
            for column in numeric_columns:
                segment_stats[segment][column] = {
                    "mean": float(segment_data[column].mean()),
                    "median": float(segment_data[column].median()),
                    "std": float(segment_data[column].std()),
                    "count": int(segment_data[column].count())
                }
        
        # Generate insights
        insights = []
        for segment in segments:
            for column in numeric_columns:
                segment_mean = segment_stats[segment][column]["mean"]
                overall_mean = float(data[column].mean())
                
                difference = segment_mean - overall_mean
                percent_diff = (difference / overall_mean) * 100
                
                if abs(percent_diff) > 20:  # Significant difference threshold
                    direction = "higher" if difference > 0 else "lower"
                    insights.append(
                        f"Segment '{segment}' has {abs(percent_diff):.1f}% {direction} {column} than average"
                    )
        
        return {
            "summary": "Segmentation analysis completed successfully",
            "segment_column": segment_column,
            "segments": list(segments),
            "segment_stats": segment_stats,
            "insights": insights,
            "details": {
                "segment_count": len(segments),
                "numeric_columns": list(numeric_columns)
            }
        }
    
    def _generate_report(self, result, analysis_type, data_file):
        """Generate a report file from analysis results."""
        # Create a filename
        base_name = os.path.splitext(os.path.basename(data_file))[0]
        filename = f"/tmp/{base_name}_{analysis_type}_report_{datetime.now().strftime('%Y%m%d')}.json"
        
        # In a real implementation, this would actually write to the file
        # For this demo, we'll just return the filename
        
        return filename
    
    def _generate_visualizations(self, result, analysis_type, data_file):
        """Generate visualization files from analysis results."""
        # In a real implementation, this would generate actual visualizations
        # For this demo, we'll simulate visualization filenames
        
        base_name = os.path.splitext(os.path.basename(data_file))[0]
        
        # Generate different visualizations based on analysis type
        if analysis_type == "descriptive":
            return [
                f"/tmp/{base_name}_histogram_{datetime.now().strftime('%Y%m%d')}.png",
                f"/tmp/{base_name}_boxplot_{datetime.now().strftime('%Y%m%d')}.png"
            ]
        elif analysis_type == "trend":
            return [
                f"/tmp/{base_name}_trend_line_{datetime.now().strftime('%Y%m%d')}.png",
                f"/tmp/{base_name}_seasonal_{datetime.now().strftime('%Y%m%d')}.png"
            ]
        elif analysis_type == "correlation":
            return [
                f"/tmp/{base_name}_correlation_matrix_{datetime.now().strftime('%Y%m%d')}.png",
                f"/tmp/{base_name}_scatter_plot_{datetime.now().strftime('%Y%m%d')}.png"
            ]
        elif analysis_type == "segmentation":
            return [
                f"/tmp/{base_name}_segment_comparison_{datetime.now().strftime('%Y%m%d')}.png",
                f"/tmp/{base_name}_segment_distribution_{datetime.now().strftime('%Y%m%d')}.png"
            ]
        else:
            return []
