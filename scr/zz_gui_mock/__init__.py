#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI Package for aNA v5.0

This package provides the neural dashboard interface for real-time
monitoring of the aNA v5.0 neural architecture.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Cline
"""

from .dashboard import NeuralDashboard, create_dashboard
from .integration import DashboardController, create_dashboard_controller, integrate_dashboard_with_controller
from .test_dashboard import run_comprehensive_test, demo_dashboard

__all__ = [
    'NeuralDashboard',
    'create_dashboard',
    'DashboardController', 
    'create_dashboard_controller',
    'integrate_dashboard_with_controller',
    'run_comprehensive_test',
    'demo_dashboard'
]