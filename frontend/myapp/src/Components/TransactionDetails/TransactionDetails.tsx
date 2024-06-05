import React, { useEffect, useState } from 'react';
import axios from 'axios';
import SideBar from '../SideBar/SideBar';
import BasicDatePicker from '../DatePicker';
import './transactiondetails.css';

interface Transaction {
  id: string;
  to_account_id: string;
  transaction_type: string;
  timestamp: string;
  amount: number;
  description: string;
}

function TransactionDetails() {
  const [transactions, setTransactions] = useState<Transaction[] | null>(null);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [validDate, setValidDate] = useState<boolean>(true);

  useEffect(() => {
    if (selectedDate && validDate) {
      fetchTransaction(selectedDate);
    } else {
      setTransactions([]);
    }
  }, [selectedDate, validDate]);

  const fetchTransaction = async (start_date: string) => {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.post(
        'http://localhost:8000/get_transaction_detail',
        { start_date: start_date },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTransactions(response.data);
    } catch (err) {
      console.error('Error fetching transaction details:', err);
    }
  };

  const handleDateChange = (date: any) => {
    if (date) {
      setSelectedDate(date.format('YYYY-MM-DD'));
      setValidDate(true);
    } else {
      setSelectedDate(null);
      setValidDate(true);
    }
  };

  return (
    <div>
      <SideBar />
      <div className='transaction-container'>
        <BasicDatePicker onChange={handleDateChange} />
        <table>
          <thead>
            <tr>
              <th>To account ID</th>
              <th>Transaction type</th>
              <th>Time</th>
              <th>Amount</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {transactions === null ? (
              <tr>
                <td colSpan={5}>No transactions found</td>
              </tr>
            ) : (
              transactions.map((transaction) => (
                <tr key={transaction.id}>
                  <td>{transaction.to_account_id}</td>
                  <td>{transaction.transaction_type}</td>
                  <td>{transaction.timestamp}</td>
                  <td>{transaction.amount}</td>
                  <td>{transaction.description}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default TransactionDetails;
