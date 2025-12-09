import React, { useState } from 'react';
import styles from './ServicesPage.module.css';
import {servicesService} from "../../services/servicesService.js";
import {toast} from "react-toastify";

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
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [editingService, setEditingService] = useState(null);
  const [serviceToDelete, setServiceToDelete] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    duration: '',
    price: ''
  });

  // Открытие модального окна для редактирования
  const handleEditClick = async (service) => {
    try {
      // Получаем актуальные данные с сервера
      const updatedService = await servicesService.get(service.id);

      // Обновляем локальный стейт карточки
      setServices(prev =>
        prev.map(s => (s.id === updatedService.id ? updatedService : s))
      );

      // Открываем модальное окно и заполняем форму
      setEditingService(updatedService);
      setFormData({
        name: updatedService.name,
        description: updatedService.description,
        duration: updatedService.duration,
        price: updatedService.price
      });
      setIsModalOpen(true);

    } catch (error) {
      console.error("Ошибка при загрузке данных услуги:", error);
      toast.error(
        error?.response?.data?.detail || "Не удалось загрузить данные услуги"
      );
    }
  };

  // Открытие модального окна для добавления
  const handleAddClick = () => {
    setEditingService(null);
    setFormData({
      name: '',
      description: '',
      duration: '',
      price: ''
    });
    setIsAddModalOpen(true);
  };

  // Открытие модального окна подтверждения удаления
  const handleDeleteClick = (service, e) => {
    e.stopPropagation();
    setServiceToDelete(service);
    setIsDeleteModalOpen(true);
  };

  // Закрытие всех модальных окон
  const handleCloseModal = () => {
    setIsModalOpen(false);
    setIsAddModalOpen(false);
    setIsDeleteModalOpen(false);
    setEditingService(null);
    setServiceToDelete(null);
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
  const handleSave = async (e) => {
    e.preventDefault();

    if (!editingService) return;

    try {
      const payload = {
        name: formData.name,
        description: formData.description,
        duration: Number(formData.duration),
        price: Number(formData.price),
      };

      // Отправляем PATCH на сервер
      const updatedService = await servicesService.update(editingService.id, payload);

      // Обновляем локальный стейт
      setServices(prev =>
        prev.map(service =>
          service.id === updatedService.id ? updatedService : service
        )
      );

      toast.success("Услуга успешно сохранена!");
      handleCloseModal();
    } catch (error) {
      console.error("Ошибка при сохранении услуги:", error);
      toast.error(
        error?.response?.data?.detail || "Не удалось сохранить услугу"
      );
    }
  };

  // Добавление новой услуги
  const handleAddService = async (e) => {
    e.preventDefault();

    try {
      const payload = {
        name: formData.name,
        description: formData.description,
        duration: Number(formData.duration),
        price: Number(formData.price),
      };

      const createdService = await servicesService.create(payload);

      setServices(prev => [...prev, createdService]);

      toast.success("Услуга успешно добавлена!");
      handleCloseModal();
    } catch (error) {
      console.error("Ошибка при добавлении услуги:", error);

      toast.error(
        error?.response?.data?.detail || "Не удалось добавить услугу"
      );
    }
  };

  // Подтверждение удаления услуги
  const handleConfirmDelete = async () => {
    if (!serviceToDelete) return;

    try {
      // Отправляем DELETE на сервер
      await servicesService.delete(serviceToDelete.id);

      // Удаляем услугу из локального стейта
      setServices(prev =>
        prev.filter(service => service.id !== serviceToDelete.id)
      );

      toast.success("Услуга успешно удалена!");
      handleCloseModal();
    } catch (error) {
      console.error("Ошибка при удалении услуги:", error);
      toast.error(
        error?.response?.data?.detail || "Не удалось удалить услугу"
      );
    }
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
    } else {
      setFormData({
        name: '',
        description: '',
        duration: '',
        price: ''
      });
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.headerLeft}>
          <h1 className={styles.title}>Услуги</h1>
          <div className={styles.stats}>
            Всего услуг: <span className={styles.count}>{services.length}</span>
          </div>
        </div>
        <button
          className={styles.addButton}
          onClick={handleAddClick}
        >
          + Добавить услугу
        </button>
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
              <div className={styles.serviceActions}>
                <span className={styles.serviceDuration}>{service.duration} мин.</span>
                <button
                  className={styles.deleteButton}
                  onClick={(e) => handleDeleteClick(service, e)}
                  title="Удалить услугу"
                >
                  ✕
                </button>
              </div>
            </div>
            <div className={styles.servicePrice}>{service.price} ₽</div>
            <p className={styles.serviceDescription}>{service.description}</p>
            <div className={styles.editHint}>Нажмите для редактирования</div>
          </div>
        ))}
      </div>

      {services.length === 0 && (
        <div className={styles.emptyState}>
          <p>Услуги пока не добавлены</p>
          <button
            className={styles.addButton}
            onClick={handleAddClick}
          >
            + Добавить первую услугу
          </button>
        </div>
      )}

      {/* Модальное окно редактирования */}
      {isModalOpen && (
        <div className={styles.modalOverlay}>
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

      {/* Модальное окно добавления */}
      {isAddModalOpen && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <h2>Добавление услуги</h2>
              <button
                className={styles.closeButton}
                onClick={handleCloseModal}
              >
                ×
              </button>
            </div>

            <form onSubmit={handleAddService} className={styles.modalForm}>
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
                  placeholder="Введите название услуги"
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
                  placeholder="Опишите услугу"
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
                  Добавить услугу
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Модальное окно подтверждения удаления */}
      {isDeleteModalOpen && serviceToDelete && (
        <div className={styles.modalOverlay} onClick={handleCloseModal}>
          <div className={styles.deleteModal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.deleteModalIcon}>⚠️</div>
            <h2 className={styles.deleteModalTitle}>Удалить услугу</h2>
            <p className={styles.deleteModalText}>
              Вы уверены, что хотите удалить услугу <strong>«{serviceToDelete.name}»</strong>?
              Это действие нельзя отменить.
            </p>
            <div className={styles.deleteModalActions}>
              <button
                className={styles.deleteModalCancel}
                onClick={handleCloseModal}
              >
                Отмена
              </button>
              <button
                className={styles.deleteModalConfirm}
                onClick={handleConfirmDelete}
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ServicesPage;
