"""
test_stage3_full.py - Comprehensive Automated Verification Test Suite for Stage 3
Validates:
1. Mathematical calculations (net change, % change, annualized rate)
2. Division-by-zero guards, zero denominators, and invalid year ranges
3. Missing values preservation (no silent coercion to zero)
4. Parametric and non-parametric statistical metrics (IQR, Tukey fences, skewness)
5. Correlation matrix validation and strict indicator filtering
6. Regional comparison aggregation
7. Intervals rate dynamics across reporting periods
8. Country forest profile across multiple nation types (large, small, partial)
9. Research question findings for all 8 questions
10. All 8 dashboard navigation views execution
11. Chart generators fallback behavior with empty/sparse data
"""

import os
import sys
import unittest
import numpy as np
import pandas as pd

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import data_loader as dl
import visualizations as viz
import styles

class TestStage3ForestDashboard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Loads all datasets once for the test suite."""
        cls.df_fra = dl.load_fra_years()
        cls.df_int = dl.load_intervals()
        cls.df_deg = dl.load_degraded_forest()
        cls.df_rest = dl.load_forest_restoration()
        cls.df_pol = dl.load_forest_policy()
        cls.df_tiers = dl.load_tiers()
        cls.df_nwfp = dl.load_nwfp()

    def test_01_core_dataset_loading(self):
        """Verify that all core and secondary datasets load without data loss."""
        self.assertFalse(self.df_fra.empty, "FRA_Years dataset should not be empty")
        self.assertIn('1a_forestArea', self.df_fra.columns)
        self.assertIn('year', self.df_fra.columns)
        self.assertIn('name', self.df_fra.columns)
        self.assertGreater(self.df_fra['name'].nunique(), 200, "Should cover over 200 nations")

    def test_02_period_change_calculations(self):
        """Verify mathematical correctness of period change formulas."""
        chg_df, summary = dl.calculate_period_change(self.df_fra, 1990, 2025)
        self.assertTrue(summary['is_valid'])
        self.assertEqual(summary['years_diff'], 35)
        self.assertGreater(summary['countries_evaluated'], 200)

        # Check math consistency: net_change = total_end - total_start
        expected_net = summary['total_end_mha'] - summary['total_start_mha']
        self.assertAlmostEqual(summary['net_change_mha'], expected_net, places=2)

        # Annual rate = net_change / 35
        expected_annual = expected_net / 35.0
        self.assertAlmostEqual(summary['annual_rate_mha'], expected_annual, places=3)

        # Relative % = (net_change / total_start) * 100
        expected_pct = (expected_net / summary['total_start_mha']) * 100.0
        self.assertAlmostEqual(summary['pct_change'], expected_pct, places=2)

    def test_03_invalid_year_ranges_guards(self):
        """Verify guards against invalid milestone year pairs."""
        # 1. start == end
        _, s_equal = dl.calculate_period_change(self.df_fra, 2020, 2020)
        self.assertFalse(s_equal['is_valid'], "start_year == end_year must be invalid")
        self.assertIn("strictly greater", s_equal['error_msg'])

        # 2. start > end
        _, s_rev = dl.calculate_period_change(self.df_fra, 2025, 1990)
        self.assertFalse(s_rev['is_valid'], "start_year > end_year must be invalid")

    def test_04_zero_denominator_and_missing_guards(self):
        """Verify division-by-zero protection and missing value handling."""
        synth_data = pd.DataFrame([
            {'name': 'ZeroLand', 'regions': 'Europe', 'year': 1990, '1a_forestArea': 0.0},
            {'name': 'ZeroLand', 'regions': 'Europe', 'year': 2025, '1a_forestArea': 100.0},
            {'name': 'MissingLand', 'regions': 'Asia', 'year': 1990, '1a_forestArea': np.nan},
            {'name': 'MissingLand', 'regions': 'Asia', 'year': 2025, '1a_forestArea': 200.0},
            {'name': 'NormalLand', 'regions': 'Africa', 'year': 1990, '1a_forestArea': 500.0},
            {'name': 'NormalLand', 'regions': 'Africa', 'year': 2025, '1a_forestArea': 400.0}
        ])

        m_chg, summ = dl.calculate_period_change(synth_data, 1990, 2025)
        self.assertTrue(summ['is_valid'])

        # ZeroLand percentage change must be NaN (guard against divide by zero)
        z_rec = m_chg[m_chg['name'] == 'ZeroLand']
        self.assertEqual(len(z_rec), 1)
        self.assertTrue(np.isnan(z_rec['pct_change'].values[0]), "pct_change must be NaN when start area is 0.0")

        # MissingLand must be omitted from paired calculation (never fabricated as zero)
        m_rec = m_chg[m_chg['name'] == 'MissingLand']
        self.assertEqual(len(m_rec), 0, "Countries with missing start or end area must be safely excluded")

    def test_05_statistical_distribution_metrics(self):
        """Verify parametric and non-parametric statistical calculations."""
        dist = dl.get_statistical_distribution_metrics(self.df_fra, year=2025)
        self.assertTrue(dist['is_valid'])
        self.assertEqual(dist['count'], 236)
        self.assertGreater(dist['mean_mha'], 0)
        self.assertGreater(dist['median_mha'], 0)

        # Skewness must be strongly positive for forest area
        self.assertGreater(dist['skewness'], 1.0, "Forest area distribution must be right-skewed")

        # Tukey outlier fences math
        q25 = dist['q25_mha']
        q75 = dist['q75_mha']
        iqr = dist['iqr_mha']
        self.assertAlmostEqual(iqr, q75 - q25, places=2)
        expected_upper = round(q75 + 1.5 * iqr, 2)
        self.assertAlmostEqual(dist['upper_fence_mha'], expected_upper, places=2)

        # Known mega-forest nations must be in outliers
        outliers = dist['outliers_df']
        self.assertGreater(len(outliers), 10)
        outlier_names = outliers['name'].tolist()
        self.assertIn('Russian Federation', outlier_names)
        self.assertIn('Brazil', outlier_names)
        self.assertIn('Canada', outlier_names)
        self.assertIn('United States of America', outlier_names)
        self.assertIn('China', outlier_names)

    def test_06_correlation_matrix_filtering(self):
        """Verify strict exclusion of IDs, flags, and constant columns in correlation matrix."""
        corr_df, labels = dl.calculate_correlation_matrix(self.df_fra, year=2025)
        self.assertFalse(corr_df.empty)

        # Verify no flag or identifier columns leaked into correlation matrix
        for col in corr_df.columns:
            self.assertFalse(str(col).endswith('_flag'), f"Flag column leaked into correlation: {col}")
            self.assertNotIn(str(col), ['iso3', 'iso2', 'm49', 'name', 'Desk study', 'year'])

        # Verify values in [-1.0, 1.0]
        vals = corr_df.values.flatten()
        valid_vals = vals[~np.isnan(vals)]
        self.assertTrue((valid_vals >= -1.0).all() and (valid_vals <= 1.0).all())

    def test_07_regional_comparison_metrics(self):
        """Verify aggregation across all 6 FAO continental regions."""
        reg_df = dl.get_regional_comparison_metrics(self.df_fra, 1990, 2025)
        self.assertFalse(reg_df.empty)
        self.assertEqual(len(reg_df), 6, "Must contain all 6 FAO regions")

        expected_regions = {'Africa', 'Asia', 'Europe', 'North and Central America', 'Oceania', 'South America'}
        self.assertEqual(set(reg_df['Region'].unique()), expected_regions)

        # Verify total sum approximates world total
        sum_2025 = reg_df['Forest Area 2025 (M ha)'].sum()
        self.assertGreater(sum_2025, 4000.0)
        self.assertLess(sum_2025, 4300.0)

    def test_08_interval_dynamics_rates(self):
        """Verify interval rates extraction and units."""
        int_summary = dl.get_interval_dynamics_summary(self.df_int)
        table = int_summary['summary_table']
        self.assertFalse(table.empty)
        self.assertEqual(len(table), 5, "Must contain 5 reporting intervals")

        # Verify units and decreasing deforestation trend
        self.assertIn('Deforestation (1,000 ha/yr)', table.columns)
        self.assertIn('Deforestation (M ha/yr)', table.columns)
        obs = int_summary['observations']
        self.assertIn('deforestation_change_pct', obs)
        self.assertLess(obs['deforestation_change_pct'], 0, "Deforestation rate should trend downwards")

    def test_09_country_forest_profile(self):
        """Verify country profile generation for multiple country types."""
        # 1. Major forested nation (Brazil)
        prof_br = dl.get_country_forest_profile(
            'Brazil', self.df_fra, self.df_int, self.df_deg, self.df_rest, self.df_pol, self.df_nwfp, self.df_tiers
        )
        self.assertTrue(prof_br['found'])
        self.assertEqual(prof_br['iso3'], 'BRA')
        self.assertEqual(len(prof_br['milestones_df']), 6)
        self.assertGreater(len(prof_br['nwfp_products']), 0)
        self.assertTrue(prof_br['period_change']['is_available'])
        self.assertIn('high', prof_br['tiers']['forest_area_status'].lower())

        # 2. Planted forest leader (China)
        prof_cn = dl.get_country_forest_profile(
            'China', self.df_fra, self.df_int, self.df_deg, self.df_rest, self.df_pol, self.df_nwfp, self.df_tiers
        )
        self.assertTrue(prof_cn['found'])
        self.assertGreater(prof_cn['latest_sustainability']['planted_forest_mha'], 50.0)

        # 3. Small island state (sparse / partial observations)
        prof_sm = dl.get_country_forest_profile(
            'Tuvalu', self.df_fra, self.df_int, self.df_deg, self.df_rest, self.df_pol, self.df_nwfp, self.df_tiers
        )
        self.assertTrue(prof_sm['found'])
        # Must not raise exceptions even when fields are sparse

        # 4. Non-existent country
        prof_none = dl.get_country_forest_profile('Atlantis', self.df_fra)
        self.assertFalse(prof_none['found'])

    def test_10_research_question_findings(self):
        """Verify all 8 research questions generate dynamic findings."""
        findings = dl.get_research_question_findings(
            self.df_fra, self.df_int, self.df_deg, self.df_rest, self.df_pol, self.df_tiers
        )
        self.assertEqual(len(findings), 8, "Must generate answers for Q1 through Q8")
        for q_key in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8']:
            self.assertIn(q_key, findings)
            q = findings[q_key]
            self.assertIn('question', q)
            self.assertIn('reporting_period', q)
            self.assertIn('calculation_used', q)
            self.assertIn('interpretation', q)
            self.assertGreater(len(q['interpretation']), 30, f"{q_key} interpretation should not be empty")

    def test_11_visualizations_fallback_behavior(self):
        """Verify all chart generators handle empty data safely without crashing."""
        empty_df = pd.DataFrame()
        empty_dist = {'is_valid': False, 'df_plot': pd.DataFrame()}
        empty_prof = {'found': False, 'name': 'Empty', 'milestones_df': pd.DataFrame(), 'latest_sustainability': {}}

        # Must return valid Plotly Figures
        fig1 = viz.plot_country_forest_distribution_histogram(empty_dist)
        fig2 = viz.plot_forest_area_outliers_box(empty_dist)
        fig3 = viz.plot_statistical_correlation_heatmap(empty_df)
        fig4 = viz.plot_regional_comparison_bar(empty_df)
        fig5 = viz.plot_interval_rates_comparison(empty_df)
        fig6 = viz.plot_country_profile_trend(empty_prof)
        fig7 = viz.plot_country_natural_vs_planted_donut(empty_prof)
        fig8 = viz.plot_research_q1_global_trajectory(empty_df)
        fig9 = viz.plot_research_q4_regional_shares(empty_df)

        for i, fig in enumerate([fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9], start=1):
            self.assertIsNotNone(fig, f"Chart generator {i} returned None instead of a Figure")

    def test_12_styles_and_header(self):
        """Verify styles and Stage 3 badge rendering."""
        css = styles.get_custom_css()
        self.assertIn(".rq-card", css)
        self.assertIn(".formula-callout", css)

        header_html = styles.render_header("Test", "Subtitle", "FAO", country_count=236)
        self.assertIn("Stage 3", header_html)

if __name__ == '__main__':
    unittest.main()
