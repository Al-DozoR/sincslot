import React, { useState } from 'react';
import styles from './CompanySettingsPage.module.css';

const CompanySettingsPage = () => {
  // Состояние для данных компании
  const [companyData, setCompanyData] = useState({
    // Основная информация
    name: 'Салон красоты "Элегант"',
    phone: '+7 (912) 345-67-89',
    email: 'elegant@mail.ru',
    address: 'г. Екатеринбург, ул. Ленина, 45',
    
    // Расписание
    schedule: {
      monday: { enabled: true, start: '09:00', end: '18:00' },
      tuesday: { enabled: true, start: '09:00', end: '18:00' },
      wednesday: { enabled: true, start: '09:00', end: '18:00' },
      thursday: { enabled: true, start: '09:00', end: '18:00' },
      friday: { enabled: true, start: '09:00', end: '18:00' },
      saturday: { enabled: true, start: '10:00', end: '16:00' },
      sunday: { enabled: false, start: '10:00', end: '16:00' }
    },
    
    // Дополнительные настройки
    logo: null,
    companyUrl: 'elegant-beauty',
    bookingLink: 'https://syncslot.ru/booking/elegant-beauty'
  });

  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  const [logoPreview, setLogoPreview] = useState(null);

  // Обработчики изменений основной информации
  const handleBasicInfoChange = (field, value) => {
    setCompanyData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Обработчики изменений расписания
  const handleScheduleChange = (day, field, value) => {
    setCompanyData(prev => ({
      ...prev,
      schedule: {
        ...prev.schedule,
        [day]: {
          ...prev.schedule[day],
          [field]: field === 'enabled' ? !prev.schedule[day].enabled : value
        }
      }
    }));
  };

  // Обработчик загрузки логотипа
  const handleLogoUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setLogoPreview(e.target.result);
        setCompanyData(prev => ({
          ...prev,
          logo: file
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  // Обработчик изменения пароля
  const handlePasswordChange = (field, value) => {
    setPasswordData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Копирование ссылки для записи
  const copyBookingLink = () => {
    navigator.clipboard.writeText(companyData.bookingLink)
      .then(() => {
        alert('Ссылка скопирована в буфер обмена!');
      })
      .catch(err => {
        console.error('Ошибка копирования: ', err);
      });
  };

  // Сохранение изменений
  const handleSave = (e) => {
    e.preventDefault();
    console.log('Сохранение данных:', companyData);
    console.log('Изменение пароля:', passwordData);
    alert('Изменения сохранены успешно!');
  };

  // Сброс изменений
  const handleReset = () => {
    setCompanyData({
      name: 'Салон красоты "Элегант"',
      phone: '+7 (912) 345-67-89',
      email: 'elegant@mail.ru',
      address: 'г. Екатеринбург, ул. Ленина, 45',
      schedule: {
        monday: { enabled: true, start: '09:00', end: '18:00' },
        tuesday: { enabled: true, start: '09:00', end: '18:00' },
        wednesday: { enabled: true, start: '09:00', end: '18:00' },
        thursday: { enabled: true, start: '09:00', end: '18:00' },
        friday: { enabled: true, start: '09:00', end: '18:00' },
        saturday: { enabled: true, start: '10:00', end: '16:00' },
        sunday: { enabled: false, start: '10:00', end: '16:00' }
      },
      logo: null,
      companyUrl: 'elegant-beauty',
      bookingLink: 'https://syncslot.ru/booking/elegant-beauty'
    });
    setPasswordData({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    });
    setLogoPreview(null);
    alert('Изменения сброшены!');
  };

  // Удаление профиля
  const handleDeleteProfile = () => {
    if (window.confirm('Вы уверены, что хотите удалить профиль компании? Это действие нельзя отменить.')) {
      console.log('Удаление профиля компании');
      alert('Профиль компании удален');
    }
  };

  const daysOfWeek = [
    { key: 'monday', label: 'Понедельник' },
    { key: 'tuesday', label: 'Вторник' },
    { key: 'wednesday', label: 'Среда' },
    { key: 'thursday', label: 'Четверг' },
    { key: 'friday', label: 'Пятница' },
    { key: 'saturday', label: 'Суббота' },
    { key: 'sunday', label: 'Воскресенье' }
  ];

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Настройки компании</h1>
      </div>

      <form onSubmit={handleSave} className={styles.form}>
        {/* Основная информация */}
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Основная информация</h2>
          <div className={styles.formGrid}>
            <div className={styles.formGroup}>
              <label htmlFor="name">Название компании</label>
              <input
                type="text"
                id="name"
                value={companyData.name}
                onChange={(e) => handleBasicInfoChange('name', e.target.value)}
                className={styles.input}
                required
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="phone">Телефон</label>
              <input
                type="tel"
                id="phone"
                value={companyData.phone}
                onChange={(e) => handleBasicInfoChange('phone', e.target.value)}
                className={styles.input}
                required
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                value={companyData.email}
                onChange={(e) => handleBasicInfoChange('email', e.target.value)}
                className={styles.input}
                required
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="address">Адрес</label>
              <input
                type="text"
                id="address"
                value={companyData.address}
                onChange={(e) => handleBasicInfoChange('address', e.target.value)}
                className={styles.input}
                required
              />
            </div>
          </div>
        </section>

        {/* Расписание */}
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Расписание</h2>
          <div className={styles.scheduleGrid}>
            {daysOfWeek.map((day) => (
              <div key={day.key} className={styles.scheduleItem}>
                <label className={styles.dayLabel}>
                  <input
                    type="checkbox"
                    checked={companyData.schedule[day.key].enabled}
                    onChange={() => handleScheduleChange(day.key, 'enabled')}
                    className={styles.checkbox}
                  />
                  <span>{day.label}</span>
                </label>
                
                {companyData.schedule[day.key].enabled && (
                  <div className={styles.timeInputs}>
                    <input
                      type="time"
                      value={companyData.schedule[day.key].start}
                      onChange={(e) => handleScheduleChange(day.key, 'start', e.target.value)}
                      className={styles.timeInput}
                    />
                    <span className={styles.timeSeparator}>—</span>
                    <input
                      type="time"
                      value={companyData.schedule[day.key].end}
                      onChange={(e) => handleScheduleChange(day.key, 'end', e.target.value)}
                      className={styles.timeInput}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>

        <div className={styles.divider}></div>

        {/* Дополнительные настройки */}
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Дополнительные настройки</h2>
          
          {/* Логотип */}
          <div className={styles.logoSection}>
            <label className={styles.logoLabel}>Логотип компании</label>
            <div className={styles.logoUpload}>
              <div className={styles.logoPreview}>
                {logoPreview ? (
                  <img src={logoPreview} alt="Логотип" className={styles.logoImage} />
                ) : (
                  <div className={styles.logoPlaceholder}>Логотип</div>
                )}
              </div>
              <input
                type="file"
                id="logo"
                accept="image/*"
                onChange={handleLogoUpload}
                className={styles.fileInput}
              />
              <label htmlFor="logo" className={styles.uploadButton}>
                Выбрать файл
              </label>
            </div>
          </div>

          {/* Ссылка на компанию */}
          <div className={styles.formGroup}>
            <label htmlFor="companyUrl">Ссылка на компанию</label>
            <div className={styles.urlInputWrapper}>
              <span className={styles.urlPrefix}>syncslot.ru/</span>
              <input
                type="text"
                id="companyUrl"
                value={companyData.companyUrl}
                onChange={(e) => handleBasicInfoChange('companyUrl', e.target.value)}
                className={styles.urlInput}
                required
              />
            </div>
          </div>

          {/* Изменение пароля */}
          <div className={styles.passwordSection}>
            <h3 className={styles.subsectionTitle}>Изменить пароль</h3>
            <div className={styles.formGrid}>
              <div className={styles.formGroup}>
                <label htmlFor="currentPassword">Текущий пароль</label>
                <input
                  type="password"
                  id="currentPassword"
                  value={passwordData.currentPassword}
                  onChange={(e) => handlePasswordChange('currentPassword', e.target.value)}
                  className={styles.input}
                />
              </div>
              <div className={styles.formGroup}>
                <label htmlFor="newPassword">Новый пароль</label>
                <input
                  type="password"
                  id="newPassword"
                  value={passwordData.newPassword}
                  onChange={(e) => handlePasswordChange('newPassword', e.target.value)}
                  className={styles.input}
                />
              </div>
              <div className={styles.formGroup}>
                <label htmlFor="confirmPassword">Подтвердите пароль</label>
                <input
                  type="password"
                  id="confirmPassword"
                  value={passwordData.confirmPassword}
                  onChange={(e) => handlePasswordChange('confirmPassword', e.target.value)}
                  className={styles.input}
                />
              </div>
            </div>
          </div>

          {/* Ссылка для записи */}
          <div className={styles.bookingLinkSection}>
            <h3 className={styles.subsectionTitle}>Ссылка для записи</h3>
            <div className={styles.bookingLinkWrapper}>
              <input
                type="text"
                value={companyData.bookingLink}
                readOnly
                className={styles.bookingLinkInput}
              />
              <button
                type="button"
                onClick={copyBookingLink}
                className={styles.copyButton}
              >
                Копировать
              </button>
            </div>
          </div>

          {/* Удаление профиля */}
          <div className={styles.deleteSection}>
            <button
              type="button"
              onClick={handleDeleteProfile}
              className={styles.deleteButton}
            >
              Удалить профиль компании
            </button>
          </div>
        </section>

        {/* Кнопки действий */}
        <div className={styles.actions}>
          <button
            type="button"
            onClick={handleReset}
            className={styles.resetButton}
          >
            Сбросить
          </button>
          <button
            type="submit"
            className={styles.saveButton}
          >
            Сохранить изменения
          </button>
        </div>
      </form>
    </div>
  );
};

export default CompanySettingsPage;