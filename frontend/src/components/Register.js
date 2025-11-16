import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Auth.css';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      alert('Пароли не совпадают!');
      return;
    }
    
    console.log('Регистрация:', formData);
    // Здесь будет логика регистрации
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>Регистрация в SyncSlot</h2>
          <p>Создайте новый аккаунт</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="name">Название организации</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Введите название вашей организации"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="address">Адрес</label>
            <input
              type="text"
              id="address"
              name="address"
              value={formData.address}
              onChange={handleChange}
              placeholder="Введите адрес вашей организации"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="example@mail.ru"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="phone">Телефон</label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="+7 XXX XXX XX XX"
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
              placeholder="Придумайте надежный пароль"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Повторите пароль</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Повторите ваш пароль"
              required
            />
          </div>

          <button type="submit" className="btn btn-primary btn-full">
            Зарегистрироваться
          </button>

          <div className="auth-links">
            <span>Уже есть аккаунт?</span>
            <Link to="/login" className="auth-link">
              Войти
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;