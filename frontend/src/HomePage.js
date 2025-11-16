import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  return (
    <div className="home-page">
      <header className="header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <h1>SyncSlot</h1>
            </div>
            <nav className="auth-buttons">
              <Link to="/login">
                <button className="btn btn-outline">Войти</button>
              </Link>
              <Link to="/register">
                <button className="btn btn-primary">Зарегистрироваться</button>
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className="main">
        <div className="container">
          <section className="section">
            <h2>Кто мы</h2>
            <div className="content-card">
              <p className="intro">
                <strong>SyncSlot</strong> - это инновационная платформа для онлайн-записи, 
                которая объединяет организации и клиентов в одном удобном пространстве.
              </p>
              
              <div className="features-grid">
                <div className="feature">
                  <h3>🏢 Для организаций</h3>
                  <ul>
                    <li>Личные кабинеты для управления записями</li>
                    <li>Гибкое расписание и настройка слотов</li>
                    <li>Автоматическое напоминание клиентам</li>
                    <li>Аналитика и статистика посещений</li>
                  </ul>
                </div>
                
                <div className="feature">
                  <h3>👥 Для клиентов</h3>
                  <ul>
                    <li>Быстрая запись в один клик</li>
                    <li>Поиск услуг и организаций поблизости</li>
                    <li>Уведомления о предстоящих визитах</li>
                    <li>История записей и отзывы</li>
                  </ul>
                </div>
              </div>
            </div>
          </section>

          <section className="section">
            <h2>Почему стоит выбрать SyncSlot?</h2>
            <div className="content-card">
              <div className="advantages-grid">
                <div className="advantage-item">
                  <div className="advantage-icon">🚀</div>
                  <h3>Простота использования</h3>
                  <p>Интуитивный интерфейс, который понятен с первого взгляда</p>
                </div>
                
                <div className="advantage-item">
                  <div className="advantage-icon">⏰</div>
                  <h3>Экономия времени</h3>
                  <p>Записывайтесь за 30 секунд без звонков и ожидания</p>
                </div>
                
                <div className="advantage-item">
                  <div className="advantage-icon">📅</div>
                  <h3>Умное расписание</h3>
                  <p>Автоматическое распределение времени и предотвращение накладок</p>
                </div>
                
                <div className="advantage-item">
                  <div className="advantage-icon">🔔</div>
                  <h3>Напоминания</h3>
                  <p>Никогда не пропустите визит благодаря автоматическим уведомлениям</p>
                </div>
                
                <div className="advantage-item">
                  <div className="advantage-icon">📱</div>
                  <h3>Доступность</h3>
                  <p>Работает на всех устройствах в любое время суток</p>
                </div>
                
                <div className="advantage-item">
                  <div className="advantage-icon">🛡️</div>
                  <h3>Безопасность</h3>
                  <p>Ваши данные защищены по современным стандартам</p>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>

     <footer className="footer">
    <div className="container">
        <div className="footer-content">
        <p className="copyright">&copy; 2025 УрФУ  SyncSlot. Все права защищены.</p>
        
        <div className="team-section">
            <h4>Команда разработки РИЗМ-151207:</h4>
            <div className="team-members-inline">
            <span>Снежана Шевчук</span>
            <span>Салимов Александр</span>
            <span>Иван Казанцев</span>
            <span>Владислав Казанцев</span>
            <span>Роман Чечулин</span>
            </div>
        </div>
        </div>
    </div>
    </footer>
    </div>
  );
}

export default HomePage;