// src/Login.js
import React, { useState } from 'react';
import './App.css';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const secretKey = 'A1B2C3D4E5'; // 固定密钥

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === secretKey) {
      navigate('/main');
    } else {
      alert('密码错误');
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="输入密钥"
        />
        <button type="submit">提交</button>
      </form>
    </div>
  );
};

export default Login;
