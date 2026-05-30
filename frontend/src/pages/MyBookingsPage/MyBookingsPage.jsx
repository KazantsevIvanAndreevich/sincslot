import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './MyBookingsPage.module.css';

const MyBookingsPage = () => {
  const navigate = useNavigate();
  const [bookings, setBookings] = useState([]);
  const [selectedBooking, setSelectedBooking] = useState(null);
  const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false);
  const [isCancelModalOpen, setIsCancelModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [userPhone, setUserPhone] = useState('');

  // Моковые данные записей (всегда показываем их)
  const mockBookings = [
    {
      id: 1,
      serviceName: 'Стрижка мужская',
      serviceDuration: '60 мин',
      servicePrice: '1500 ₽',
      companyName: 'Салон красоты "Элегант"',
      companyAddress: 'г. Екатеринбург, ул. Ленина, 45',
      date: '2024-01-20',
      time: '10:00',
      status: 'Подтвержден',
      clientName: 'Иван Иванов',
      clientPhone: '+7 (912) 345-67-89',
      createdAt: '2024-01-15'
    },
    {
      id: 2,
      serviceName: 'Маникюр',
      serviceDuration: '90 мин',
      servicePrice: '2000 ₽',
      companyName: 'Салон красоты "Элегант"',
      companyAddress: 'г. Екатеринбург, ул. Ленина, 45',
      date: '2024-01-22',
      time: '14:30',
      status: 'Ожидание',
      clientName: 'Мария Петрова',
      clientPhone: '+7 (923) 456-78-90',
      createdAt: '2024-01-18'
    },
    {
      id: 3,
      serviceName: 'Массаж спины',
      serviceDuration: '45 мин',
      servicePrice: '2500 ₽',
      companyName: 'Салон красоты "Элегант"',
      companyAddress: 'г. Екатеринбург, ул. Ленина, 45',
      date: '2024-01-25',
      time: '11:00',
      status: 'Подтвержден',
      clientName: 'Алексей Сидоров',
      clientPhone: '+7 (934) 567-89-01',
      createdAt: '2024-01-20'
    },
    {
      id: 4,
      serviceName: 'SPA-процедура',
      serviceDuration: '120 мин',
      servicePrice: '5000 ₽',
      companyName: 'Салон красоты "Элегант"',
      companyAddress: 'г. Екатеринбург, ул. Ленина, 45',
      date: '2024-01-18',
      time: '16:00',
      status: 'Отменен',
      clientName: 'Екатерина Козлова',
      clientPhone: '+7 (945) 678-90-12',
      createdAt: '2024-01-10',
      cancelledAt: '2024-01-12'
    },
    {
      id: 5,
      serviceName: 'Консультация',
      serviceDuration: '30 мин',
      servicePrice: '1000 ₽',
      companyName: 'Салон красоты "Элегант"',
      companyAddress: 'г. Екатеринбург, ул. Ленина, 45',
      date: '2024-01-21',
      time: '09:30',
      status: 'Ожидание',
      clientName: 'Сергей Федоров',
      clientPhone: '+7 (956) 789-01-23',
      createdAt: '2024-01-19'
    }
  ];

  useEffect(() => {
    // Проверяем, авторизован ли пользователь (есть ли телефон в sessionStorage)
    const phone = sessionStorage.getItem('userPhone');

    if (!phone) {
      // Если телефона нет, используем тестовый номер
      const testPhone = '+7 (999) 123-45-67';
      sessionStorage.setItem('userPhone', testPhone);
      setUserPhone(testPhone);
    } else {
      setUserPhone(phone);
    }

    // Имитация загрузки данных
    setTimeout(() => {
      // В тестовом режиме показываем все моковые данные
      // (в реальном приложении здесь был бы API запрос)
      setBookings(mockBookings);
      setIsLoading(false);
    }, 800);
  }, [navigate]);

  const handleBookingClick = (booking) => {
    setSelectedBooking(booking);
    setIsDetailsModalOpen(true);
  };

  const handleCancelClick = (booking) => {
    setSelectedBooking(booking);
    setIsCancelModalOpen(true);
  };

  const handleCloseDetailsModal = () => {
    setIsDetailsModalOpen(false);
    setSelectedBooking(null);
  };

  const handleCloseCancelModal = () => {
    setIsCancelModalOpen(false);
    setSelectedBooking(null);
  };

  const handleConfirmCancel = () => {
    if (selectedBooking) {
      // Обновляем статус записи
      const updatedBookings = bookings.map(booking =>
        booking.id === selectedBooking.id
          ? {
              ...booking,
              status: 'Отменен',
              cancelledAt: new Date().toISOString().split('T')[0]
            }
          : booking
      );

      setBookings(updatedBookings);
      setIsCancelModalOpen(false);
      setIsDetailsModalOpen(false);
      setSelectedBooking(null);

      alert('Запись успешно отменена');
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem('userPhone');
    navigate('/my-bookings-auth');
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      weekday: 'short',
      day: 'numeric',
      month: 'long'
    });
  };

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

  const getStatusText = (status) => {
    switch (status) {
      case 'Подтвержден':
        return 'Подтверждена';
      case 'Ожидание':
        return 'Ожидает подтверждения';
      case 'Отменен':
        return 'Отменена';
      default:
        return status;
    }
  };

  // Функция для добавления тестовой записи (для тестирования)
  const addTestBooking = () => {
    const newBooking = {
      id: Date.now(),
      serviceName: 'Тестовая услуга',
      serviceDuration: '60 мин',
      servicePrice: '2000 ₽',
      companyName: 'Тестовая компания',
      companyAddress: 'г. Тестовый, ул. Тестовая, 1',
      date: '2024-01-30',
      time: '15:00',
      status: 'Ожидание',
      clientName: 'Тестовый Клиент',
      clientPhone: userPhone,
      createdAt: new Date().toISOString().split('T')[0]
    };

    setBookings(prev => [newBooking, ...prev]);
    alert('Тестовая запись добавлена!');
  };

  if (isLoading) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.loadingSpinner}></div>
        <p>Загружаем ваши записи...</p>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.headerLeft}>
            <h1 className={styles.title}>Мои записи</h1>
            <div className={styles.userInfo}>
              <p className={styles.userPhone}>📱 {userPhone}</p>
              <p className={styles.testNote}>👆 Все записи показаны для тестирования</p>
            </div>
          </div>
          <div className={styles.headerRight}>
            <button
              className={styles.testButton}
              onClick={addTestBooking}
            >
              + Тестовая запись
            </button>
            <button
              className={styles.logoutButton}
              onClick={handleLogout}
            >
              Выйти
            </button>
          </div>
        </div>
      </header>

      <div className={styles.content}>
        <div className={styles.stats}>
          <div className={styles.statItem}>
            <span className={styles.statLabel}>Всего записей:</span>
            <span className={styles.statValue}>{bookings.length}</span>
          </div>
          <div className={styles.statItem}>
            <span className={styles.statLabel}>Активные:</span>
            <span className={styles.statValue}>
              {bookings.filter(b => b.status !== 'Отменен').length}
            </span>
          </div>
          <div className={styles.statItem}>
            <span className={styles.statLabel}>Ожидание:</span>
            <span className={styles.statValue}>
              {bookings.filter(b => b.status === 'Ожидание').length}
            </span>
          </div>
          <div className={styles.statItem}>
            <span className={styles.statLabel}>Отменены:</span>
            <span className={styles.statValue}>
              {bookings.filter(b => b.status === 'Отменен').length}
            </span>
          </div>
        </div>

        <div className={styles.bookingsGrid}>
          {bookings.map((booking) => (
            <div
              key={booking.id}
              className={`${styles.bookingCard} ${booking.status === 'Отменен' ? styles.cancelled : ''}`}
              onClick={() => handleBookingClick(booking)}
            >
              <div className={styles.bookingHeader}>
                <div className={styles.serviceInfo}>
                  <h3 className={styles.serviceName}>{booking.serviceName}</h3>
                  <span className={styles.serviceDuration}>{booking.serviceDuration}</span>
                </div>
                <div className={styles.bookingStatus}>
                  <span className={`${styles.status} ${getStatusClass(booking.status)}`}>
                    {getStatusText(booking.status)}
                  </span>
                </div>
              </div>

              <div className={styles.bookingDetails}>
                <div className={styles.dateTime}>
                  <span className={styles.dateIcon}>📅</span>
                  <span>{formatDate(booking.date)}</span>
                  <span className={styles.time}>⏰ {booking.time}</span>
                </div>
                <div className={styles.price}>{booking.servicePrice}</div>
              </div>

              <div className={styles.companyInfo}>
                <span className={styles.companyIcon}>🏢</span>
                <span className={styles.companyName}>{booking.companyName}</span>
              </div>

              <div className={styles.bookingActions}>
                {booking.status !== 'Отменен' && (
                  <button
                    className={styles.cancelButton}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleCancelClick(booking);
                    }}
                  >
                    Отменить запись
                  </button>
                )}
                <button
                  className={styles.detailsButton}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleBookingClick(booking);
                  }}
                >
                  Подробнее
                </button>
              </div>
            </div>
          ))}
        </div>

      </div>

      {/* Модальное окно с деталями записи */}
      {isDetailsModalOpen && selectedBooking && (
        <div className={styles.modalOverlay} onClick={handleCloseDetailsModal}>
          <div className={styles.detailsModal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <h2>Детали записи</h2>
              <button
                className={styles.closeButton}
                onClick={handleCloseDetailsModal}
              >
                ×
              </button>
            </div>

            <div className={styles.modalContent}>
              <div className={styles.bookingSummary}>
                <div className={styles.summarySection}>
                  <h3 className={styles.sectionTitle}>Услуга</h3>
                  <div className={styles.summaryItem}>
                    <span className={styles.summaryLabel}>Название:</span>
                    <span className={styles.summaryValue}>{selectedBooking.serviceName}</span>
                  </div>
                  <div className={styles.summaryItem}>
                    <span className={styles.summaryLabel}>Длительность:</span>
                    <span className={styles.summaryValue}>{selectedBooking.serviceDuration}</span>
                  </div>
                  <div className={styles.summaryItem}>
                    <span className={styles.summaryLabel}>Стоимость:</span>
                    <span className={styles.summaryPrice}>{selectedBooking.servicePrice}</span>
                  </div>
                </div>

                <div className={styles.summarySection}>
                  <h3 className={styles.sectionTitle}>Дата и время</h3>
                  <div className={styles.summaryItem}>
                    <span className={styles.summaryLabel}>Дата:</span>
                    <span className={styles.summaryValue}>
                      {new Date(selectedBooking.date).toLocaleDateString('ru-RU', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </span>
                  </div>
                  <div className={styles.summaryItem}>
                    <span className={styles.summaryLabel}>Время:</span>
                    <span className={styles.summaryValue}>{selectedBooking.time}</span>
                  </div>
                  <div className={styles.summaryItem}>
                    <span className={styles.summaryLabel}>Статус:</span>
                    <span className={`${styles.summaryStatus} ${getStatusClass(selectedBooking.status)}`}>
                      {getStatusText(selectedBooking.status)}
                    </span>
                  </div>
                </div>

                <div className={styles.summarySection}>
                  <h3 className={styles.sectionTitle}>Компания</h3>
                  <div className={styles.companyDetails}>
                    <div className={styles.companyName}>{selectedBooking.companyName}</div>
                    <div className={styles.companyAddress}>📍 {selectedBooking.companyAddress}</div>
                  </div>
                </div>

                <div className={styles.summarySection}>
                  <h3 className={styles.sectionTitle}>Ваши данные</h3>
                  <div className={styles.clientDetails}>
                    <div className={styles.clientItem}>
                      <span className={styles.clientLabel}>Имя:</span>
                      <span className={styles.clientValue}>{selectedBooking.clientName}</span>
                    </div>
                    <div className={styles.clientItem}>
                      <span className={styles.clientLabel}>Телефон:</span>
                      <span className={styles.clientValue}>{selectedBooking.clientPhone}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className={styles.modalActions}>
                {selectedBooking.status !== 'Отменен' && (
                  <button
                    className={styles.cancelActionButton}
                    onClick={() => {
                      handleCloseDetailsModal();
                      handleCancelClick(selectedBooking);
                    }}
                  >
                    Отменить запись
                  </button>
                )}
                <button
                  className={styles.closeActionButton}
                  onClick={handleCloseDetailsModal}
                >
                  Закрыть
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Модальное окно подтверждения отмены */}
      {isCancelModalOpen && selectedBooking && (
        <div className={styles.modalOverlay} onClick={handleCloseCancelModal}>
          <div className={styles.cancelModal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.cancelModalIcon}>⚠️</div>
            <h2 className={styles.cancelModalTitle}>Отмена записи</h2>
            <div className={styles.cancelModalContent}>
              <p className={styles.cancelModalText}>
                Вы уверены, что хотите отменить запись на услугу <strong>«{selectedBooking.serviceName}»</strong>?
              </p>
              <div className={styles.appointmentDetails}>
                <div className={styles.detailItem}>
                  <span className={styles.detailLabel}>Дата и время:</span>
                  <span className={styles.detailValue}>
                    {formatDate(selectedBooking.date)} в {selectedBooking.time}
                  </span>
                </div>
                <div className={styles.detailItem}>
                  <span className={styles.detailLabel}>Компания:</span>
                  <span className={styles.detailValue}>{selectedBooking.companyName}</span>
                </div>
              </div>
              <div className={styles.cancelModalWarning}>
                После отмены вы сможете записаться на другое удобное время.
              </div>
            </div>
            <div className={styles.cancelModalActions}>
              <button
                className={styles.cancelModalCancel}
                onClick={handleCloseCancelModal}
              >
                Вернуться
              </button>
              <button
                className={styles.cancelModalConfirm}
                onClick={handleConfirmCancel}
              >
                Отменить запись
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MyBookingsPage;
