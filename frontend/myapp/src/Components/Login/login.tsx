import React, { useState } from 'react'
import './login.css'
import email_icon from '../Assets/email.png'
import passwor_icon from '../Assets/password.png'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function Register() {

    const navigate = useNavigate();
    const [formData,setFormData] = useState({
        email : "",
        password : ""
    })
    const handleChange = (e:any) => {
        const {name,value} = e.target;
        setFormData({
            ...formData,
            [name]:value
        })
    }
    const handleSubmit = async ()=> {
        try{
            const response = await axios.post('http://localhost:8000/login',formData);
            const token = response.data.access_token
            localStorage.setItem("token",token)
            window.alert('Login sucesss')
            navigate('/account_details')
        } catch (err) {
            console.error(err);
        };
    }
    
  return (
    <div className="main-container">
        <div className="container">
            <div className="header">
                <div className="text">Login</div>
                <div className="underline"></div>
            </div>
            <div className="inputs">
                <div className="input">
                    <img src={email_icon} alt="" />
                    <input className='login-input' onChange={handleChange} name="email" value={formData.email} type="email" placeholder='EmailID' />
                </div>
                <div className="input">
                    <img src={passwor_icon} alt="" />
                    <input className='login-input' value={formData.password} onChange={handleChange} name="password" type="password" placeholder='Enter password' />
                </div>
            </div>
            <div className="forget-password">
                <p>"Don't have an account? "</p><span onClick={()=>navigate('/register')}>Register</span></div>
            <div className="submit-container">
                <div className="submit-btn" onClick={handleSubmit}>Login</div>
            </div>
        </div>
    </div>
)
}

export default Register
