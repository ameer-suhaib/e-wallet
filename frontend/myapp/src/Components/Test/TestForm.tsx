import React, { useEffect, useState } from 'react'
import './testform.css'
import bank from '../Assets/pngwing.com.png'
import SideBar from '../SideBar/SideBar'
import { useNavigate } from "react-router-dom";
import axios from 'axios';

function TestForm() {
    const navigate = useNavigate();
    const [form,setForm] = useState({
        random_id : '',
        balance : 0
    })

    useEffect(()=>{
        const token = localStorage.getItem("token")
        const response = axios.get('http://localhost:8000/account_details', {
            headers:{
                Authorization:`Bearer ${token}`
            }
        }).then((response)=>{
            const data = response.data
            console.log(data,"dataaaaaaaaaaaaa");
            
            setForm({
                random_id : data.random_id,
                balance : data.balance
            })

        })
    },[])


  return (

    <div className=''>
        <SideBar/>
        <div className='accnt-container'>
            <div className="left-container">
                <img className='bank-icon' src={bank}></img>
            </div>
            <div className="right-container">
                <form action="">
                <h1><u>Account Details</u></h1>
                <p style={{fontSize:'20px', fontWeight:'500'}}>AccoutID : {form.random_id}</p>
                 <p style={{fontSize:'20px', fontWeight:'500'}}>Balance : ${form.balance}</p>
                 <div className="btn">
                        <button type="button" onClick={()=>navigate('/deposite')} className='deposite-btn'>Deposit</button>
                        <button type='button' onClick={()=>navigate('/withdraw')} className='deposite-btn'>Withdraw</button>
                    </div>
                    </form>
                </div>
            </div>
        </div>
  )
}

export default TestForm