import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function Chart({ data }) {
  return (
    <div style={{ width: '100%', height: 300 }}>
      <h3>Last 6 Months</h3>
      <ResponsiveContainer>
        <BarChart data={data}>
          <XAxis dataKey="month" />
          <YAxis tickFormatter={(v) => `$${v/1000}k`} />
          <Tooltip formatter={(v) => [`$${Number(v).toFixed(2)}`, '']} />
          <Legend />
          <Bar dataKey="credit" name="Income" fill="#4CAF50" />
          <Bar dataKey="debit" name="Expense" fill="#F44336" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
