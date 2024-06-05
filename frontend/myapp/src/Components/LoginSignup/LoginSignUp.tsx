import React, { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom';
import './loginsignup.css'
import axios from "axios";
import person_icon from '../Assets/person.png'
import email_icon from '../Assets/email.png'
import passwor_icon from '../Assets/password.png'



function LoginSignUp() {

    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: "",
        phone: "",
        email: "",
        password: ""
    })
    const handleChange = (e: any) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };
    const handleSubmit = async () => {
        try {
            const response = await axios.post('http://localhost:8000/signup', formData);
            console.log(response.data);
            window.alert('registerd success')
            navigate('/')
        }
        catch (err) {
            console.error(err);
            window.alert('An error occure please try again later')

        }
    };
    // const setAuthToken = (token:any) => {
    //     if (token) {
    //         axios.defaults.headers.common['Authorization'] = `Bearere ${token}`
    //     } else {
    //         delete axios.defaults.headers.common['Authorization']
    //     }
    // }

    return (
        <div className="main-container">
            <div className="container">
                <div className="header">
                    <div className="text">Signup</div>
                </div>
                <div className="inputs">
                    <div className="input">
                        <img src={person_icon} alt="" />
                        <input className='login-input' type="text" onChange={handleChange} name="username" placeholder='Enter username' />
                    </div>
                    <div className='input'>
                        <img />
                        <input placeholder='Enter phone number' onChange={handleChange} name="phone" className='login-input' />
                    </div>
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
                    <p> Already have an account? </p><span onClick={()=>navigate('/')}>Login</span></div>
                <div className="submit-container">
                    <div className="submit-btn" onClick={handleSubmit}> Signup</div>
                </div>
            </div>
        </div>
    )
}

export default LoginSignUp