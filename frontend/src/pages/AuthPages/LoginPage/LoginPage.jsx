import React, { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import styles from '../Auth.module.css';
import { authService } from "../../../services/authService";
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Login = () => {
  const navigate = useNavigate();
  const inputRefs = useRef([]);

  useEffect(() => {
    inputRefs.current[0]?.focus();
  }, []);

  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState({});
  const [isFormValid, setIsFormValid] = useState(false);

 const validateField = (name, value) => {
    switch (name) {
      case 'email': {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!value.trim()) {
          return 'Поле обязательно для заполнения';
        }
        return emailRegex.test(value) ? '' : 'Введите корректный email';
      }
      case 'password':
        if (!value.trim()) {
          return 'Поле обязательно для заполнения';
        }
        return '';
      default:
        return '';
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => {
      const newFormData = { ...prev, [name]: value };

      setErrors((prevErrors) => {
        const newErrors = { ...prevErrors };
        newErrors[name] = validateField(name, value);

        // Проверка валидности всей формы
        setIsFormValid(newFormData.email && newFormData.password && !Object.values(newErrors).some(error => error));

        return newErrors;
      });

      return newFormData;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isFormValid) return;

    try {
      const result = await authService.login(formData);

      // Сохраняем токен
      localStorage.setItem("accessToken", result.accessToken);

      console.log('Вход успешен:', formData);

      // Перенаправляем на главную
      navigate("/schedule");

    } catch (error) {
      console.error("Ошибка входа:", error);
      const serverError = error?.response?.data?.error;
      toast.error(serverError || "Ошибка входа. Попробуйте позже");
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <div className={styles.authHeader}>
          <h2>Вход в SyncSlot</h2>
          <p>Войдите в свой аккаунт</p>
        </div>

        <form onSubmit={handleSubmit} className={styles.authForm}>
          <div className={styles.formGroup}>
            <label htmlFor="email">Email</label>
            <input
              type="email" // Изменено на тип "email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="example@mail.ru"
              required
            />
            {errors.email && <span className={styles.error}>{errors.email}</span>} {/* Отображение ошибки */}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Введите ваш пароль"
              required
            />
            {errors.password && <span className={styles.error}>{errors.password}</span>} {/* Отображение ошибки */}
          </div>

          <button
            type="submit"
            className={`${styles.btn} ${styles.btnPrimary} ${styles.btnFull}`}
            disabled={!isFormValid} // кнопка неактивна, пока есть ошибки
          >
            Войти
          </button>

          <div className={styles.authLinks}>
            <Link to="/forgot-password" className={styles.authLink}>
              Восстановить пароль
            </Link>
            <span className={styles.authDivider}>|</span>
            <Link to="/register" className={styles.authLink}>
              Зарегистрироваться
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
