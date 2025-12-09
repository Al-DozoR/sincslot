import React, {useEffect, useRef, useState} from 'react';
import styles from './CompanySettingsPage.module.css';
import {toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {companyService} from "../../services/companyService.js";
import {getChangedFields} from "../../utils/getChangedFields";

const CompanySettingsPage = () => {
  const [errors, setErrors] = useState({});
  const [companyData, setCompanyData] = useState(null);
  const [savedCompanyData, setSavedCompanyData] = useState(null);

  const [schedule, setSchedule] = useState(null);
  const [savedSchedule, setSavedSchedule] = useState(null);

  const [isLoading, setIsLoading] = useState(true);

  const [passwordData, setPasswordData] = useState({
    currentPassword: "",
    newPassword: "",
    newRepeatPassword: ""
  });

  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  const [logoFile, setLogoFile] = useState(null);
  const [logoPreview, setLogoPreview] = useState(null);
  const [savedLogoPreview, setSavedLogoPreview] = useState(null);

  const logoInputRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const company = await companyService.getCompanySettings();
        const backendSchedule = await companyService.getCompanySchedule();

        const normalizedCompany = {
          ...company,
          description: company.description ?? ""
        };

        setCompanyData(structuredClone(normalizedCompany));
        setSavedCompanyData(structuredClone(normalizedCompany));

        const frontendSchedule = mapBackendScheduleToFrontend(
          backendSchedule.workSchedule
        );
        setSchedule(frontendSchedule);
        setSavedSchedule(structuredClone(frontendSchedule));

        try {
          const response = await companyService.getCompanyLogo();

          if (response?.error) {
            setLogoPreview(null);
            setSavedLogoPreview(null);
          } else {
            setLogoPreview(response);
            setSavedLogoPreview(response);
          }
        } catch (err) {
          console.log("Логотип не найден");
          setLogoPreview(null);
          setSavedLogoPreview(null);
        }
      } catch (error) {
        console.error(error);
        toast.error("Ошибка загрузки данных компании");
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const DAYS_MAP = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
    7: "sunday"
  };

  const mapBackendScheduleToFrontend = (backendSchedule) => {
    const schedule = {};

    // Сначала заполняем все дни дефолтными значениями
    Object.values(DAYS_MAP).forEach(day => {
      schedule[day] = {
        enabled: false,
        start: "",
        end: ""
      };
    });

    if (backendSchedule && backendSchedule.length > 0) {
      backendSchedule.forEach(item => {
        const dayKey = DAYS_MAP[item.dayOfWeek];
        if (dayKey && item.workStart !== null && item.workEnd !== null) {
          schedule[dayKey] = {
            enabled: true,
            start: item.workStart || "",
            end: item.workEnd || ""
          };
        }
      });
    }

    return schedule;
  };

  const mapFrontendScheduleToBackend = (frontendSchedule) => {
    const DAYS_MAP_REVERSE = {
      monday: 1,
      tuesday: 2,
      wednesday: 3,
      thursday: 4,
      friday: 5,
      saturday: 6,
      sunday: 7
    };

    const workSchedule = Object.entries(frontendSchedule)
      .map(([day, {enabled, start, end}]) => ({
        dayOfWeek: DAYS_MAP_REVERSE[day],
        workStart: enabled ? start : null,
        workEnd: enabled ? end : null
      }))
      // фильтруем только активные дни
      .filter(day => day.workStart !== null && day.workEnd !== null);

    return {workSchedule};
  };

  // Обработчики изменений основной информации
  const handleBasicInfoChange = (field, value) => {
    let newValue = value;

    //маска телефона
    if (field === "phone") {
      if (newValue === "7") newValue = "+7";
      newValue = newValue.replace(/[^\d+]/g, "");
    }

    setCompanyData(prev => {
      const newData = { ...prev, [field]: newValue };

      setErrors(prevErrors => ({
        ...prevErrors,
        [field]: validateField(field, newValue, newData)
      }));

      return newData;
    });
  };

  //Обработчики изменений расписания
  const handleScheduleChange = (day, field, value) => {
    setSchedule(prev => ({
      ...prev,
      [day]: {
        ...prev[day],
        [field]: field === "enabled" ? !prev[day].enabled : value
      }
    }));
  };

  //Обработчик загрузки логотипа
  const handleLogoUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLogoFile(file); //запоминаем файл для сохранения

    const reader = new FileReader();
    reader.onload = (e) => {
      setLogoPreview(e.target.result);
    };
    reader.readAsDataURL(file);
  };

  // Обработчик изменения пароля
  const handlePasswordChange = (field, value) => {
    setPasswordData(prev => {
      const newData = { ...prev, [field]: value };

      setErrors(prevErrors => {
        const newErrors = {
          ...prevErrors,
          [field]: validateField(field, value, newData)
        };

        //при смене пароля перепроверяем repeat
        if (field === 'newPassword' && newData.newRepeatPassword) {
          newErrors.newRepeatPassword = validateField(
            'newRepeatPassword',
            newData.newRepeatPassword,
            newData
          );
        }

        return newErrors;
      });

      return newData;
    });
  };

  // Копирование ссылки для записи
  const copyBookingLink = () => {
    const fullUrl = `https://syncslot.ru/booking/${companyData.slugBookingUrl}`;

    navigator.clipboard.writeText(fullUrl)
      .then(() => {
        toast.info("Ссылка скопирована в буфер обмена!");
      })
      .catch(err => {
        toast.error("Ошибка копирования");
      });
  };

  // Открытие модального окна удаления
  const handleDeleteClick = () => {
    setIsDeleteModalOpen(true);
  };

  // Закрытие модального окна удаления
  const handleCloseDeleteModal = () => {
    setIsDeleteModalOpen(false);
  };

  // Подтверждение удаления профиля
  const handleConfirmDelete = () => {
    console.log('Удаление профиля компании');
    alert('Профиль компании удален');
    handleCloseDeleteModal();
    // Здесь будет логика реального удаления профиля
  };

  const isScheduleChanged = (saved, current) => {
    if (!saved || !current) return false;
    return JSON.stringify(saved) !== JSON.stringify(current);
  };

  // Сохранение изменений
  const handleSave = async (e) => {
    e.preventDefault();

    const hasErrors = Object.values(errors).some(err => err);
    if (hasErrors) {
      toast.error("Исправьте ошибки в форме");
      return;
    }

    try {
      let somethingSaved = false;

      // Сохраняем изменения основной информации
      const changedCompanyFields = getChangedFields(savedCompanyData, companyData);

      const passwordPayload =
        passwordData.currentPassword &&
        passwordData.newPassword &&
        passwordData.newRepeatPassword
          ? {
            currentPassword: passwordData.currentPassword,
            newPassword: passwordData.newPassword,
            newRepeatPassword: passwordData.newRepeatPassword
          }
          : {};

      const companyPayload = {
        ...Object.fromEntries(
          Object.entries(changedCompanyFields || {})
            .filter(([_, value]) => value !== null && value !== undefined && value !== "")
        ),
        ...passwordPayload
      };


      if (Object.keys(companyPayload).length > 0) {
        const updatedCompany = await companyService.updateCompanySettings(companyPayload);

        const mergedCompany = {
          ...companyData,
          ...updatedCompany
        };

        setCompanyData(structuredClone(mergedCompany));
        setSavedCompanyData(structuredClone(mergedCompany));
        somethingSaved = true;
      }

      // Сохраняем изменения расписания
      if (isScheduleChanged(savedSchedule, schedule)) {
        const backendPayload = mapFrontendScheduleToBackend(schedule);
        const backendSchedule = await companyService.updateCompanySchedule(backendPayload);

        const frontendSchedule = mapBackendScheduleToFrontend(
          backendSchedule.workSchedule
        );

        setSchedule(frontendSchedule);
        setSavedSchedule(structuredClone(frontendSchedule));
        somethingSaved = true;
      }

      //СОХРАНЯЕМ ЛОГОТОИП (ТОЛЬКО ЕСЛИ ВЫБРАЛИ ФАЙЛ)
      if (logoFile) {
        // Отправляем файл на сервер
        await companyService.uploadCompanyLogo(logoFile);

        // После успешной загрузки обновляем превью и сохранённый логотип
        const newLogoUrl = await companyService.getCompanyLogo();

        if (newLogoUrl?.error) {
          setLogoPreview(null);
          setSavedLogoPreview(null);
        } else {
          setLogoPreview(newLogoUrl);
          setSavedLogoPreview(newLogoUrl);
        }

        // Очищаем локальный файл
        setLogoFile(null);
        somethingSaved = true;
      }

      if (!somethingSaved) {
        toast.info("Нет изменений для сохранения");
        return;
      }

      toast.success("Изменения успешно сохранены");
    } catch (error) {
      console.error(error);
      toast.error("Ошибка при сохранении данных");
    }
  };

  // Сброс изменений
  const handleReset = () => {
    setCompanyData({
      ...structuredClone(savedCompanyData),
      slugBookingUrl: savedCompanyData.slugBookingUrl ?? ""
    });

    setSchedule(structuredClone(savedSchedule));

    setLogoPreview(savedLogoPreview); //возвращаем старый логотип
    setLogoFile(null);                //очищаем файл

    if (logoInputRef.current) {
      logoInputRef.current.value = "";
    }

    setPasswordData({
      currentPassword: "",
      newPassword: "",
      newRepeatPassword: ""
    });

    toast.info("Изменения отменены");
  };

  const daysOfWeek = [
    {key: 'monday', label: 'Понедельник'},
    {key: 'tuesday', label: 'Вторник'},
    {key: 'wednesday', label: 'Среда'},
    {key: 'thursday', label: 'Четверг'},
    {key: 'friday', label: 'Пятница'},
    {key: 'saturday', label: 'Суббота'},
    {key: 'sunday', label: 'Воскресенье'}
  ];

  const validateField = (name, value, currentData) => {
    switch (name) {
      case 'email': {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(value) ? '' : 'Введите корректный email';
      }

      case 'phone': {
        const phoneRegex = /^\+?\d{11}$/;
        return phoneRegex.test(value.replace(/\s+/g, '')) ? '' : 'Введите корректный телефон';
      }

      case 'newPassword': {
        if (!value) return '';

        const errors = [];

        if (value.length < 6) {
          errors.push('Минимум 6 символов');
        }
        if (!/[A-Z]/.test(value)) {
          errors.push('Хотя бы одна заглавная буква');
        }
        if (!/[a-z]/.test(value)) {
          errors.push('Хотя бы одна строчная буква');
        }
        if (!/[!@#$%^&*()_+\-=]/.test(value)) {
          errors.push('Хотя бы один спецсимвол');
        }

        return errors.join(', ');
      }

      case 'newRepeatPassword':
        return value === currentData.newPassword ? '' : 'Пароли не совпадают';

      default:
        return '';
    }
  };

  if (isLoading || !companyData || !schedule) {
    return <div>Загрузка...</div>;
  }

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
                value={companyData.name ?? ""}
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
                value={companyData.phone ?? ""}
                onChange={(e) => handleBasicInfoChange('phone', e.target.value)}
                className={styles.input}
                required
              />
              {errors.phone && <span className={styles.error}>{errors.phone}</span>}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                value={companyData.email ?? ""}
                onChange={(e) => handleBasicInfoChange('email', e.target.value)}
                className={styles.input}
                required
              />
              {errors.email && (
                <span className={styles.error}>{errors.email}</span>
              )}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="address">Адрес</label>
              <input
                type="text"
                id="address"
                value={companyData.address ?? ""}
                onChange={(e) => handleBasicInfoChange('address', e.target.value)}
                className={styles.input}
                required
              />
            </div>

            <div className={`${styles.formGroup} ${styles.fullWidth}`}>
              <label htmlFor="description">Описание</label>
              <textarea
                id="description"
                value={companyData.description ?? ""}
                onChange={(e) => handleBasicInfoChange('description', e.target.value)}
                className={styles.textarea}
                rows={5}
                placeholder="Введите описание компании..."
                required
              />
            </div>
          </div>
        </section>

        {/* Расписание */}
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Расписание</h2>
          <div className={styles.scheduleGrid}>
            {daysOfWeek.map((day) => {
              const daySchedule = schedule?.[day.key] || {enabled: false, start: "", end: ""};
              return (
                <div key={day.key} className={styles.scheduleItem}>
                  <label className={styles.dayLabel}>
                    <input
                      type="checkbox"
                      checked={daySchedule.enabled}
                      onChange={() => handleScheduleChange(day.key, 'enabled')}
                      className={styles.checkbox}
                    />
                    <span>{day.label}</span>
                  </label>

                  <div className={styles.timeInputs}>
                    <input
                      type="time"
                      value={daySchedule.start}
                      onChange={(e) => handleScheduleChange(day.key, 'start', e.target.value)}
                      className={styles.timeInput}
                      disabled={!daySchedule.enabled}
                      required={daySchedule.enabled}
                    />
                    <span className={styles.timeSeparator}>—</span>
                    <input
                      type="time"
                      value={daySchedule.end}
                      onChange={(e) => handleScheduleChange(day.key, 'end', e.target.value)}
                      className={styles.timeInput}
                      disabled={!daySchedule.enabled}
                      required={daySchedule.enabled}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        <div className={styles.divider}></div>

        {/*Дополнительные настройки*/}
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Дополнительные настройки</h2>

          {/*Логотип*/}
          <div className={styles.logoSection}>
            <label className={styles.logoLabel}>Логотип компании</label>
            <div className={styles.logoUpload}>
              <div className={styles.logoPreview}>
                {logoPreview ? (
                  <img src={logoPreview} alt="Логотип" className={styles.logoImage}/>
                ) : (
                  <div className={styles.logoPlaceholder}>Логотип</div>
                )}
              </div>
              <input
                ref={logoInputRef}
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

          {/*Ссылка на компанию*/}
          <div className={styles.formGroup}>
            <label htmlFor="slugBookingUrl">Ссылка на компанию</label>
            <div className={styles.urlInputWrapper}>
              <span className={styles.urlPrefix}>syncslot.ru/booking/</span>
              <input
                type="text"
                id="slugBookingUrl"
                value={companyData.slugBookingUrl ?? ""}
                onChange={(e) => handleBasicInfoChange('slugBookingUrl', e.target.value)}
                className={styles.urlInput}
                required
              />
            </div>
          </div>

          {/*Изменение пароля*/}
          <div className={styles.passwordSection}>
            <h3 className={styles.subsectionTitle}>Изменить пароль</h3>
            <div className={styles.formGrid}>
              <div className={styles.formGroup}>
                <label htmlFor="currentPassword">Текущий пароль</label>
                <input
                  type="password"
                  id="currentPassword"
                  value={passwordData.currentPassword ?? ""}
                  onChange={(e) => handlePasswordChange('currentPassword', e.target.value)}
                  className={styles.input}
                />
              </div>
              <div className={styles.formGroup}>
                <label htmlFor="newPassword">Новый пароль</label>
                <input
                  type="password"
                  id="newPassword"
                  value={passwordData.newPassword ?? ""}
                  onChange={(e) => handlePasswordChange('newPassword', e.target.value)}
                  className={styles.input}
                />
                {errors.newPassword && (
                  <span className={styles.error}>{errors.newPassword}</span>
                )}
              </div>
              <div className={styles.formGroup}>
                <label htmlFor="newRepeatPassword">Подтвердите пароль</label>
                <input
                  type="password"
                  id="newRepeatPassword"
                  value={passwordData.newRepeatPassword ?? ""}
                  onChange={(e) => handlePasswordChange('newRepeatPassword', e.target.value)}
                  className={styles.input}
                />
                {errors.newRepeatPassword && (
                  <span className={styles.error}>{errors.newRepeatPassword}</span>
                )}
              </div>
            </div>
          </div>

          {/* Ссылка для записи*/}
          <div className={styles.bookingLinkSection}>
            <h3 className={styles.subsectionTitle}>Ссылка для записи</h3>
            <div className={styles.bookingLinkWrapper}>
              <input
                type="text"
                value={`https://syncslot.ru/booking/${companyData.slugBookingUrl}`}
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

          {/*Удаление профиля*/}
          <div className={styles.deleteSection}>
            <h3 className={styles.subsectionTitle}>Опасная зона</h3>
            <p className={styles.deleteWarning}>
              Удаление профиля компании приведет к безвозвратной потере всех данных, включая записи клиентов и
              настройки.
            </p>
            <button
              type="button"
              onClick={handleDeleteClick}
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

      {/* Модальное окно подтверждения удаления */}
      {isDeleteModalOpen && (
        <div className={styles.modalOverlay} onClick={handleCloseDeleteModal}>
          <div className={styles.deleteModal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.deleteModalIcon}>⚠️</div>
            <h2 className={styles.deleteModalTitle}>Удалить профиль компании</h2>
            <div className={styles.deleteModalContent}>
              <p className={styles.deleteModalText}>
                Вы уверены, что хотите удалить профиль компании <strong>«{companyData.name}»</strong>?
              </p>
              <div className={styles.deleteModalWarning}>
                <strong>Это действие нельзя отменить!</strong> Будут безвозвратно удалены:
                <ul className={styles.deleteModalList}>
                  <li>Все данные компании</li>
                  <li>Расписание и услуги</li>
                  <li>История записей клиентов</li>
                  <li>Настройки и конфигурации</li>
                </ul>
              </div>
              <div className={styles.deleteModalConfirmText}>
                Для подтверждения введите название вашей компании:
              </div>
              <input
                type="text"
                placeholder={companyData.name}
                className={styles.deleteModalInput}
                onChange={(e) => {
                  // Можно добавить проверку на совпадение с названием компании
                }}
              />
            </div>
            <div className={styles.deleteModalActions}>
              <button
                className={styles.deleteModalCancel}
                onClick={handleCloseDeleteModal}
              >
                Отмена
              </button>
              <button
                className={styles.deleteModalConfirm}
                onClick={handleConfirmDelete}
              >
                Удалить профиль
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CompanySettingsPage;
