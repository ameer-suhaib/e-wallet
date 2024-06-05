import React, { useState } from 'react'
import SideBar from '../SideBar/SideBar'
import { useNavigate } from 'react-router-dom'
import './deposit.css'
import axios from 'axios';
import { BASE_URL } from '../../URL/Base-url';

function Deposit() {
  const navigate = useNavigate();
  const [formData,setFormData] = useState({
    amount:''
  })
  
  const handleChange = (e:any) => {
    const {name,value} = e.target;
    setFormData({
      ...formData,
      [name]:value
    })
  }
  const handleSubmit =async () => {
    const token = localStorage.getItem("token")
    try{
      const amountInt = parseInt(formData.amount)
      const response = axios.post(`http://localhost:8000/deposit`,{...formData,amount:amountInt}, {
        headers : {
          Authorization : `Bearer ${token}`
        } 
      })
      window.alert('Deposte success')
      navigate('/account_details')
      console.log(response,"oooooo");
    } catch (err) {
      console.error("Failed",err)
    }
  }
  return (
    <div>
      <SideBar/>
      <div className="withrawcontainer">
        <form className="form-container" action="">
          <h2>Deposit</h2>
          <div className="form-group">
            <label className='col-form-label' htmlFor="">Amount</label>
            <input className='form-control' onChange={handleChange} value={formData.amount} name='amount' type='number'></input>
          </div>
          <div style={{gap:'10px'}} className="modal-footer">
            <button onClick={()=>navigate('/account_details')} type='button'>Close</button>
            <button onClick={handleSubmit} type='button'>Submit</button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Deposit