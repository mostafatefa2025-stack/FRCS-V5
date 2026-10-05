import sys
import math
import numpy as np
import pandas as pd
import traceback

def global_exception_handler(exc_type, exc_value, exc_tb):
    err = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(None, "FRCS V5 Engine Error", f"System Encountered Exception:\n\n{err}")
    except Exception:
        print(err)
    sys.exit(1)

sys.excepthook = global_exception_handler

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
    QHBoxLayout, QFrame, QDialog, QFormLayout, QLineEdit, QMessageBox,
    QGroupBox, QScrollArea, QTabWidget, QComboBox, QGridLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QTextEdit, QSplitter, QTreeWidget, QTreeWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class FRCSFullEngineSuite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financial Risk & Consulting System - FRCS V5 Professional Enterprise Edition")
        self.resize(1280, 850)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Header Bar
        header = QFrame()
        header.setStyleSheet("background: linear-gradient(135deg, #0F172A, #1E3A8A); border-radius: 8px; padding: 15px;")
        h_layout = QVBoxLayout(header)
        title = QLabel("FRCS V5 - ADVANCED CORPORATE VALUATION & DISTRESS ENGINE")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #F8FAFC; font-size: 22px; font-weight: bold; letter-spacing: 1px;")
        subtitle = QLabel("Comprehensive Financial Statement Modeling | Bankruptcy Analytics | CAPM & WACC | DCF & DDM Valuation Suite")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #93C5FD; font-size: 13px;")
        h_layout.addWidget(title)
        h_layout.addWidget(subtitle)
        main_layout.addWidget(header)

        # Tab Navigator
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { font-weight: bold; padding: 10px 20px; }")
        
        self.tab_inputs = QWidget()
        self.tab_distress = QWidget()
        self.tab_valuation = QWidget()
        self.tab_sensitivity = QWidget()
        
        self.tabs.addTab(self.tab_inputs, "1. Financial Statements & Data Inputs")
        self.tabs.addTab(self.tab_distress, "2. Bankruptcy & Distress Scores (Multi-Model)")
        self.tabs.addTab(self.tab_valuation, "3. WACC & Valuation Models (DCF / DDM / Multiples)")
        self.tabs.addTab(self.tab_sensitivity, "4. Stress Testing & Scenario Matrix")
        
        main_layout.addWidget(self.tabs)

        # Build Tab Content
        self.init_inputs_tab()
        self.init_distress_tab()
        self.init_valuation_tab()
        self.init_sensitivity_tab()

        # Action Buttons Bottom
        btn_layout = QHBoxLayout()
        calc_all_btn = QPushButton("RUN COMPREHENSIVE ENTERPRISE EVALUATION (ALL ENGINES)")
        calc_all_btn.setStyleSheet("background-color: #059669; color: white; padding: 14px; font-weight: bold; font-size: 14px; border-radius: 6px;")
        calc_all_btn.clicked.connect(self.run_full_analysis)
        btn_layout.addWidget(calc_all_btn)
        main_layout.addLayout(btn_layout)

    def init_inputs_tab(self):
        layout = QVBoxLayout(self.tab_inputs)
        
        # Parameters Box
        param_box = QGroupBox("Corporate Macro & Capital Parameters")
        grid = QGridLayout(param_box)
        
        self.company_name = QLineEdit("EGX Listed Target Enterprise")
        self.sector_box = QComboBox()
        self.sector_box.addItems(["Manufacturing & Industrial", "Real Estate & Housing", "Retail & Commerce", "Services & Tech"])
        
        self.rf_rate = QLineEdit("0.135")
        self.beta = QLineEdit("1.15")
        self.erp = QLineEdit("0.085")
        self.cost_debt = QLineEdit("0.150")
        self.tax_rate = QLineEdit("0.225")
        self.shares_out = QLineEdit("50000000")
        self.terminal_g = QLineEdit("0.04")
        self.d1_dividend = QLineEdit("3.50")

        grid.addWidget(QLabel("Enterprise Name:"), 0, 0)
        grid.addWidget(self.company_name, 0, 1)
        grid.addWidget(QLabel("Sector:"), 0, 2)
        grid.addWidget(self.sector_box, 0, 3)

        grid.addWidget(QLabel("Risk-Free Rate (Rf):"), 1, 0)
        grid.addWidget(self.rf_rate, 1, 1)
        grid.addWidget(QLabel("Equity Beta (β):"), 1, 2)
        grid.addWidget(self.beta, 1, 3)

        grid.addWidget(QLabel("Equity Risk Premium (ERP):"), 2, 0)
        grid.addWidget(self.erp, 2, 1)
        grid.addWidget(QLabel("Pre-Tax Cost of Debt (Kd):"), 2, 2)
        grid.addWidget(self.cost_debt, 2, 3)

        grid.addWidget(QLabel("Corporate Tax Rate (T):"), 3, 0)
        grid.addWidget(self.tax_rate, 3, 1)
        grid.addWidget(QLabel("Terminal Growth (g):"), 3, 2)
        grid.addWidget(self.terminal_g, 3, 3)

        grid.addWidget(QLabel("Shares Outstanding:"), 4, 0)
        grid.addWidget(self.shares_out, 4, 1)
        grid.addWidget(QLabel("Expected Dividend (D1):"), 4, 2)
        grid.addWidget(self.d1_dividend, 4, 3)

        layout.addWidget(param_box)

        # Financial Statements Input Table
        sub_tabs = QTabWidget()
        
        self.bs_table = QTableWidget(12, 2)
        self.bs_table.setHorizontalHeaderLabels(["Year T (Current)", "Year T-1 (Prior)"])
        self.bs_items = [
            "Cash & Cash Equivalents", "Accounts Receivable", "Inventories", "Total Current Assets",
            "Net PPE & Non-Current Assets", "TOTAL ASSETS", "Accounts Payable", "Short-Term Debt",
            "Total Current Liabilities", "Long-Term Debt", "TOTAL LIABILITIES", "TOTAL SHAREHOLDERS EQUITY"
        ]
        self.bs_table.setVerticalHeaderLabels(self.bs_items)
        self.bs_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Pre-fill sample values for validation
        default_bs = [
            [50000000, 45000000], [120000000, 110000000], [180000000, 160000000], [350000000, 315000000],
            [650000000, 600000000], [1000000000, 915000000], [90000000, 85000000], [60000000, 50000000],
            [150000000, 135000000], [250000000, 220000000], [400000000, 355000000], [600000000, 560000000]
        ]
        for r in range(12):
            self.bs_table.setItem(r, 0, QTableWidgetItem(str(default_bs[r][0])))
            self.bs_table.setItem(r, 1, QTableWidgetItem(str(default_bs[r][1])))

        self.is_table = QTableWidget(7, 2)
        self.is_table.setHorizontalHeaderLabels(["Year T (Current)", "Year T-1 (Prior)"])
        self.is_items = [
            "Total Revenues (Sales)", "Cost of Goods Sold (COGS)", "Gross Profit",
            "Operating Income (EBIT)", "Interest Expense", "Earnings Before Tax (EBT)", "NET INCOME"
        ]
        self.is_table.setVerticalHeaderLabels(self.is_items)
        self.is_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        default_is = [
            [800000000, 720000000], [520000000, 470000000], [280000000, 250000000],
            [140000000, 125000000], [35000000, 30000000], [105000000, 95000000], [81375000, 73625000]
        ]
        for r in range(7):
            self.is_table.setItem(r, 0, QTableWidgetItem(str(default_is[r][0])))
            self.is_table.setItem(r, 1, QTableWidgetItem(str(default_is[r][1])))

        sub_tabs.addTab(self.bs_table, "Balance Sheet Data")
        sub_tabs.addTab(self.is_table, "Income Statement Data")
        layout.addWidget(sub_tabs)

    def init_distress_tab(self):
        layout = QVBoxLayout(self.tab_distress)
        self.distress_report = QTextEdit()
        self.distress_report.setFont(QFont("Consolas", 11))
        self.distress_report.setReadOnly(True)
        layout.addWidget(self.distress_report)

    def init_valuation_tab(self):
        layout = QVBoxLayout(self.tab_valuation)
        self.valuation_report = QTextEdit()
        self.valuation_report.setFont(QFont("Consolas", 11))
        self.valuation_report.setReadOnly(True)
        layout.addWidget(self.valuation_report)

    def init_sensitivity_tab(self):
        layout = QVBoxLayout(self.tab_sensitivity)
        self.sensitivity_report = QTextEdit()
        self.sensitivity_report.setFont(QFont("Consolas", 11))
        self.sensitivity_report.setReadOnly(True)
        layout.addWidget(self.sensitivity_report)

    def get_val(self, table, r, c):
        try:
            val = table.item(r, c).text()
            return float(val)
        except Exception:
            return 0.0

    def run_full_analysis(self):
        # Extract Inputs
        try:
            rf = float(self.rf_rate.text())
            beta = float(self.beta.text())
            erp = float(self.erp.text())
            kd = float(self.cost_debt.text())
            tax = float(self.tax_rate.text())
            shares = float(self.shares_out.text())
            g = float(self.terminal_g.text())
            d1 = float(self.d1_dividend.text())
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please verify numerical parameter values.")
            return

        # Balance Sheet Year T
        cash_t = self.get_val(self.bs_table, 0, 0)
        ar_t = self.get_val(self.bs_table, 1, 0)
        inv_t = self.get_val(self.bs_table, 2, 0)
        ca_t = self.get_val(self.bs_table, 3, 0)
        ppe_t = self.get_val(self.bs_table, 4, 0)
        assets_t = self.get_val(self.bs_table, 5, 0)
        ap_t = self.get_val(self.bs_table, 6, 0)
        st_debt_t = self.get_val(self.bs_table, 7, 0)
        cl_t = self.get_val(self.bs_table, 8, 0)
        lt_debt_t = self.get_val(self.bs_table, 9, 0)
        liab_t = self.get_val(self.bs_table, 10, 0)
        equity_t = self.get_val(self.bs_table, 11, 0)

        # Balance Sheet Year T-1
        assets_t1 = self.get_val(self.bs_table, 5, 1)
        cl_t1 = self.get_val(self.bs_table, 8, 1)
        ca_t1 = self.get_val(self.bs_table, 3, 1)

        # Income Statement
        rev_t = self.get_val(self.is_table, 0, 0)
        cogs_t = self.get_val(self.is_table, 1, 0)
        ebit_t = self.get_val(self.is_table, 3, 0)
        ebt_t = self.get_val(self.is_table, 5, 0)
        net_inc_t = self.get_val(self.is_table, 6, 0)
        
        rev_t1 = self.get_val(self.is_table, 0, 1)
        net_inc_t1 = self.get_val(self.is_table, 6, 1)

        if assets_t <= 0:
            QMessageBox.warning(self, "Data Error", "Total Assets must be strictly greater than zero.")
            return

        wc_t = ca_t - cl_t

        # ---------------------------------------------------------
        # 1. DISTRESS ENGINES COMPUTATION
        # ---------------------------------------------------------
        # Altman Z-Score (Manufacturing original)
        z1 = wc_t / assets_t
        z2 = (net_inc_t * 0.7) / assets_t # Approx retained earnings addition
        z3 = ebit_t / assets_t
        z4 = equity_t / liab_t if liab_t > 0 else 1.0
        z5 = rev_t / assets_t
        altman_z = 1.2 * z1 + 1.4 * z2 + 3.3 * z3 + 0.6 * z4 + 0.999 * z5

        # Springate Score
        springate_s = 1.03 * (wc_t / assets_t) + 3.07 * (ebit_t / assets_t) + 0.66 * (ebt_t / cl_t if cl_t > 0 else 0) + 0.4 * (rev_t / assets_t)

        # Zmijewski Probe
        zmij_k = -4.336 - 4.34 * (net_inc_t / assets_t) + 5.79 * (liab_t / assets_t) - 0.07 * (ca_t / cl_t if cl_t > 0 else 1)
        p_zmijewski = 1 / (1 + math.exp(-zmij_k))

        # Ohlson O-Score
        ohlson_k = (-1.32 - 0.407 * math.log(max(assets_t / 1000, 1)) + 6.03 * (liab_t / assets_t)
                    - 1.43 * (wc_t / assets_t) + 0.0757 * (cl_t / ca_t if ca_t > 0 else 1)
                    - 1.72 * (1.0 if liab_t > assets_t else 0.0) - 2.37 * (net_inc_t / assets_t)
                    - 1.83 * ((ebit_t) / liab_t if liab_t > 0 else 0))
        p_ohlson = 1 / (1 + math.exp(-ohlson_k))

        # Piotroski F-Score (9 Metrics)
        f_score = 0
        if net_inc_t > 0: f_score += 1
        if ebit_t > 0: f_score += 1
        roa_t = net_inc_t / assets_t
        roa_t1 = net_inc_t1 / assets_t1 if assets_t1 > 0 else 0
        if roa_t > roa_t1: f_score += 1
        if ebit_t > net_inc_t: f_score += 1 # Quality of earnings
        if (lt_debt_t / assets_t) < (self.get_val(self.bs_table, 9, 1) / assets_t1 if assets_t1 > 0 else 1): f_score += 1
        if (ca_t / cl_t if cl_t > 0 else 0) > (ca_t1 / cl_t1 if cl_t1 > 0 else 0): f_score += 1
        if (cogs_t / rev_t if rev_t > 0 else 1) < (self.get_val(self.is_table, 1, 1) / rev_t1 if rev_t1 > 0 else 1): f_score += 1
        if (rev_t / assets_t) > (rev_t1 / assets_t1 if assets_t1 > 0 else 0): f_score += 1

        distress_txt = f"""========================================================================================
                      FRCS V5 MULTI-MODEL FINANCIAL DISTRESS ANALYSIS
========================================================================================

1. ALTMAN Z-SCORE MODEL (Emerging/Industrial Standard)
   - Calculated Z-Score: {altman_z:.2f}
   - Zone Classification: {'SAFE ZONE (Low Default Risk)' if altman_z > 2.99 else ('GREY ZONE (Moderate Risk)' if altman_z > 1.81 else 'DISTRESS ZONE (High Bankruptcy Risk)')}

2. SPRINGATE S-SCORE MODEL
   - Calculated S-Score: {springate_s:.2f}
   - Solvent Threshold (> 0.862): {'SOLVENT' if springate_s > 0.862 else 'POTENTIAL DISTRESS'}

3. ZMIJEWSKI PROBIT MODEL
   - Default Probability: {p_zmijewski:.2%}
   - Financial Health: {'HEALTHY' if p_zmijewski < 0.50 else 'FINANCIALLY DISTRESSED'}

4. OHLSON O-SCORE MODEL
   - Default Probability: {p_ohlson:.2%}
   - Evaluation: {'LOW DEFAULT PROBABILITY' if p_ohlson < 0.50 else 'HIGH DEFAULT RISK'}

5. PIOTROSKI F-SCORE TREND INDEX
   - Total Score: {f_score} / 9
   - Health Status: {'STRONG FINANCIAL POSITION (7-9)' if f_score >= 7 else ('MODERATE POSITION (4-6)' if f_score >= 4 else 'WEAK FINANCIAL POSITION (0-3)')}
"""
        self.distress_report.setText(distress_txt)

        # ---------------------------------------------------------
        # 2. WACC & VALUATION ENGINE
        # ---------------------------------------------------------
        ke = rf + (beta * erp)
        after_tax_kd = kd * (1 - tax)
        total_debt = st_debt_t + lt_debt_t
        total_cap = equity_t + total_debt
        
        we = equity_t / total_cap if total_cap > 0 else 0.70
        wd = total_debt / total_cap if total_cap > 0 else 0.30
        wacc = (we * ke) + (wd * after_tax_kd)

        # FCFF & Valuation
        nopat = ebit_t * (1 - tax)
        capex_est = assets_t - assets_t1 + (ebit_t * 0.15)
        delta_wc = wc_t - (ca_t1 - cl_t1)
        fcff = nopat - capex_est - delta_wc

        # DCF Model
        disc_rate = wacc if wacc > g else ke + 0.02
        terminal_value = (fcff * (1 + g)) / (disc_rate - g) if disc_rate > g else 0
        enterprise_value = (fcff / (1 + disc_rate)) + (terminal_value / (1 + disc_rate))
        net_debt = total_debt - cash_t
        equity_val_dcf = enterprise_value - net_debt
        dcf_share_price = equity_val_dcf / shares if shares > 0 else 0

        # DDM Gordon Model
        ddm_share_price = d1 / (ke - g) if ke > g else 0

        # Multiples Valuation (P/E Basis)
        eps = net_inc_t / shares if shares > 0 else 0
        pe_multiple = 10.0 # Benchmark Sector P/E
        pe_share_price = eps * pe_multiple

        val_txt = f"""========================================================================================
                      FRCS V5 CAPITAL COST & MULTI-MODEL VALUATION
========================================================================================

[A] COST OF CAPITAL STRUCTURE (CAPM & WACC)
----------------------------------------------------------------------------------------
• Cost of Equity (Ke via CAPM): {ke:.2%}
• After-Tax Cost of Debt [Kd * (1-T)]: {after_tax_kd:.2%}
• Equity Weight (We): {we:.2%} | Debt Weight (Wd): {wd:.2%}
• Weighted Average Cost of Capital (WACC): {wacc:.2%}

[B] DISCOUNTED CASH FLOW (DCF) VALUATION
----------------------------------------------------------------------------------------
• Operating NOPAT: ${nopat:,.2f}
• Estimated Free Cash Flow to Firm (FCFF): ${fcff:,.2f}
• Terminal Enterprise Value: ${terminal_value:,.2f}
• Calculated Enterprise Value (EV): ${enterprise_value:,.2f}
• Net Debt (Total Debt - Cash): ${net_debt:,.2f}
• Fair Equity Value: ${equity_val_dcf:,.2f}
► DCF FAIR PRICE PER SHARE: ${dcf_share_price:,.2f}

[C] ALTERNATIVE VALUATION MODELS
----------------------------------------------------------------------------------------
• Dividend Discount Model (DDM / Gordon): ${ddm_share_price:,.2f} / Share
• P/E Multiples Valuation (Benchmark 10.0x): ${pe_share_price:,.2f} / Share
• Trailing Earnings Per Share (EPS): ${eps:,.2f}
"""
        self.valuation_report.setText(val_txt)

        # ---------------------------------------------------------
        # 3. SENSITIVITY MATRIX
        # ---------------------------------------------------------
        sens_txt = f"""========================================================================================
                      FRCS V5 STRESS TESTING & SENSITIVITY MATRIX
========================================================================================

DCF FAIR SHARE PRICE SENSITIVITY TO WACC AND TERMINAL GROWTH (g):

----------------------------------------------------------------------------------------
WACC \\ g         | g = {g-0.01:.1%}       | g = {g:.1%} (Base)     | g = {g+0.01:.1%}
----------------------------------------------------------------------------------------
WACC = {wacc-0.01:.1%}  | ${self.calc_sens_price(fcff, wacc-0.01, g-0.01, net_debt, shares):,.2f}         | ${self.calc_sens_price(fcff, wacc-0.01, g, net_debt, shares):,.2f}         | ${self.calc_sens_price(fcff, wacc-0.01, g+0.01, net_debt, shares):,.2f}
WACC = {wacc:.1%}  | ${self.calc_sens_price(fcff, wacc, g-0.01, net_debt, shares):,.2f}         | ${dcf_share_price:,.2f} (Base)    | ${self.calc_sens_price(fcff, wacc, g+0.01, net_debt, shares):,.2f}
WACC = {wacc+0.01:.1%}  | ${self.calc_sens_price(fcff, wacc+0.01, g-0.01, net_debt, shares):,.2f}         | ${self.calc_sens_price(fcff, wacc+0.01, g, net_debt, shares):,.2f}         | ${self.calc_sens_price(fcff, wacc+0.01, g+0.01, net_debt, shares):,.2f}
----------------------------------------------------------------------------------------
"""
        self.sensitivity_report.setText(sens_txt)
        
        QMessageBox.information(self, "Analysis Complete", "All Financial Engines Executed Successfully!")

    def calc_sens_price(self, fcff, w, g, net_debt, shares):
        if w <= g or shares <= 0:
            return 0.0
        tv = (fcff * (1 + g)) / (w - g)
        ev = (fcff / (1 + w)) + (tv / (1 + w))
        eq = ev - net_debt
        return max(eq / shares, 0.0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FRCSFullEngineSuite()
    win.show()
    sys.exit(app.exec())
