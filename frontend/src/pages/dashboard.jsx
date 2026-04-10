import { useState, useEffect } from 'react';
import AccountSwitcher from '../components/account-switcher.jsx';
import DashboardStats from '../components/dashboard-stats.jsx';
import Chart from '../components/chart.jsx';
import { getDashboardStats, getAccounts } from '../services/api.js';
import { useAccount } from '../context/AccountContext.jsx';

export default function DashboardPage() {
  const { selectedAccountId, setSelectedAccountId } = useAccount();
  const [stats, setStats] = useState(null);
  const [allAccounts, setAllAccounts] = useState([]);
  const [chartData, setChartData] = useState([]);

  // Load accounts for switcher
  useEffect(() => {
    async function loadAccounts() {
      try {
        const accounts = await getAccounts();
        setAllAccounts(accounts);
      } catch (err) {
        console.error(err);
      }
    }
    loadAccounts();
  }, []);

  // Load dashboard stats for current month
  useEffect(() => {
    const now = new Date();
    const month = now.getMonth() + 1;
    const year = now.getFullYear();
    async function loadStats() {
      try {
        const params = { month, year };
        if (selectedAccountId) params.account_id = selectedAccountId;
        const data = await getDashboardStats(params);
        setStats(data);
      } catch (err) {
        console.error(err);
      }
    }
    loadStats();
  }, [selectedAccountId]);

  // Load last 6 months data for chart (simple: loop months)
  useEffect(() => {
    async function loadChartData() {
      try {
        const months = [];
        const now = new Date();
        for (let i = 5; i >= 0; i--) {
          const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
          months.push({ month: d.getMonth() + 1, year: d.getFullYear() });
        }
        // For each month, fetch stats
        const promises = months.map(m => getDashboardStats({ month: m.month, year: m.year, account_id: selectedAccountId }));
        const results = await Promise.all(promises);
        const data = results.map((res, idx) => ({
          month: `${months[idx].year}-${String(months[idx].month).padStart(2, '0')}`,
          credit: res.credit_total,
          debit: res.debit_total
        }));
        setChartData(data);
      } catch (err) {
        console.error(err);
      }
    }
    loadChartData();
  }, [selectedAccountId]);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Dashboard</h1>
      <AccountSwitcher accounts={allAccounts} selectedAccountId={selectedAccountId} onSelect={setSelectedAccountId} />
      {stats && <DashboardStats stats={stats} />}
      {chartData.length > 0 && <Chart data={chartData} />}
    </div>
  );
}
