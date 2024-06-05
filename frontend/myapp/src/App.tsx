import React from 'react';
import './App.css';
import { BrowserRouter, Routes,Route  } from "react-router-dom";
import LoginSignUp from './Components/LoginSignup/LoginSignUp';
import TestForm from './Components/Test/TestForm';
import Deposit from './Components/Deposit/Deposit';
import Withdraw from './Components/Withdraw/Withdraw';
import Login from './Components/Login/login';
import TransactionDetails from './Components/TransactionDetails/TransactionDetails';
import TransferAmount from './Components/TransferAmount/TransferAmount';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Login/>}/>
        <Route path='/register' element={<LoginSignUp/>}/>
        <Route path='/transactions' element={<TransactionDetails/>}/>
        <Route path='/account_details' element={<TestForm/>}/>
        <Route path='/deposite' element={<Deposit/>}/>
        <Route path='/withdraw' element={<Withdraw/>}/>
        <Route path='/transfer_amount' element={<TransferAmount/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
