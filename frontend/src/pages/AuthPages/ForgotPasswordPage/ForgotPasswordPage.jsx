import React, {useEffect, useRef, useState} from 'react';
import { Link } from 'react-router-dom';
import styles from '../Auth.module.css';
import {authService} from "../../../services/authService.js";
import {toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState('');

  const emailInputRef = useRef(null);

  useEffect(() => {
    emailInputRef.current?.focus();
  }, []);

  const handleChange = (e) => {
    const value = e.target.value;
    setEmail(value);

    if (!validateEmail(value)) {
      setError('Введите корректный email');
    } else {
      setError('');
    }
  };

  const validateEmail = (value) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateEmail(email)) {
      setError('Введите корректный email');
      return;
    }

    try {
      const result = await authService.forgotPassword(email);
      console.log('Ответ сервера:', result);
      setIsSubmitted(true);
    } catch (err) {
      console.error('Ошибка восстановления пароля:', err);
      toast.error("Ошибка сервера, попробуйте позже");
    }
  };

  if (isSubmitted) {
    return (
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <div className={styles.authHeader}>
            <div className={styles.successIcon}>✅</div>
            <h2>Письмо отправлено!</h2>
            <p>Мы отправили инструкции по восстановлению пароля на email: <strong>{email}</strong></p>
          </div>

          <div className={styles.authLinks} style={{ justifyContent: 'center', marginTop: '2rem' }}>
            <Link to="/login" className={`${styles.btn} ${styles.btnPrimary}`}>
              Вернуться к входу
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <div className={styles.authHeader}>
          <h2>Восстановление пароля</h2>
          <p>Введите email, указанный при регистрации</p>
        </div>

        <form onSubmit={handleSubmit} className={styles.authForm}>
          <div className={styles.formGroup}>
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={handleChange}
              placeholder="example@mail.ru"
              required
              ref={emailInputRef}
            />
            {error && <span className={styles.error}>{error}</span>}
          </div>

          <button
            type="submit"
            className={`${styles.btn} ${styles.btnPrimary} ${styles.btnFull}`}
            disabled={!email || !!error}
          >
            Восстановить пароль
          </button>

          <div className={styles.authLinks}>
            <Link to="/login" className={styles.authLink}>
              ← Вернуться к входу
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ForgotPasswordPage;
