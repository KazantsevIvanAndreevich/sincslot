import React, { useState } from 'react';
import Header from '../../components/Header/Header';
import styles from './SchedulePage.module.css';

const SchedulePage = () => {
  // Моковые данные для демонстрации
  const [appointments, setAppointments] = useState([
    {
      id: 1,
      clientName: 'Иванов Алексей',
      phone: '+7 (912) 345-67-89',
      service: 'Стрижка',
      date: '2024-01-15',
      time: '10:00',
      status: 'Ожидание' // Изменено с "Подтвержден" на "Ожидание"
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
  const [isCancelModalOpen, setIsCancelModalOpen] = useState(false);
  const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
  const [appointmentToCancel, setAppointmentToCancel] = useState(null);
  const [appointmentToConfirm, setAppointmentToConfirm] = useState(null);

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

  // Открытие модального окна отмены записи
  const handleCancelClick = (appointment, e) => {
    e.stopPropagation();
    if (appointment.status === 'Отменен') {
      return;
    }
    setAppointmentToCancel(appointment);
    setIsCancelModalOpen(true);
  };

  // Открытие модального окна подтверждения записи
  const handleConfirmClick = (appointment, e) => {
    e.stopPropagation();
    if (appointment.status === 'Подтвержден' || appointment.status === 'Отменен') {
      return;
    }
    setAppointmentToConfirm(appointment);
    setIsConfirmModalOpen(true);
  };

  // Закрытие модальных окон
  const handleCloseCancelModal = () => {
    setIsCancelModalOpen(false);
    setAppointmentToCancel(null);
  };

  const handleCloseConfirmModal = () => {
    setIsConfirmModalOpen(false);
    setAppointmentToConfirm(null);
  };

  // Подтверждение отмены записи
  const handleConfirmCancel = () => {
    if (appointmentToCancel) {
      const updatedAppointments = appointments.map(appointment =>
        appointment.id === appointmentToCancel.id
          ? { ...appointment, status: 'Отменен' }
          : appointment
      );
      setAppointments(updatedAppointments);
    }
    handleCloseCancelModal();
  };

  // Подтверждение записи
  const handleConfirmAppointment = () => {
    if (appointmentToConfirm) {
      const updatedAppointments = appointments.map(appointment =>
        appointment.id === appointmentToConfirm.id
          ? { ...appointment, status: 'Подтвержден' }
          : appointment
      );
      setAppointments(updatedAppointments);
    }
    handleCloseConfirmModal();
  };

  // Восстановление записи
  const handleRestoreClick = (appointment, e) => {
    e.stopPropagation();
    const updatedAppointments = appointments.map(apt =>
      apt.id === appointment.id
        ? { ...apt, status: 'Ожидание' }
        : apt
    );
    setAppointments(updatedAppointments);
  };

  return (
    <div className={styles.pageContainer}>
      <Header title="SyncSlot" />

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
                <th className={styles.actionsHeader}>Действия</th>
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
                  <td className={styles.actionsCell}>
                    {appointment.status === 'Ожидание' && (
                      <>
                        <button
                          className={styles.confirmButton}
                          onClick={(e) => handleConfirmClick(appointment, e)}
                          title="Подтвердить запись"
                        >
                          Подтвердить
                        </button>
                        <button
                          className={styles.cancelButton}
                          onClick={(e) => handleCancelClick(appointment, e)}
                          title="Отменить запись"
                        >
                          Отменить
                        </button>
                      </>
                    )}
                    {appointment.status === 'Подтвержден' && (
                      <button
                        className={styles.cancelButton}
                        onClick={(e) => handleCancelClick(appointment, e)}
                        title="Отменить запись"
                      >
                        Отменить
                      </button>
                    )}
                    {appointment.status === 'Отменен' && (
                      <button
                        className={styles.restoreButton}
                        onClick={(e) => handleRestoreClick(appointment, e)}
                        title="Восстановить запись"
                      >
                        Восстановить
                      </button>
                    )}
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

        {/* Модальное окно подтверждения записи */}
        {isConfirmModalOpen && appointmentToConfirm && (
          <div className={styles.modalOverlay} onClick={handleCloseConfirmModal}>
            <div className={styles.confirmModal} onClick={(e) => e.stopPropagation()}>
              <div className={styles.confirmModalIcon}>✅</div>
              <h2 className={styles.confirmModalTitle}>Подтверждение записи</h2>
              <div className={styles.confirmModalContent}>
                <p className={styles.confirmModalText}>
                  Подтвердить запись клиента <strong>«{appointmentToConfirm.clientName}»</strong>?
                </p>
                <div className={styles.appointmentDetails}>
                  <div className={styles.detailItem}>
                    <span className={styles.detailLabel}>Услуга:</span>
                    <span className={styles.detailValue}>{appointmentToConfirm.service}</span>
                  </div>
                  <div className={styles.detailItem}>
                    <span className={styles.detailLabel}>Дата и время:</span>
                    <span className={styles.detailValue}>
                      {new Date(appointmentToConfirm.date).toLocaleDateString('ru-RU')} в {appointmentToConfirm.time}
                    </span>
                  </div>
                  <div className={styles.detailItem}>
                    <span className={styles.detailLabel}>Телефон:</span>
                    <span className={styles.detailValue}>{appointmentToConfirm.phone}</span>
                  </div>
                </div>
                <div className={styles.confirmModalInfo}>
                  После подтверждения клиенту будет отправлено уведомление.
                </div>
              </div>
              <div className={styles.confirmModalActions}>
                <button
                  className={styles.confirmModalCancel}
                  onClick={handleCloseConfirmModal}
                >
                  Отмена
                </button>
                <button
                  className={styles.confirmModalConfirm}
                  onClick={handleConfirmAppointment}
                >
                  Подтвердить запись
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Модальное окно отмены записи */}
        {isCancelModalOpen && appointmentToCancel && (
          <div className={styles.modalOverlay} onClick={handleCloseCancelModal}>
            <div className={styles.cancelModal} onClick={(e) => e.stopPropagation()}>
              <div className={styles.cancelModalIcon}>📞</div>
              <h2 className={styles.cancelModalTitle}>Отмена записи</h2>
              <div className={styles.cancelModalContent}>
                <p className={styles.cancelModalText}>
                  Вы уверены, что хотите отменить запись клиента <strong>«{appointmentToCancel.clientName}»</strong>?
                </p>
                <div className={styles.appointmentDetails}>
                  <div className={styles.detailItem}>
                    <span className={styles.detailLabel}>Услуга:</span>
                    <span className={styles.detailValue}>{appointmentToCancel.service}</span>
                  </div>
                  <div className={styles.detailItem}>
                    <span className={styles.detailLabel}>Дата и время:</span>
                    <span className={styles.detailValue}>
                      {new Date(appointmentToCancel.date).toLocaleDateString('ru-RU')} в {appointmentToCancel.time}
                    </span>
                  </div>
                  <div className={styles.detailItem}>
                    <span className={styles.detailLabel}>Телефон:</span>
                    <span className={styles.detailValue}>{appointmentToCancel.phone}</span>
                  </div>
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
                  Подтвердить отмену
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SchedulePage;
