import React, { useState } from 'react'
import SideBar from '../SideBar/SideBar'
import './withdraw.css'
import { useNavigate } from 'react-router-dom'
import axios from 'axios';

function Withdraw() {
  const navigate = useNavigate();
  const [amount, setAmount] = useState('')
  
  const handlewithDraw =async () => {
    const token = localStorage.getItem("token")
    const amountInt = parseInt(amount)
    try {
      await axios.post('http://localhost:8000/withdraw',{amount : amountInt},{
        headers:{
          Authorization:`Bearer ${token}`
        }
      })
      navigate('/account_details')
      
    } catch (err) {
      console.error("Failed", err)
    }
  }
  return (
    <div>
      <SideBar/>
      <div className="withrawcontainer">
        <form className="form-container" onSubmit={(e)=>{
          e.preventDefault();
          handlewithDraw()
        }} 
        action="">
          <h2>Withdraw</h2>
          <div className="form-group">
            <label className='col-form-label' htmlFor="">Amount</label>
            <input className='form-control' onChange={(e)=>setAmount(e.target.value)} value={amount} name="amount" type='number'></input>
          </div>
          <div style={{gap:'10px'}} className="modal-footer">
            <button onClick={()=>navigate('/account_details')} type='button'>Close</button>
            <button type='submit'>Withdraw</button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Withdraw