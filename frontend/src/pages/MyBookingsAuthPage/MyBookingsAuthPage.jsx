import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './MyBookingsAuthPage.module.css';

const MyBookingsAuthPage = () => {
  const navigate = useNavigate();
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const validatePhone = (phoneNumber) => {
    // Простая валидация российских номеров
    const cleanedPhone = phoneNumber.replace(/\D/g, '');
    return cleanedPhone.length >= 10 && cleanedPhone.length <= 12;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!phone.trim()) {
      setError('Введите номер телефона');
      return;
    }

    if (!validatePhone(phone)) {
      setError('Введите корректный номер телефона');
      return;
    }

    setIsLoading(true);

    // Имитация запроса к API
    setTimeout(() => {
      setIsLoading(false);
      // Сохраняем телефон в sessionStorage для дальнейшего использования
      sessionStorage.setItem('userPhone', phone);
      // Переходим на страницу записей
      navigate('/my-bookings');
    }, 1000);
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h1 className={styles.title}>Мои записи</h1>
          <p className={styles.subtitle}>Введите номер телефона, чтобы посмотреть свои записи</p>
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="phone" className={styles.label}>
              Номер телефона
            </label>
            <input
              type="tel"
              id="phone"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className={`${styles.input} ${error ? styles.inputError : ''}`}
              placeholder="+7 (XXX) XXX-XX-XX"
              disabled={isLoading}
            />
            {error && <span className={styles.error}>{error}</span>}
          </div>

          <div className={styles.infoBox}>
            <p>🔒 Ваши данные защищены</p>
            <p>📅 Вы увидите все свои текущие записи</p>
          </div>

          <button
            type="submit"
            className={styles.submitButton}
            disabled={isLoading}
          >
            {isLoading ? (
              <span className={styles.loadingText}>Проверяем...</span>
            ) : (
              'Посмотреть записи'
            )}
          </button>
        </form>

        <div className={styles.footer}>
          <p className={styles.footerText}>
            Нет записей? <button className={styles.linkButton} onClick={() => navigate('/booking')}>Записаться сейчас</button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default MyBookingsAuthPage;
