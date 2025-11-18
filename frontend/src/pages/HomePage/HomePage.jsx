import React from 'react';
import styles from './HomePage.module.css';
import {Link} from 'react-router-dom';

function HomePage() {
  return (
    <div>
      <header className={styles.header}>
        <div className={styles.container}>
          <div className={styles.headerContent}>
            <div className={styles.logo}>
              <h1>SyncSlot</h1>
            </div>
            <nav className={styles.authButtons}>
              <Link to="/login">
                <button className={`${styles.btn} ${styles.btnOutline}`}>Войти</button>
              </Link>
              <Link to="/register">
                <button className={`${styles.btn} ${styles.btnPrimary}`}>Зарегистрироваться</button>
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className={styles.main}>
        <div className={styles.container}>
          <section className={styles.section}>
            <h2>Кто мы</h2>
            <div className={styles.contentCard}>
              <p className={styles.intro}>
                <strong>SyncSlot</strong> - это инновационная платформа для онлайн-записи,
                которая объединяет организации и клиентов в одном удобном пространстве.
              </p>

              <div className={styles.featuresGrid}>
                <div className={styles.feature}>
                  <h3>🏢 Для организаций</h3>
                  <ul>
                    <li>Личные кабинеты для управления записями</li>
                    <li>Гибкое расписание и настройка слотов</li>
                    <li>Автоматическое напоминание клиентам</li>
                    <li>Аналитика и статистика посещений</li>
                  </ul>
                </div>

                <div className={styles.feature}>
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

          <section className={styles.section}>
            <h2>Почему стоит выбрать SyncSlot?</h2>
            <div className={styles.contentCard}>
              <div className={styles.advantagesGrid}>
                <div className={styles.advantageItem}>
                  <div className={styles.advantageIcon}>🚀</div>
                  <h3>Простота использования</h3>
                  <p>Интуитивный интерфейс, который понятен с первого взгляда</p>
                </div>

                <div className={styles.advantageItem}>
                  <div className={styles.advantageIcon}>⏰</div>
                  <h3>Экономия времени</h3>
                  <p>Записывайтесь за 30 секунд без звонков и ожидания</p>
                </div>

                <div className={styles.advantageItem}>
                  <div className={styles.advantageIcon}>📅</div>
                  <h3>Умное расписание</h3>
                  <p>Автоматическое распределение времени и предотвращение накладок</p>
                </div>

                <div className={styles.advantageItem}>
                  <div className={styles.advantageIcon}>🔔</div>
                  <h3>Напоминания</h3>
                  <p>Никогда не пропустите визит благодаря автоматическим уведомлениям</p>
                </div>

                <div className={styles.advantageItem}>
                  <div className={styles.advantageIcon}>📱</div>
                  <h3>Доступность</h3>
                  <p>Работает на всех устройствах в любое время суток</p>
                </div>

                <div className={styles.advantageItem}>
                  <div className={styles.advantageIcon}>🛡️</div>
                  <h3>Безопасность</h3>
                  <p>Ваши данные защищены по современным стандартам</p>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>

      <footer className={styles.footer}>
        <div className={styles.container}>
          <div className={styles.footerContent}>
            <p className={styles.copyright}>&copy; 2025 УрФУ SyncSlot. Все права защищены.</p>
            <div className={styles.teamSection}>
              <h4>Команда разработки РИЗМ-151207:</h4>
              <div className={styles.teamMembersInline}>
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