import React, {useState} from 'react';
import {Link} from 'react-router-dom';
import styles from '../Auth.module.css';

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
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <div className={styles.authHeader}>
          <h2>Вход в SyncSlot</h2>
          <p>Войдите в свой аккаунт</p>
        </div>

        <form onSubmit={handleSubmit} className={styles.authForm}>
          <div className={styles.formGroup}>
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

          <div className={styles.formGroup}>
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

          <button type="submit" className={`${styles.btn} ${styles.btnPrimary} ${styles.btnFull}`}>
            Войти
          </button>

          <div className={styles.authLinks}>
            <Link to="/forgot-password" className={styles.authLink}>
              Восстановить пароль
            </Link>
            <span className={styles.authDivider}>|</span>
            <Link to="/register" className={styles.authLink}>
              Зарегистрироваться
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;