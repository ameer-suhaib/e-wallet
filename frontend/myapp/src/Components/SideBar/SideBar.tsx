import React, { useState } from 'react'
import './sidebar.css';
import { useNavigate } from 'react-router-dom';


function SideBar() {
    const navigate = useNavigate();

    const handleLogout = () => {
      localStorage.clear()
      navigate('/')
    }

  return (
    <div className="sidebar">
        <div className="menu">
            <a onClick={()=>navigate('/account_details')} href=''>Dashboard</a>
            <a onClick={()=>navigate('/deposite')} href=''>Deposit</a>
            <a onClick={()=>navigate('/withdraw')} href=''>Withdraw</a>
            <a onClick={()=>navigate('/transfer_amount')} href=''>Transfer Amount</a>
            <a onClick={()=>navigate('/transactions')} href=''>Transactions Details</a>
            <a onClick={handleLogout} href=''>Logout</a>
        </div>
    </div>
  )
}

export default SideBar