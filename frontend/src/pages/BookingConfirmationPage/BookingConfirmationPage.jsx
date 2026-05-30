import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styles from './BookingConfirmationPage.module.css';

const BookingConfirmationPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const bookingData = location.state || {
    service: {
      name: 'Стрижка мужская',
      price: '1500 ₽'
    },
    date: '2024-01-15',
    time: '10:00',
    clientInfo: {
      name: 'Иван Иванов',
      phone: '+7 (912) 345-67-89'
    },
    companyInfo: {
      name: 'Салон красоты "Элегант"',
      address: 'г. Екатеринбург, ул. Ленина, 45'
    }
  };

  const handleMyBookingsClick = () => {

    navigate('/my-bookings');
  };

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
      <div className={styles.confirmationCard}>
        <div className={styles.successIcon}>✅</div>

        <h1 className={styles.title}>Вы записаны!</h1>

        <p className={styles.subtitle}>
          Запись успешно создана. С вами свяжутся для подтверждения.
        </p>

        <div className={styles.bookingDetails}>
          <div className={styles.detailSection}>
            <h2 className={styles.detailTitle}>Детали записи</h2>

            <div className={styles.detailItem}>
              <span className={styles.detailLabel}>Услуга:</span>
              <span className={styles.detailValue}>{bookingData.service.name}</span>
            </div>

            <div className={styles.detailItem}>
              <span className={styles.detailLabel}>Дата и время:</span>
              <span className={styles.detailValue}>
                {formatDisplayDate(bookingData.date)} в {bookingData.time}
              </span>
            </div>

            <div className={styles.detailItem}>
              <span className={styles.detailLabel}>Стоимость:</span>
              <span className={styles.detailPrice}>{bookingData.service.price}</span>
            </div>
          </div>

          <div className={styles.detailSection}>
            <h2 className={styles.detailTitle}>Ваши данные</h2>

            <div className={styles.detailItem}>
              <span className={styles.detailLabel}>Имя:</span>
              <span className={styles.detailValue}>{bookingData.clientInfo.name}</span>
            </div>

            <div className={styles.detailItem}>
              <span className={styles.detailLabel}>Телефон:</span>
              <span className={styles.detailValue}>{bookingData.clientInfo.phone}</span>
            </div>
          </div>

          <div className={styles.detailSection}>
            <h2 className={styles.detailTitle}>Адрес</h2>

            <div className={styles.addressCard}>
              <div className={styles.companyName}>{bookingData.companyInfo.name}</div>
              <div className={styles.companyAddress}>📍 {bookingData.companyInfo.address}</div>
            </div>
          </div>
        </div>

        <div className={styles.instructions}>
          <h3 className={styles.instructionsTitle}>Что дальше?</h3>
          <ul className={styles.instructionsList}>
            <li>⏰ Приходите за 5-10 минут до назначенного времени</li>
            <li>📱 Сохраните эту информацию</li>
            <li>🔄 Вы можете отменить запись в разделе "Мои записи"</li>
          </ul>
        </div>

        <div className={styles.actions}>
          <button
            onClick={handleMyBookingsClick}
            className={styles.myBookingsButton}
          >
            Мои записи
          </button>
        </div>
      </div>
    </div>
  );
};

export default BookingConfirmationPage;
