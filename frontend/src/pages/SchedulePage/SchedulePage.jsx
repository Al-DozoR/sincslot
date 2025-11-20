import React, { useState } from 'react';
import styles from './SchedulePage.module.css';

const SchedulePage = () => {
  // Тестовые данные для демонстрации
  const [appointments, setAppointments] = useState([
    {
      id: 1,
      clientName: 'Иванов Алексей',
      phone: '+7 (912) 345-67-89',
      service: 'Стрижка',
      date: '2024-01-15',
      time: '10:00',
      status: 'Подтвержден'
    },
    {
      id: 2,
      clientName: 'Петрова Мария',
      phone: '+7 (923) 456-78-90',
      service: 'Маникюр',
      date: '2024-01-15',
      time: '11:30',
      status: 'Ожидание'
    },
    {
      id: 3,
      clientName: 'Сидоров Дмитрий',
      phone: '+7 (934) 567-89-01',
      service: 'Массаж',
      date: '2024-01-16',
      time: '14:00',
      status: 'Отменен'
    },
    {
      id: 4,
      clientName: 'Козлова Анна',
      phone: '+7 (945) 678-90-12',
      service: 'Консультация',
      date: '2024-01-16',
      time: '16:30',
      status: 'Подтвержден'
    },
    {
      id: 5,
      clientName: 'Федоров Сергей',
      phone: '+7 (956) 789-01-23',
      service: 'Стрижка',
      date: '2024-01-17',
      time: '09:00',
      status: 'Ожидание'
    }
  ]);

  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  // Функция для сортировки
  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }

    const sortedAppointments = [...appointments].sort((a, b) => {
      if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
      if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
      return 0;
    });

    setAppointments(sortedAppointments);
    setSortConfig({ key, direction });
  };

  // Функция для получения класса статуса
  const getStatusClass = (status) => {
    switch (status) {
      case 'Подтвержден':
        return styles.statusConfirmed;
      case 'Ожидание':
        return styles.statusPending;
      case 'Отменен':
        return styles.statusCancelled;
      default:
        return '';
    }
  };

  // Функция для отображения значка сортировки 
  const getSortIcon = (key) => {
    if (sortConfig.key !== key) return null;
    return sortConfig.direction === 'asc' ? '↑' : '↓';
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Расписание записей</h1>
        <div className={styles.stats}>
          Всего записей: <span className={styles.count}>{appointments.length}</span>
        </div>
      </div>

      <div className={styles.tableContainer}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th 
                onClick={() => handleSort('clientName')} 
                className={styles.sortable}
              >
                <div className={styles.thContent}>
                  Имя клиента
                  {getSortIcon('clientName') && (
                    <span className={styles.sortIcon}>{getSortIcon('clientName')}</span>
                  )}
                </div>
              </th>
              <th 
                onClick={() => handleSort('phone')} 
                className={styles.sortable}
              >
                <div className={styles.thContent}>
                  Телефон
                  {getSortIcon('phone') && (
                    <span className={styles.sortIcon}>{getSortIcon('phone')}</span>
                  )}
                </div>
              </th>
              <th 
                onClick={() => handleSort('service')} 
                className={styles.sortable}
              >
                <div className={styles.thContent}>
                  Услуга
                  {getSortIcon('service') && (
                    <span className={styles.sortIcon}>{getSortIcon('service')}</span>
                  )}
                </div>
              </th>
              <th 
                onClick={() => handleSort('date')} 
                className={styles.sortable}
              >
                <div className={styles.thContent}>
                  Дата
                  {getSortIcon('date') && (
                    <span className={styles.sortIcon}>{getSortIcon('date')}</span>
                  )}
                </div>
              </th>
              <th 
                onClick={() => handleSort('time')} 
                className={styles.sortable}
              >
                <div className={styles.thContent}>
                  Время
                  {getSortIcon('time') && (
                    <span className={styles.sortIcon}>{getSortIcon('time')}</span>
                  )}
                </div>
              </th>
              <th 
                onClick={() => handleSort('status')} 
                className={styles.sortable}
              >
                <div className={styles.thContent}>
                  Статус
                  {getSortIcon('status') && (
                    <span className={styles.sortIcon}>{getSortIcon('status')}</span>
                  )}
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            {appointments.map((appointment) => (
              <tr key={appointment.id} className={styles.row}>
                <td className={styles.cell}>{appointment.clientName}</td>
                <td className={styles.cell}>{appointment.phone}</td>
                <td className={styles.cell}>{appointment.service}</td>
                <td className={styles.cell}>
                  {new Date(appointment.date).toLocaleDateString('ru-RU')}
                </td>
                <td className={styles.cell}>{appointment.time}</td>
                <td className={styles.cell}>
                  <span className={`${styles.status} ${getStatusClass(appointment.status)}`}>
                    {appointment.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {appointments.length === 0 && (
        <div className={styles.emptyState}>
          <p>Нет записей на выбранную дату</p>
        </div>
      )}
    </div>
  );
};

export default SchedulePage;