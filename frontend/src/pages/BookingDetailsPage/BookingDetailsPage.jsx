import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styles from './BookingDetailsPage.module.css';

const BookingDetailsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Данные из предыдущей страницы (из модального окна выбора времени)
  const bookingData = location.state || {
    service: {
      name: 'Стрижка мужская',
      duration: '60 мин',
      price: '1500 ₽'
    },
    date: '2024-01-15',
    time: '10:00'
  };

  const [formData, setFormData] = useState({
    name: '',
    phone: ''
  });

  const [errors, setErrors] = useState({});

  // Моковые данные компании
  const companyInfo = {
    name: 'Салон красоты "Элегант"',
    address: 'г. Екатеринбург, ул. Ленина, 45',
    phone: '+7 (912) 345-67-89'
  };

  // Обработчик изменения полей
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Очищаем ошибку при вводе
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  // Валидация формы
  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Введите ваше имя';
    } else if (formData.name.trim().length < 2) {
      newErrors.name = 'Имя должно содержать минимум 2 символа';
    }

    if (!formData.phone.trim()) {
      newErrors.phone = 'Введите ваш телефон';
    } else if (!/^(\+7|8)?[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/.test(formData.phone.replace(/\s/g, ''))) {
      newErrors.phone = 'Введите корректный номер телефона';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Обработчик отправки формы
  const handleSubmit = (e) => {
    e.preventDefault();

    if (validateForm()) {
      // Переход на страницу подтверждения с данными
      navigate('/booking-confirmation', {
        state: {
          ...bookingData,
          clientInfo: formData,
          companyInfo: companyInfo
        }
      });
    }
  };

  // Форматирование даты
  const formatDisplayDate = (dateString) => {
    const date = new Date(dateString);
    const options = {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    };
    return date.toLocaleDateString('ru-RU', options);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Детали записи</h1>
        <p className={styles.subtitle}>Пожалуйста, заполните ваши данные для завершения записи</p>
      </div>

      <div className={styles.content}>
        {/* Информация о записи */}
        <div className={styles.bookingSummary}>
          <h2 className={styles.summaryTitle}>Информация о записи</h2>
          <div className={styles.summaryCard}>
            <div className={styles.summaryItem}>
              <span className={styles.summaryLabel}>Услуга:</span>
              <span className={styles.summaryValue}>{bookingData.service.name}</span>
            </div>
            <div className={styles.summaryItem}>
              <span className={styles.summaryLabel}>Дата и время:</span>
              <span className={styles.summaryValue}>
                {formatDisplayDate(bookingData.date)} в {bookingData.time}
              </span>
            </div>
            <div className={styles.summaryItem}>
              <span className={styles.summaryLabel}>Длительность:</span>
              <span className={styles.summaryValue}>{bookingData.service.duration}</span>
            </div>
            <div className={styles.summaryItem}>
              <span className={styles.summaryLabel}>Стоимость:</span>
              <span className={styles.summaryPrice}>{bookingData.service.price}</span>
            </div>
          </div>

          <div className={styles.companyInfo}>
            <h3 className={styles.companyTitle}>{companyInfo.name}</h3>
            <p className={styles.companyAddress}>📍 {companyInfo.address}</p>
            <p className={styles.companyPhone}>📞 {companyInfo.phone}</p>
          </div>
        </div>

        {/* Форма для данных клиента */}
        <form onSubmit={handleSubmit} className={styles.bookingForm}>
          <h2 className={styles.formTitle}>Ваши данные</h2>

          <div className={styles.formGroup}>
            <label htmlFor="name" className={styles.label}>
              Имя *
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className={`${styles.input} ${errors.name ? styles.inputError : ''}`}
              placeholder="Введите ваше имя"
            />
            {errors.name && <span className={styles.error}>{errors.name}</span>}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="phone" className={styles.label}>
              Телефон *
            </label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleInputChange}
              className={`${styles.input} ${errors.phone ? styles.inputError : ''}`}
              placeholder="+7 (XXX) XXX-XX-XX"
            />
            {errors.phone && <span className={styles.error}>{errors.phone}</span>}
          </div>

          <div className={styles.formNote}>
            <p>📞 После записи с вами свяжутся для подтверждения</p>
            <p>⏰ Пожалуйста, приходите за 5-10 минут до назначенного времени</p>
          </div>

          <button type="submit" className={styles.submitButton}>
            Записаться
          </button>
        </form>
      </div>
    </div>
  );
};

export default BookingDetailsPage;
