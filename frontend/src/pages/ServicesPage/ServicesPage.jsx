import React, { useState } from 'react';
import styles from './ServicesPage.module.css';

const ServicesPage = () => {
  // Моковые данные услуг
  const [services, setServices] = useState([
    {
      id: 1,
      name: 'Стрижка мужская',
      duration: '60 мин',
      description: 'Классическая мужская стрижка с укладкой',
      price: '1500 ₽'
    },
    {
      id: 2,
      name: 'Маникюр',
      duration: '90 мин',
      description: 'Комплексный маникюр с покрытием',
      price: '2000 ₽'
    },
    {
      id: 3,
      name: 'Массаж спины',
      duration: '45 мин',
      description: 'Расслабляющий массаж шейно-воротниковой зоны',
      price: '2500 ₽'
    },
    {
      id: 4,
      name: 'Консультация',
      duration: '30 мин',
      description: 'Первичная консультация специалиста',
      price: '1000 ₽'
    },
    {
      id: 5,
      name: 'SPA-процедура',
      duration: '120 мин',
      description: 'Полный комплекс SPA-ухода',
      price: '5000 ₽'
    }
  ]);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingService, setEditingService] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    duration: '',
    price: ''
  });

  // Открытие модального окна для редактирования
  const handleEditClick = (service) => {
    setEditingService(service);
    setFormData({
      name: service.name,
      description: service.description,
      duration: service.duration,
      price: service.price
    });
    setIsModalOpen(true);
  };

  // Закрытие модального окна
  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingService(null);
    setFormData({
      name: '',
      description: '',
      duration: '',
      price: ''
    });
  };

  // Обработчик изменения полей формы
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Сохранение изменений
  const handleSave = (e) => {
    e.preventDefault();
    
    if (editingService) {
      const updatedServices = services.map(service =>
        service.id === editingService.id
          ? { ...service, ...formData }
          : service
      );
      setServices(updatedServices);
    }
    
    handleCloseModal();
  };

  // Сброс формы
  const handleReset = () => {
    if (editingService) {
      setFormData({
        name: editingService.name,
        description: editingService.description,
        duration: editingService.duration,
        price: editingService.price
      });
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Услуги</h1>
        <div className={styles.stats}>
          Всего услуг: <span className={styles.count}>{services.length}</span>
        </div>
      </div>

      <div className={styles.servicesGrid}>
        {services.map((service) => (
          <div
            key={service.id}
            className={styles.serviceCard}
            onClick={() => handleEditClick(service)}
          >
            <div className={styles.serviceHeader}>
              <h3 className={styles.serviceName}>{service.name}</h3>
              <span className={styles.serviceDuration}>{service.duration}</span>
            </div>
            <div className={styles.servicePrice}>{service.price}</div>
            <p className={styles.serviceDescription}>{service.description}</p>
            <div className={styles.editHint}>Нажмите для редактирования</div>
          </div>
        ))}
      </div>

      {/* Модальное окно редактирования */}
      {isModalOpen && (
        <div className={styles.modalOverlay} onClick={handleCloseModal}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <h2>Редактирование услуги</h2>
              <button
                className={styles.closeButton}
                onClick={handleCloseModal}
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSave} className={styles.modalForm}>
              <div className={styles.formGroup}>
                <label htmlFor="name">Название услуги</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  className={styles.input}
                />
              </div>

              <div className={styles.formGroup}>
                <label htmlFor="description">Описание услуги</label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  rows="3"
                  required
                  className={styles.textarea}
                />
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label htmlFor="duration">Длительность</label>
                  <input
                    type="text"
                    id="duration"
                    name="duration"
                    value={formData.duration}
                    onChange={handleInputChange}
                    placeholder="60 мин"
                    required
                    className={styles.input}
                  />
                </div>

                <div className={styles.formGroup}>
                  <label htmlFor="price">Стоимость</label>
                  <input
                    type="text"
                    id="price"
                    name="price"
                    value={formData.price}
                    onChange={handleInputChange}
                    placeholder="1500 ₽"
                    required
                    className={styles.input}
                  />
                </div>
              </div>

              <div className={styles.modalActions}>
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
                  Сохранить
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ServicesPage;