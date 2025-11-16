import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Auth.css';

function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Восстановление пароля для:', email);
    // Здесь будет логика отправки email для восстановления
    setIsSubmitted(true);
  };

  if (isSubmitted) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-header">
            <div className="success-icon">✅</div>
            <h2>Письмо отправлено!</h2>
            <p>Мы отправили инструкции по восстановлению пароля на email: <strong>{email}</strong></p>
          </div>

          <div className="auth-links" style={{ justifyContent: 'center', marginTop: '2rem' }}>
            <Link to="/login" className="btn btn-primary">
              Вернуться к входу
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>Восстановление пароля</h2>
          <p>Введите email, указанный при регистрации</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="example@mail.ru"
              required
            />
          </div>

          <button type="submit" className="btn btn-primary btn-full">
            Восстановить пароль
          </button>

          <div className="auth-links">
            <Link to="/login" className="auth-link">
              ← Вернуться к входу
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ForgotPassword;