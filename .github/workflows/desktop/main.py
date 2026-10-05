import sys
import math
import traceback

def show_error_and_exit(exc_type, exc_value, exc_tb):
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(None, "FRCS V5 Startup Error", f"Runtime Error:\n\n{error_msg}")
    except Exception:
        print(error_msg)
    sys.exit(1)

sys.excepthook = show_error_and_exit

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, 
    QPushButton, QHBoxLayout, QFrame, QDialog, QFormLayout, 
    QLineEdit, QMessageBox, QGroupBox, QScrollArea, QTabWidget,
    QComboBox, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit
)
from PySide6.QtCore import Qt

class MasterFRCSDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FRCS V5 - Comprehensive Multi-Model Financial & Valuation Suite")
        self.resize(1020, 820)
        layout = QVBoxLayout(self)

        setup_group = QGroupBox("1. Corporate Setup & Valuation Parameters")
        setup_grid = QGridLayout(setup_group)
        
        self.sector_combo = QComboBox()
        self.sector_combo.addItems([
            "Manufacturing & Industrial", 
            "Real Estate & Construction", 
            "Retail & Wholesale", 
            "Commercial Services", 
            "Healthcare & Pharma"
        ])
        
        self.scenario_combo = QComboBox()
        self.scenario_combo.addItems([
            "Base Case (Standard)",
            "Revenue Shock (-15%)",
            "Interest Rate Hike (+300 bps)",
            "Combined Severe Stress (-25% Sales, +10% COGS)"
        ])

        self.rf_input = QLineEdit("0.12")
        self.beta_input = QLineEdit("1.10")
        self.erp_input = QLineEdit("0.08")
        self.shares_input = QLineEdit("1000000")
        self.growth_input = QLineEdit("0.03")
        self.tax_rate_input = QLineEdit("0.225")
        self.cost_debt_input = QLineEdit("0.14")
        self.dividend_input = QLineEdit("2.50")

        setup_grid.addWidget(QLabel("Industry Sector:"), 0, 0)
        setup_grid.addWidget(self.sector_combo, 0, 1)
        setup_grid.addWidget(QLabel("Stress Scenario:"), 0, 2)
        setup_grid.addWidget(self.scenario_combo, 0, 3)
        
        setup_grid.addWidget(QLabel("Risk Free Rate (Rf):"), 1, 0)
        setup_grid.addWidget(self.rf_input, 1, 1)
        setup_grid.addWidget(QLabel("Equity Beta:"), 1, 2)
        setup_grid.addWidget(self.beta_input, 1, 3)

        setup_grid.addWidget(QLabel("Equity Risk Premium:"), 2, 0)
        setup_grid.addWidget(self.erp_input, 2, 1)
        setup_grid.addWidget(QLabel("Terminal Growth Rate (g):"), 2, 2)
        setup_grid.addWidget(self.growth_input, 2, 3)

        setup_grid.addWidget(QLabel("Pre-Tax Cost of Debt (Kd):"), 3, 0)
        setup_grid.addWidget(self.cost_debt_input, 3, 1)
        setup_grid.addWidget(QLabel("Corporate Tax Rate:"), 3, 2)
        setup_grid.addWidget(self.tax_rate_input, 3, 3)

        setup_grid.addWidget(QLabel("Total Shares Outstanding:"), 4, 0)
        setup_grid.addWidget(self.shares_input, 4, 1)
        setup_grid.addWidget(QLabel("Expected Dividend Per Share (D1):"), 4, 2)
        setup_grid.addWidget(self.dividend_input, 4, 3)

        layout.addWidget(setup_group)

        tabs = QTabWidget()
        
        def create_year_table(items):
            table = QTableWidget(len(items), 2)
            table.setHorizontalHeaderLabels(["Current Year (T)", "Prior Year (T-1)"])
            table.setVerticalHeaderLabels([item[1] for item in items])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for row in range(len(items)):
                table.setItem(row, 0, QTableWidgetItem("0.00"))
                table.setItem(row, 1, QTableWidgetItem("0.00"))
            return table

        self.bs_fields = [
            ("cash", "Cash & Cash Equivalents"),
            ("receivables", "Accounts Receivable"),
            ("inventory", "Inventory"),
            ("total_ca", "Total Current Assets"),
            ("ppe", "Net PPE"),
            ("total_assets", "TOTAL ASSETS"),
            ("st_debt", "Short-Term Debt"),
            ("payables", "Accounts Payable"),
            ("total_cl", "Total Current Liabilities"),
            ("lt_debt", "Long-Term Debt"),
            ("total_liabilities", "TOTAL LIABILITIES"),
            ("retained_earnings", "Retained Earnings"),
            ("total_equity", "TOTAL SHAREHOLDERS EQUITY")
        ]
        self.bs_table = create_year_table(self.bs_fields)
        tabs.addTab(self.bs_table, "Balance Sheet (2 Years)")

        self.is_fields = [
            ("revenue", "Total Revenues"),
            ("cogs", "Cost of Goods Sold (COGS)"),
            ("ebit", "Operating Income (EBIT)"),
            ("interest_exp", "Interest Expense"),
            ("ebt", "Earnings Before Tax (EBT)"),
            ("tax_exp", "Income Tax Expense"),
            ("net_income", "NET INCOME")
        ]
        self.is_table = create_year_table(self.is_fields)
        tabs.addTab(self.is_table, "Income Statement (2 Years)")

        self.cf_fields = [
            ("ocf", "Operating Cash Flow (OCF)"),
            ("capex", "CAPEX"),
            ("fcff", "Free Cash Flow to Firm (FCFF)")
        ]
        self.cf_table = create_year_table(self.cf_fields)
        tabs.addTab(self.cf_table, "Cash Flow (2 Years)")

        layout.addWidget(tabs)

        btn_box = QHBoxLayout()
        run_btn = QPushButton("Execute Complete Multi-Model Advisory Suite")
        run_btn.setStyleSheet("background-color: #059669; color: white; padding: 14px; font-weight: bold; border-radius: 6px;")
        run_btn.clicked.connect(self.run_all_engines)
        btn_box.addWidget(run_btn)
        layout.addLayout(btn_box)

    def get_cell_val(self, table, row, col):
        try:
            item = table.item(row, col)
            return float(item.text()) if item else 0.0
        except ValueError:
            return 0.0

    def run_all_engines(self):
        assets_t = self.get_cell_val(self.bs_table, 5, 0)
        liab_t = self.get_cell_val(self.bs_table, 10, 0)
        equity_t = self.get_cell_val(self.bs_table, 12, 0)
        re_t = self.get_cell_val(self.bs_table, 11, 0)
        ca_t = self.get_cell_val(self.bs_table, 3, 0)
        cl_t = self.get_cell_val(self.bs_table, 8, 0)
        st_debt_t = self.get_cell_val(self.bs_table, 6, 0)
        lt_debt_t = self.get_cell_val(self.bs_table, 9, 0)
        cash_t = self.get_cell_val(self.bs_table, 0, 0)

        rev_t = self.get_cell_val(self.is_table, 0, 0)
        ebit_t = self.get_cell_val(self.is_table, 2, 0)
        ebt_t = self.get_cell_val(self.is_table, 4, 0)
        net_inc_t = self.get_cell_val(self.is_table, 6, 0)

        ocf_t = self.get_cell_val(self.cf_table, 0, 0)
        fcff_t = self.get_cell_val(self.cf_table, 2, 0)

        assets_t1 = self.get_cell_val(self.bs_table, 5, 1)
        net_inc_t1 = self.get_cell_val(self.is_table, 6, 1)

        if assets_t <= 0:
            QMessageBox.warning(self, "Input Error", "Total Assets must be greater than zero.")
            return

        # 1. Financial Distress Engines
        wc_t = ca_t - cl_t

        x1 = wc_t / assets_t
        x2 = re_t / assets_t
        x3 = ebit_t / assets_t
        x4 = equity_t / liab_t if liab_t > 0 else 1.0
        x5 = rev_t / assets_t
        z_score = round(1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 0.999 * x5, 2)

        s_a = wc_t / assets_t
        s_b = ebit_t / assets_t
        s_c = ebt_t / cl_t if cl_t > 0 else 0
        s_d = rev_t / assets_t
        s_score = round(1.03 * s_a + 3.07 * s_b + 0.66 * s_c + 0.4 * s_d, 2)

        x_a = net_inc_t / assets_t
        x_b = liab_t / assets_t
        x_c = ca_t / cl_t if cl_t > 0 else 1.0
        x_score = -4.336 - (4.34 * x_a) + (5.79 * x_b) - (0.07 * x_c)
        p_zmijewski = round(1 / (1 + math.exp(-x_score)), 4)

        # Ohlson O-Score
        gNP = 0.03 
        l_ohlson = (-1.32 - 0.407 * math.log(max(assets_t, 1)) + 6.03 * (liab_t / assets_t)
                    - 1.43 * (wc_t / assets_t) + 0.0757 * (cl_t / ca_t if ca_t > 0 else 1)
                    - 1.72 * (1.0 if liab_t > assets_t else 0.0) - 2.37 * (net_inc_t / assets_t)
                    - 1.83 * (ocf_t / liab_t if liab_t > 0 else 0)
                    + 0.285 * (1.0 if (net_inc_t < 0 and net_inc_t1 < 0) else 0.0)
                    - 0.521 * ((net_inc_t - net_inc_t1) / (abs(net_inc_t) + abs(net_inc_t1)) if (abs(net_inc_t) + abs(net_inc_t1)) > 0 else 0))
        p_ohlson = round(1 / (1 + math.exp(-l_ohlson)), 4)

        # 2. Trend & Health (Piotroski)
        f_score = 0
        if net_inc_t > 0: f_score += 1
        if ocf_t > 0: f_score += 1
        roa_t = net_inc_t / assets_t
        roa_t1 = net_inc_t1 / assets_t1 if assets_t1 > 0 else 0
        if roa_t > roa_t1: f_score += 1
        if ocf_t > net_inc_t: f_score += 1

        # 3. Valuation & Cost of Capital Engines
        rf = float(self.rf_input.text() or 0.12)
        beta = float(self.beta_input.text() or 1.1)
        erp = float(self.erp_input.text() or 0.08)
        ke = rf + (beta * erp)
        
        kd = float(self.cost_debt_input.text() or 0.14)
        tax = float(self.tax_rate_input.text() or 0.225)
        after_tax_kd = kd * (1 - tax)

        total_debt_t = st_debt_t + lt_debt_t
        total_cap = equity_t + total_debt_t
        we = equity_t / total_cap if total_cap > 0 else 0.7
        wd = total_debt_t / total_cap if total_cap > 0 else 0.3

        wacc = (we * ke) + (wd * after_tax_kd)

        g = float(self.growth_input.text() or 0.03)
        shares = float(self.shares_input.text() or 1000000)
        d1 = float(self.dividend_input.text() or 2.50)

        # Gordon Growth Model (DDM)
        ddm_price = d1 / (ke - g) if ke > g else 0.0

        # DCF Model
        discount_rate = wacc if wacc > g else ke
        terminal_val = (fcff_t * (1 + g)) / (discount_rate - g) if discount_rate > g else 0
        enterprise_val = (fcff_t / (1 + discount_rate)) + (terminal_val / (1 + discount_rate))
        equity_val = enterprise_val + cash_t - total_debt_t
        fair_price_dcf = equity_val / shares if shares > 0 else 0

        res_dialog = QDialog(self)
        res_dialog.setWindowTitle("FRCS V5 - Executive Multi-Model Advisory Report")
        res_dialog.resize(780, 680)
        res_layout = QVBoxLayout(res_dialog)

        text_report = QTextEdit()
        text_report.setReadOnly(True)
        
        report_content = f"""==================================================
FRCS V5 MASTER FINANCIAL & VALUATION REPORT
==================================================

[1] FINANCIAL DISTRESS & RISK PREDICTION ENGINES
--------------------------------------------------
• Altman Z-Score: {z_score} -> ({'Safe Zone' if z_score > 2.99 else 'Grey/Distress Zone'})
• Springate S-Score: {s_score} -> ({'Solvent' if s_score > 0.862 else 'Distress Risk'})
• Zmijewski Distress Probability: {p_zmijewski:.2%}
• Ohlson O-Score Probability: {p_ohlson:.2%} -> ({'High Default Risk' if p_ohlson > 0.5 else 'Healthy'})

[2] FINANCIAL HEALTH & TREND ENGINES
--------------------------------------------------
• Piotroski F-Score (Trend Indicator): {f_score} / 9
• Current Net Working Capital: {wc_t:,.2f}
• ROA Trend: Current {roa_t:.2%} vs Prior {roa_t1:.2%}

[3] COST OF CAPITAL ENGINES
--------------------------------------------------
• Cost of Equity (Ke via CAPM): {ke:.2%}
• After-Tax Cost of Debt (Kd * (1-T)): {after_tax_kd:.2%}
• Weighted Average Cost of Capital (WACC): {wacc:.2%}

[4] CORPORATE VALUATION ENGINES
--------------------------------------------------
• Dividend Discount Model (DDM / Gordon Growth): ${ddm_price:,.2f} / Share
• Enterprise Value (EV via DCF): ${enterprise_val:,.2f}
• Net Debt Adjustment: ${total_debt_t - cash_t:,.2f}
• Total Equity Value: ${equity_val:,.2f}
• DCF Fair Value Per Share: ${fair_price_dcf:,.2f}

==================================================
"""
        text_report.setText(report_content)
        res_layout.addWidget(text_report)

        close_btn = QPushButton("Close Report")
        close_btn.clicked.connect(res_dialog.accept)
        res_layout.addWidget(close_btn)

        res_dialog.exec()

class FRCSMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financial Risk & Consulting System - FRCS V5")
        self.resize(900, 600)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        header = QFrame()
        header.setStyleSheet("background-color: #1E3A8A; border-radius: 8px; padding: 25px;")
        h_layout = QVBoxLayout(header)
        title = QLabel("FRCS V5 - Master Financial Advisory Platform")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        sub = QLabel("Multi-Model Financial Statement Analysis & Corporate Valuation System")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #93C5FD; font-size: 15px;")
        h_layout.addWidget(title)
        h_layout.addWidget(sub)
        layout.addWidget(header)

        desc = QLabel("Enter Year T and Year T-1 raw financial statements to run multi-model distress scoring and DCF valuation.")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("font-size: 15px; color: #374151; margin-top: 40px;")
        layout.addWidget(desc)

        btn_box = QHBoxLayout()
        btn_start = QPushButton("Open Multi-Year Financial Inputs & Valuation Suite")
        btn_start.setStyleSheet("background-color: #059669; color: white; padding: 15px 30px; font-size: 16px; font-weight: bold; border-radius: 6px;")
        btn_start.clicked.connect(self.open_dialog)

        btn_exit = QPushButton("Exit")
        btn_exit.setStyleSheet("background-color: #DC2626; color: white; padding: 15px 30px; font-size: 16px; font-weight: bold; border-radius: 6px;")
        btn_exit.clicked.connect(self.close)

        btn_box.addWidget(btn_exit)
        btn_box.addWidget(btn_start)
        layout.addLayout(btn_box)

    def open_dialog(self):
        d = MasterFRCSDialog(self)
        d.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FRCSMainWindow()
    win.show()
    sys.exit(app.exec())
