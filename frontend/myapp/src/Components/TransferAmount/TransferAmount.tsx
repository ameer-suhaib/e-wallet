import React, { useState } from 'react'
import './transferamount.css'
import SideBar from '../SideBar/SideBar'
import { useNavigate } from 'react-router-dom'
import axios from 'axios';

function TransferAmount() {
    const navigate = useNavigate();
    const [formData,setFormData] = useState({
        to_account_id : '',
        amount : ''
    })
    const handleChange = (e:any) => {
        const {name,value} = e.target;
        setFormData({
            ...formData,
            [name]:value
        })
    }
    const handleSubmit = async () => {
        const token = localStorage.getItem("token")
        try { 
            const amountInt = parseInt(formData.amount)
            const response = axios.post('http://localhost:8000/transfer_amount', {to_account_id:formData.to_account_id, amount: amountInt},{
                headers:{
                    Authorization:`Bearer ${token}`
                }
            })
            console.log(response);
            window.alert('transaction success')
            navigate('/account_details')
        }catch (err) {
            console.log(err,"errrrr");
            
        }
    }
  return (
    <div>
      <SideBar/>
      <div className="withrawcontainer">
        <form className="form-container" action="">
          <h2>Transfer amount</h2>
          <div className="form-group">
            <label className='col-form-label' htmlFor="">Account id: </label>
            <input className='form-control' onChange={handleChange} value={formData.to_account_id} name='to_account_id' type='number'></input>
          </div>
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

export default TransferAmount