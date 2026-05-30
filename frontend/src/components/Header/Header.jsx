import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Header.module.css';
import {authService} from "../../services/authService.js";

const Header = ({ title, showLogout = true }) => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await authService.logout();
    } finally {
      localStorage.removeItem("accessToken");
      navigate("/", { replace: true });
    }
  };

  const handleGoToSchedule = () => {
    navigate('/schedule');
  };

  const handleGoToServices = () => {
    navigate('/services');
  };

  const handleGoToSettings = () => {
    navigate('/settings');
  };

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.leftSection}>
          <h1 className={styles.title}>{title}</h1>
          <nav className={styles.nav}>
            <button
              className={styles.navButton}
              onClick={handleGoToSchedule}
            >
              Расписание
            </button>
            <button
              className={styles.navButton}
              onClick={handleGoToServices}
            >
              Услуги
            </button>
            <button
              className={styles.navButton}
              onClick={handleGoToSettings}
            >
              Настройки
            </button>
          </nav>
        </div>

        {showLogout && (
          <div className={styles.rightSection}>
            <button
              className={styles.logoutButton}
              onClick={handleLogout}
            >
              Выйти из учетной записи
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
