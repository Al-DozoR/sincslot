import React, { useState, useEffect } from 'react';
import styles from './ClientBookingPage.module.css';
import { useParams, useNavigate } from 'react-router-dom';

const ClientBookingPage = () => {
  const { companySlug } = useParams(); // Получаем Slug из URL
  const navigate = useNavigate();
  
  const [services, setServices] = useState([]); // Состояние для хранения услуг
  const [selectedService, setSelectedService] = useState(null); // Состояние для выбранной услуги
  const [selectedTime, setSelectedTime] = useState(null); // Состояние для выбранного времени
  const [selectedDate, setSelectedDate] = useState(null); // Состояние для выбранной даты
  const [loading, setLoading] = useState(true); // Состояние для загрузки данных

  useEffect(() => {
    // Функция для получения услуг компании по companySlug
    const fetchServices = async () => {
      try {
        const response = await fetch(/api/v1/booking/services/company/${companySlug});
        if (!response.ok) {
          throw new Error('Ошибка при получении услуг');
        }
        const data = await response.json();
        setServices(data.services); // Предполагаю, что данные приходят в формате { services: [...] }
      } catch (error) {
        console.error('Ошибка:', error);
      } finally {
        setLoading(false); // Завершаем загрузку
      }
    };

    fetchServices();
  }, [companySlug]); // Зависимость от companySlug

  if (loading) {
    return <div>Загрузка услуг...</div>;
  }

  if (error) {
    return <div>Ошибка: {error}</div>;
  }
  
return (
    <div>
        <h1>Услуги компании: {companySlug}</h1>
        <ul>
            {services.map(service => (
                <li key={service.id}>{service.name}</li>
            ))}
        </ul>
    </div>
);

  // Генерация тестовых дат на 30 дней вперед
  const generateAvailableDates = () => {
    const dates = [];
    const today = new Date();
    
    for (let i = 1; i <= 30; i++) {
      const date = new Date();
      date.setDate(today.getDate() + i);
      
      // Делаем доступными примерно 70% дат для демонстрации
      if (Math.random() > 0.3) {
        dates.push(date.toISOString().split('T')[0]);
      }
    }
    
    return dates;
  };

  // Генерация тестового времени для дат
  const generateAvailableTimes = (dates) => {
    const times = {};
    const timeSlots = ['09:00', '10:30', '12:00', '13:30', '15:00', '16:30', '18:00'];
    
    dates.forEach(date => {
      // Для каждой даты оставляем случайные 3-5 временных слотов
      const availableSlots = [...timeSlots]
        .sort(() => Math.random() - 0.5)
        .slice(0, 3 + Math.floor(Math.random() * 3));
      
      times[date] = availableSlots.sort();
    });
    
    return times;
  };

  const availableDates = generateAvailableDates();
  const availableTimes = generateAvailableTimes(availableDates);

  // Функции для работы с календарем
  const getDaysInMonth = (year, month) => {
    return new Date(year, month + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (year, month) => {
    return new Date(year, month, 1).getDay();
  };

  const isDateAvailable = (date) => {
    return availableDates.includes(date);
  };

  const formatDate = (date) => {
    return date.toISOString().split('T')[0];
  };

  // Генерация календаря на 30 дней вперед
  const generateCalendar = () => {
    const today = new Date();
    const calendar = [];
    
    // Генерируем 30 дней начиная с завтрашнего дня
    for (let i = 1; i <= 30; i++) {
      const date = new Date();
      date.setDate(today.getDate() + i);
      const dateString = formatDate(date);
      
      calendar.push({
        day: date.getDate(),
        date: dateString,
        available: isDateAvailable(dateString),
        isToday: dateString === formatDate(today),
        month: date.getMonth(),
        year: date.getFullYear()
      });
    }
    
    return calendar;
  };

  const calendarDays = generateCalendar();
  const today = new Date();
  const monthNames = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ];

  // Группируем дни по месяцам для отображения
  const groupDaysByMonth = (days) => {
    const groups = {};
    
    days.forEach(day => {
      const key = `${day.year}-${day.month}`;
      if (!groups[key]) {
        groups[key] = {
          month: day.month,
          year: day.year,
          days: []
        };
      }
      groups[key].days.push(day);
    });
    
    return Object.values(groups);
  };

  const monthGroups = groupDaysByMonth(calendarDays);

  // Обработчики
  const handleServiceSelect = (service) => {
    setSelectedService(service);
    setIsCalendarModalOpen(true);
  };

  const handleDateSelect = (date) => {
    if (date.available) {
      setSelectedDate(date.date);
      setSelectedTime(null);
    }
  };

  const handleTimeSelect = (time) => {
    setSelectedTime(time);
  };

  const handleCloseCalendar = () => {
    setIsCalendarModalOpen(false);
    setSelectedDate(null);
    setSelectedTime(null);
  };

  const handleContinueToDetails = () => {
    if (selectedService && selectedDate && selectedTime) {
        navigate('/booking-details', { 
        state: { 
            service: selectedService, 
            date: selectedDate, 
            time: selectedTime 
        } 
        });
    }
    };

  const getDayName = (dateString) => {
    const date = new Date(dateString);
    const days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
    return days[date.getDay()];
  };

  const getShortDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long'
    });
  };

 return (
    <div className={styles.pageContainer}>
      {/* Header как на других страницах */}
      <header className={styles.header}>
        <div className={styles.container}>
          <div className={styles.headerContent}>
            <div className={styles.logo}>
              <h1>Timeslot</h1>
            </div>
            <button
              className={styles.myBookingsButton}
              onClick={() => navigate('/my-bookings-auth')}
            >
              📋 Мои записи
            </button>
          </div>
        </div>
      </header>
      
      <div className={styles.mainContent}>
        <div className={styles.pageHeader}>
          <h2 className={styles.pageTitle}>Запись на услугу</h2>
          <p className={styles.pageSubtitle}>Выберите услугу и удобное время для записи</p>
        </div>

        <div className={styles.servicesSection}>
          <h3 className={styles.sectionTitle}>Выберите услугу</h3>
          <div className={styles.servicesGrid}>
            {services.map((service) => (
              <div
                key={service.id}
                className={`${styles.serviceCard} ${
                  selectedService?.id === service.id ? styles.serviceCardSelected : ''
                }`}
                onClick={() => handleServiceSelect(service)}
              >
                <div className={styles.serviceHeader}>
                  <h4 className={styles.serviceName}>{service.name}</h4>
                  <span className={styles.serviceDuration}>{service.duration}</span>
                </div>
                <div className={styles.servicePrice}>{service.price}</div>
                <p className={styles.serviceDescription}>{service.description}</p>
                <div className={styles.selectHint}>
                  {selectedService?.id === service.id ? '✓ Выбрано' : 'Выбрать'}
                </div>
              </div>
            ))}
          </div>
        </div>

      {/* Модальное окно с календарем */}
      {isCalendarModalOpen && selectedService && (
        <div className={styles.modalOverlay} onClick={handleCloseCalendar}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <h2>Выберите дату и время</h2>
              <div className={styles.selectedService}>
                <strong>{selectedService.name}</strong> • {selectedService.duration} • {selectedService.price}
              </div>
              <button
                className={styles.closeButton}
                onClick={handleCloseCalendar}
              >
                ×
              </button>
            </div>

            <div className={styles.calendarSection}>
              <div className={styles.calendarInfo}>
                <p>✅ Доступные даты отмечены зеленой точкой</p>
                <p>📅 Выберите дату, чтобы увидеть доступное время</p>
              </div>

              {monthGroups.map((monthGroup, groupIndex) => (
                <div key={groupIndex} className={styles.monthSection}>
                  <div className={styles.monthHeader}>
                    <h3>{monthNames[monthGroup.month]} {monthGroup.year}</h3>
                  </div>
                  
                  <div className={styles.calendarGrid}>
                    <div className={styles.weekDays}>
                      {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map(day => (
                        <div key={day} className={styles.weekDay}>{day}</div>
                      ))}
                    </div>
                    
                    <div className={styles.calendarDays}>
                      {/* Пустые ячейки для выравнивания первого дня месяца */}
                      {Array.from({ length: new Date(monthGroup.year, monthGroup.month, 1).getDay() }, (_, i) => (
                        <div key={`empty-${i}`} className={styles.calendarDayEmpty}></div>
                      ))}
                      
                      {monthGroup.days.map((day, dayIndex) => (
                        <div
                          key={dayIndex}
                          className={`${styles.calendarDay} ${
                            day.available ? styles.available : styles.unavailable
                          } ${selectedDate === day.date ? styles.selected : ''} ${
                            day.isToday ? styles.today : ''
                          }`}
                          onClick={() => handleDateSelect(day)}
                        >
                          <span className={styles.dayNumber}>{day.day}</span>
                          {day.available && (
                            <div className={styles.availableDot}></div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}

              {/* Выбор времени */}
              {selectedDate && (
                <div className={styles.timeSelection}>
                  <h4 className={styles.timeTitle}>
                    {getDayName(selectedDate)}, {getShortDate(selectedDate)}
                  </h4>
                  <div className={styles.timeSlots}>
                    {availableTimes[selectedDate]?.length > 0 ? (
                      availableTimes[selectedDate].map((time) => (
                        <button
                          key={time}
                          className={`${styles.timeSlot} ${
                            selectedTime === time ? styles.timeSlotSelected : ''
                          }`}
                          onClick={() => handleTimeSelect(time)}
                        >
                          {time}
                        </button>
                      ))
                    ) : (
                      <div className={styles.noTimesAvailable}>
                        На выбранную дату нет доступного времени
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Кнопка продолжения */}
              {selectedTime && (
                <div className={styles.continueSection}>
                  <div className={styles.selectedInfo}>
                    <strong>Выбрано:</strong> {getDayName(selectedDate)}, {getShortDate(selectedDate)} в {selectedTime}
                  </div>
                  <button
                    className={styles.continueButton}
                    onClick={handleContinueToDetails}
                  >
                    Продолжить запись
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
    </div>
  );
};

export default ClientBookingPage;
