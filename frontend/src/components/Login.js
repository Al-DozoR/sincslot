import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Auth.css';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Вход:', formData);
    // Здесь будет логика входа
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>Вход в SyncSlot</h2>
          <p>Войдите в свой аккаунт</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email или телефон</label>
            <input
              type="text"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="example@mail.ru или +7 XXX XXX XX XX"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Введите ваш пароль"
              required
            />
          </div>

          <button type="submit" className="btn btn-primary btn-full">
            Войти
          </button>

          <div className="auth-links">
            <Link to="/forgot-password" className="auth-link">
                Восстановить пароль
            </Link>
            <span className="auth-divider">|</span>
            <Link to="/register" className="auth-link">
                Зарегистрироваться
            </Link>
        </div>
        </form>
      </div>
    </div>
  );
};

export default Login;