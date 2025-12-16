import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Header.module.css';

const Header = ({ title, showLogout = true }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Здесь будет логика выхода (удаление токена и т.д.)
    console.log('Выход из учетной записи');
    // После выхода перенаправляем на главную страницу
    navigate('/');
  };

  const handleGoToSchedule = () => {
    navigate('/schedule');
  };

  const handleGoToServices = () => {
    navigate('/services');
  };

  const handleGoToSettings = () => {
    navigate('/settings');
  };

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.leftSection}>
          <h1 className={styles.title}>{title}</h1>
          <nav className={styles.nav}>
            <button 
              className={styles.navButton}
              onClick={handleGoToSchedule}
            >
              Расписание
            </button>
            <button 
              className={styles.navButton}
              onClick={handleGoToServices}
            >
              Услуги
            </button>
            <button 
              className={styles.navButton}
              onClick={handleGoToSettings}
            >
              Настройки
            </button>
          </nav>
        </div>
        
        {showLogout && (
          <div className={styles.rightSection}>
            <button 
              className={styles.logoutButton}
              onClick={handleLogout}
            >
              Выйти из учетной записи
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
